#!/usr/bin/env python3
"""Replay MicroHs's package list with cabal driving mhs.

MicroHs's Makefile.packages lists the Hackage packages that its hackage-ci
workflow installs with mcabal, the package manager of MicroHs, one
'mcabal install PKG' line each. This builds them with cabal instead, one at a
time and in the same order: for every line, a tiny executable depending on
PKG is built with cabal and mhs, into a store shared by all the steps, and
run. mhs compiles the C sources of the libraries a program uses when it links
the program, so even the executable that does nothing compiles the C sources
of PKG and of its dependencies; for the packages of SMOKE, the executable
calls into PKG.

What mcabal does differently is mimicked:

* The --git overrides of the Makefile become source-repository-package
  stanzas, kept in the projects of the later steps once the package builds.
* mcabal adds ghc-compat to the dependencies of every package, and uses the
  forks array-mhs and random-mhs wherever a package depends on array or
  random. With the patches, cabal does the same, so mhs needs nothing
  installed besides what 'make minstall' installs.
* mcabal ignores version bounds, so project.extra lifts the few bounds that
  stand between a package and the versions of its dependencies that support
  mhs.
* mhs sees every package that mcabal has installed, and hspec-core relies on
  that: it imports the async package without depending on it. PATCHED below
  adds the missing dependency to a copy of hspec-core, which is a local
  package of the projects from its own step on.

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

# The packages of the list that have no library, only executables.
EXE_ONLY = {"hspec-discover"}


def add_async_for_mhs(text):
    """hspec-core imports Control.Concurrent.Async, whose source it vendors but
    compiles only for GHC: with mhs, it needs the async package."""
    ghc_only = "  if impl(ghc)\n    other-modules:\n        Control.Concurrent.Async\n"
    if ghc_only not in text:
        sys.exit("hspec-core.cabal has changed, see add_async_for_mhs")
    return text.replace(ghc_only, "  if impl(mhs)\n    build-depends: async\n" + ghc_only, 1)


# Packages whose description lacks something that mcabal does not need, with
# the version to patch and the patch. A patched copy is a local package of the
# projects from the step of the package on.
PATCHED = {"hspec-core": ("hspec-core-2.11.17", add_async_for_mhs)}

# The executable of most steps does nothing. For a package of SMOKE, it is the
# program given here, which calls into the package, so that running it checks
# what building the package cannot: that the C code of the package, or of the
# packages it depends on, is compiled and linked into a program as mhs needs,
# or, for the test frameworks, that much of the list works together.
SMOKE = {
    # The time zone comes from C, lib/cbits/HsTime.c and HsTime.h.
    "time": """
import Data.Time (getCurrentTimeZone, getZonedTime)

main :: IO ()
main = do
  zone <- getCurrentTimeZone
  now <- getZonedTime
  putStrLn ("time zone " ++ show zone ++ ", now " ++ show now)
""",
    # With mhs, splitmix seeds itself from the clock, with time.
    "splitmix": """
import System.Random.SplitMix (initSMGen, nextWord64)

main :: IO ()
main = do
  gen <- initSMGen
  putStrLn ("splitmix " ++ show (fst (nextWord64 gen)))
""",
    "random": """
import Control.Monad (unless)
import System.Exit (exitFailure)
import System.Random (randomRIO)

main :: IO ()
main = do
  n <- randomRIO (1, 6 :: Int)
  putStrLn ("random " ++ show n)
  unless (1 <= n && n <= 6) exitFailure
""",
    "QuickCheck": """
import Control.Monad (unless)
import System.Exit (exitFailure)
import Test.QuickCheck (isSuccess, quickCheckResult)

main :: IO ()
main = do
  result <- quickCheckResult (\\xs -> reverse (reverse xs) == (xs :: [Int]))
  unless (isSuccess result) exitFailure
""",
    "hspec": """
import Test.Hspec (describe, hspec, it, shouldBe)

main :: IO ()
main = hspec $ describe "addition" $ it "adds" $ (1 + 1 :: Int) `shouldBe` 2
""",
    # terminfo is linked with the curses library that its configure script
    # finds, which its package file passes on to the C compiler. It imports
    # most of its C functions without a header, and mhs declares no C
    # function itself, so a program compiles only if it includes term.h,
    # which declares them: cursorAddress uses tparm, whose import names it.
    "terminfo": """
import Data.Maybe (isJust)
import System.Console.Terminfo (Point, TermOutput, cursorAddress, getCapability, setupTerm, termColumns)

main :: IO ()
main = do
  term <- setupTerm "dumb"
  let cursor = getCapability term cursorAddress :: Maybe (Point -> TermOutput)
  putStrLn ("terminfo columns " ++ show (getCapability term termColumns) ++ ", cursor addressing " ++ show (isJust cursor))
""",
    # The host-order reads of binary are in C, cbits/unaligned_read.c and
    # unaligned_read.h, and decoding a Word64 makes one.
    "binary": """
import Control.Monad (unless)
import Data.Binary (decode, encode)
import Data.Binary.Get (getWord64host, runGet)
import Data.Binary.Put (putWord64host, runPut)
import Data.Word (Word64)
import System.Exit (exitFailure)

main :: IO ()
main = do
  let value = (2 ^ (40 :: Int) + 7 :: Word64, "binary")
      decoded = decode (encode value)
      word = runGet getWord64host (runPut (putWord64host 42))
  putStrLn ("binary " ++ show decoded ++ " " ++ show word)
  unless (decoded == value && word == 42) exitFailure
""",
}

TIMEOUT = 1800
RUN_TIMEOUT = 300


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



def prepare_patched(cabal, work, pkg):
    """A copy of the package, with the patch of PATCHED applied."""
    pkgid, patch = PATCHED[pkg]
    dest = work / "patched" / pkg
    if dest.exists():
        return
    tmp = work / "patched" / ".get"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    get = subprocess.run(
        [cabal, "get", pkgid, "--destdir=" + str(tmp)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    if get.returncode != 0:
        sys.exit("cabal get {} failed:\n{}".format(pkgid, get.stdout))
    cabal_file = tmp / pkgid / (pkg + ".cabal")
    cabal_file.write_text(patch(cabal_file.read_text()))
    (tmp / pkgid).rename(dest)
    shutil.rmtree(tmp)


def project_file(git_entries, patched, extra):
    lines = [
        "packages: corpus" + "".join(" patched/" + pkg for pkg in patched),
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


def corpus_main(pkg):
    return "module Main (main) where\n" + SMOKE.get(pkg, "\nmain :: IO ()\nmain = return ()\n")


def run_corpus(cabal, work):
    """Run the executable of the step: its exit code and output."""
    proc = subprocess.run(
        [cabal, "--store-dir=" + str(work / "store"), "list-bin", "corpus", "-v0"],
        cwd=work,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    lines = proc.stdout.strip().splitlines()
    if proc.returncode != 0 or not lines:
        return -1, "cabal list-bin corpus failed:\n" + proc.stdout
    try:
        run = subprocess.run(
            [lines[-1]],
            cwd=work,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=RUN_TIMEOUT,
            text=True,
        )
        return run.returncode, run.stdout
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        return -1, partial + "\n### TIMEOUT\n"
    except OSError as exc:
        return -1, str(exc)


def last_line(text):
    """The last line of the output of a program that says something, without
    the codes that control a terminal: colours, and the backspaces with which
    QuickCheck overwrites its count of tests."""
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", text)
    lines = [line.rsplit("\b", 1)[-1].strip() for line in re.split(r"[\r\n]", text)]
    return ([line for line in lines if line] or [""])[-1]


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
        "cc": output(["cc", "--version"]).splitlines()[:1],
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
    results_file = work / "results.json"
    results = json.loads(results_file.read_text()) if results_file.exists() else {"packages": {}}
    results["inputs"] = inputs(cabal, makefile)
    packages = results["packages"]

    git_entries = []
    patched = []
    for i, e in enumerate(entries):
        pkg = e["pkg"]
        if pkg in PATCHED:
            prepare_patched(cabal, work, pkg)
            patched.append(pkg)
        if i < args.first or i > last:
            if e["git"] and packages.get(pkg, {}).get("status") == "ok":
                git_entries.append(e)
            continue
        step_git = git_entries + ([e] if e["git"] else [])
        (work / "cabal.project").write_text(project_file(step_git, patched, extra))
        (work / "corpus" / "corpus.cabal").write_text(corpus_cabal(pkg))
        (work / "corpus" / "Main.hs").write_text(corpus_main(pkg))
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
        failed = sorted(set(re.findall(r"Failed to build ([^\s]+?)(?:\.| |$)", out, re.M)))
        status = "ok" if code == 0 else ("solver" if "Could not resolve dependencies" in out else "fail")
        ran = ""
        if status == "ok":
            run_code, run_out = run_corpus(cabal, work)
            out += "\n### run: exit code {}\n{}".format(run_code, run_out)
            ran = last_line(run_out)
            if run_code != 0:
                status = "run"
        (work / "logs" / "{:03d}-{}.log".format(i, pkg)).write_text(out)
        packages[pkg] = {
            "index": i,
            "status": status,
            "failed": failed,
            "output": ran,
            "seconds": round(time.time() - start),
            "git": bool(e["git"]),
        }
        results_file.write_text(json.dumps(results, indent=1))
        if e["git"] and status == "ok":
            git_entries.append(e)
        print("{:3d} {:28s} {:6s} {:4d}s {}".format(i, pkg, status, packages[pkg]["seconds"], " ".join(failed) or ran), flush=True)

    failures = [pkg for pkg, r in packages.items() if r["status"] != "ok"]
    print("{} of {} packages build and run".format(len(packages) - len(failures), len(packages)))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
