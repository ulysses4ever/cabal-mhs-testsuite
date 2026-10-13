#!/usr/bin/env python3
"""Replay MicroHs's package list with cabal driving mhs.

MicroHs's Makefile.packages lists the Hackage packages that its hackage-ci
workflow installs with mcabal, the package manager of MicroHs, one
'mcabal install PKG' line each. This builds them with cabal instead, one at a
time and in the same order: for every line, a tiny executable depending on
PKG is built with cabal and mhs, into a store shared by all the steps.

What mcabal does differently is mimicked:

* The --git overrides of the Makefile become source-repository-package
  stanzas, kept in the projects of the later steps once the package builds.
* mcabal renames array and random to array-mhs and random-mhs, so copies of
  array-mhs and random-mhs, renamed back, are local packages of every project.
* mcabal ignores version bounds, so project.extra lifts the few bounds that
  stand between a package and the versions of its dependencies that support
  mhs.
* mcabal adds ghc-compat to the dependencies of every package. cabal does the
  same with the ghc-compat that mhs has installed: install it with
  'mcabal install ghc-compat' first.

Usage: replay.py --cabal CABAL --makefile MicroHs/Makefile.packages --work DIR
mhs must be on the PATH.
"""
import argparse
import json
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent

# The state of Hackage the packages are taken from, so that runs on different
# machines and days choose the same versions.
INDEX_STATE = "2026-07-16T00:00:00Z"

# The packages that mcabal replaces with a fork for mhs, and the fork.
OVERRIDES = {"array": "array-mhs-0.5.8.0", "random": "random-mhs-1.3.2.2"}

# The packages of the list that have no library, only executables.
EXE_ONLY = {"hspec-discover"}

TIMEOUT = 1800


def parse(makefile):
    """The 'mcabal install' lines of Makefile.packages, in order."""
    entries = []
    for raw in makefile.read_text().splitlines():
        line = raw.strip()
        if not line.startswith("$(MINST)"):
            continue
        rest = line[len("$(MINST)"):].split("#")[0].strip()
        git = branch = subdir = None
        pkgs = []
        for tok in shlex.split(rest):
            if tok.startswith("--git="):
                parts = tok[len("--git="):].split()
                git = parts[0]
                for part in parts[1:]:
                    if part.startswith("--branch="):
                        branch = part[len("--branch="):]
            elif tok.startswith("--dir="):
                subdir = tok[len("--dir="):]
            else:
                pkgs.append(tok)
        if len(pkgs) != 1:
            sys.exit("cannot parse: " + raw)
        entries.append({"pkg": pkgs[0], "git": git, "branch": branch, "subdir": subdir})
    return entries


def prepare_overrides(cabal, work):
    """Copies of the forks of OVERRIDES, renamed back to the original names."""
    for name, pkgid in OVERRIDES.items():
        dest = work / "overrides" / name
        if dest.exists():
            continue
        tmp = work / "overrides" / ".get"
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        subprocess.run([cabal, "get", pkgid, "--destdir=" + str(tmp)], check=True)
        src = tmp / pkgid
        fork = pkgid.rsplit("-", 1)[0]
        text = (src / (fork + ".cabal")).read_text()
        text = re.sub(r"^(name:\s*)" + re.escape(fork) + r"\s*$", r"\g<1>" + name, text, count=1, flags=re.M)
        (src / (fork + ".cabal")).unlink()
        (src / (name + ".cabal")).write_text(text)
        src.rename(dest)
        shutil.rmtree(tmp)


def project_file(git_entries, extra):
    lines = [
        "packages: corpus " + " ".join("overrides/" + name for name in OVERRIDES),
        "compiler: mhs",
        "with-compiler: mhs",
        "index-state: " + INDEX_STATE,
        "",
        extra,
        "",
    ]
    for e in git_entries:
        lines += ["source-repository-package", "  type: git", "  location: " + e["git"]]
        if e["branch"]:
            lines.append("  tag: " + e["branch"])
        if e["subdir"]:
            lines.append("  subdir: " + e["subdir"])
        lines.append("")
    return "\n".join(lines)


def corpus_cabal(pkg):
    dep = (
        "    build-tool-depends: {0}:{0}\n    build-depends:    base\n".format(pkg)
        if pkg in EXE_ONLY
        else "    build-depends:    base, {}\n".format(pkg)
    )
    return (
        "cabal-version:   3.0\nname:            corpus\nversion:         0\n"
        "build-type:      Simple\n\nexecutable corpus\n    main-is:          Main.hs\n"
        + dep
        + "    default-language: Haskell2010\n"
    )


def output(cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.strip()
    except OSError as exc:
        return str(exc)


def inputs(cabal, makefile):
    """What a run depends on, recorded with its results."""
    mhs_packages = output(["mhs", "-L"])
    return {
        "cabal": output([cabal, "--version"]).splitlines()[-1:],
        "mhs": output(["mhs", "--numeric-version"]),
        "mhs packages": [line.strip() for line in mhs_packages.splitlines() if line.startswith(" ")],
        "MicroHs commit": output(["git", "-C", str(makefile.parent), "rev-parse", "HEAD"]),
        "index-state": INDEX_STATE,
        "project.extra": (HERE / "project.extra").read_text(),
        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--cabal", required=True, help="the cabal executable to test")
    parser.add_argument("--makefile", required=True, type=pathlib.Path, help="MicroHs's Makefile.packages")
    parser.add_argument("--work", required=True, type=pathlib.Path, help="directory for the projects, store and logs")
    parser.add_argument("--first", type=int, default=0, help="index of the first package to build")
    parser.add_argument("--last", type=int, default=None, help="index of the last package to build")
    args = parser.parse_args()

    cabal = str(pathlib.Path(args.cabal).resolve())
    makefile = args.makefile.resolve()
    work = args.work.resolve()
    entries = parse(makefile)
    last = len(entries) - 1 if args.last is None else args.last
    extra = (HERE / "project.extra").read_text()

    (work / "logs").mkdir(parents=True, exist_ok=True)
    (work / "corpus").mkdir(exist_ok=True)
    (work / "corpus" / "Main.hs").write_text("module Main (main) where\n\nmain :: IO ()\nmain = return ()\n")
    prepare_overrides(cabal, work)
    results_file = work / "results.json"
    results = json.loads(results_file.read_text()) if results_file.exists() else {"packages": {}}
    results["inputs"] = inputs(cabal, makefile)
    packages = results["packages"]

    git_entries = []
    for i, e in enumerate(entries):
        pkg = e["pkg"]
        if i < args.first or i > last:
            if e["git"] and packages.get(pkg, {}).get("status") == "ok":
                git_entries.append(e)
            continue
        step_git = git_entries + ([e] if e["git"] else [])
        (work / "cabal.project").write_text(project_file(step_git, extra))
        (work / "corpus" / "corpus.cabal").write_text(corpus_cabal(pkg))
        start = time.time()
        try:
            proc = subprocess.run(
                [cabal, "--store-dir=" + str(work / "store"), "build", "corpus", "-j4", "-v1"],
                cwd=work,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=TIMEOUT,
                text=True,
            )
            out, code = proc.stdout, proc.returncode
        except subprocess.TimeoutExpired as exc:
            partial = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            out, code = partial + "\n### TIMEOUT\n", -1
        (work / "logs" / "{:03d}-{}.log".format(i, pkg)).write_text(out)
        failed = sorted(set(re.findall(r"Failed to build ([^\s]+?)(?:\.| |$)", out, re.M)))
        status = "ok" if code == 0 else ("solver" if "Could not resolve dependencies" in out else "fail")
        packages[pkg] = {
            "index": i,
            "status": status,
            "failed": failed,
            "seconds": round(time.time() - start),
            "git": bool(e["git"]),
        }
        results_file.write_text(json.dumps(results, indent=1))
        if e["git"] and status == "ok":
            git_entries.append(e)
        print("{:3d} {:28s} {:6s} {:4d}s {}".format(i, pkg, status, packages[pkg]["seconds"], " ".join(failed)), flush=True)

    failures = [pkg for pkg, r in packages.items() if r["status"] != "ok"]
    print("{} of {} packages build".format(len(packages) - len(failures), len(packages)))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
