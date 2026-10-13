#!/usr/bin/env python3
"""Summarize a replay: which packages build and run, and why the others do not.

Usage: classify.py --work DIR
Prints Markdown, which is also written to DIR/summary.md.
"""
import argparse
import json
import pathlib
import re
from collections import defaultdict

# The cause of a failure, from the first rule that matches its logs.
RULES = [
    (r"Could not resolve dependencies", "the solver finds no plan"),
    (r"Module not found: (GHC\.[\w.]+|Language\.Haskell\.TH[\w.]*)", "a module of ghc-compat is missing"),
    (r"Module not found: [\w.]+", "a module is missing"),
    (r"#error[^\n]*", "#error"),
    (r"undefined (?:type|value|class|constructor)[^\n]*", "undefined name"),
    (r"Cannot satisfy constraint[^\n]*", "type error"),
    (r"superflous instance binding", "type error"),
    (r"cpphs: [^\n]*", "cpphs"),
    (r"configure: error: [^\n]*", "configure script"),
    (r"uncaught exception: error: [^\n]*", "mhs error"),
    (r"### TIMEOUT", "timeout"),
]


def reason_of(text):
    for pattern, reason in RULES:
        m = re.search(pattern, text)
        if m:
            return reason, m.group(0).strip()
    return "other", ""


def logs_of_step(step_log):
    """The step log, followed by the cabal build logs it refers to."""
    texts = [step_log]
    for path in re.findall(r"Build log \(\s*(\S+?)\s*\):", step_log):
        p = pathlib.Path(path)
        if p.exists():
            texts.append(p.read_text(errors="replace"))
    return "\n".join(reversed(texts))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--work", required=True, type=pathlib.Path)
    work = parser.parse_args().work
    results = json.loads((work / "results.json").read_text())
    packages = sorted(results["packages"].items(), key=lambda kv: kv[1]["index"])
    inputs = results.get("inputs", {})

    failures = []
    by_reason = defaultdict(list)
    for pkg, r in packages:
        if r["status"] == "ok":
            continue
        if r["status"] == "run":
            # It builds, and its executable fails: the end of the output says why.
            reason, evidence, culprit = "the executable fails", r.get("output", ""), pkg
            failures.append((r["index"], pkg, culprit, reason, evidence))
            by_reason[reason].append(pkg)
            continue
        step_log = (work / "logs" / "{:03d}-{}.log".format(r["index"], pkg)).read_text(errors="replace")
        reason, evidence = reason_of(logs_of_step(step_log))
        culprit = r["failed"][0] if r["failed"] else pkg
        failures.append((r["index"], pkg, culprit, reason, evidence))
        by_reason[reason].append(pkg)

    out = ["## Replay of MicroHs's package list", ""]
    out.append("**{} of {} packages build and run.**".format(len(packages) - len(failures), len(packages)))
    out.append("")
    if inputs:
        out.append("| Input | Value |")
        out.append("|---|---|")
        for key in ["cabal", "mhs", "mhs packages", "cc", "MicroHs commit", "index-state", "date"]:
            value = inputs.get(key, "")
            if isinstance(value, list):
                value = ", ".join(value)
            out.append("| {} | `{}` |".format(key, value))
        out.append("")
    if failures:
        out.append("| # | Package | First package that fails | Cause | Evidence |")
        out.append("|---|---|---|---|---|")
        for index, pkg, culprit, reason, evidence in failures:
            out.append("| {} | {} | {} | {} | `{}` |".format(index, pkg, culprit, reason, evidence[:160].replace("|", "\\|")))
        out.append("")
        for reason, pkgs in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
            out.append("* {}: {}".format(reason, ", ".join(pkgs)))
        out.append("")
    smoke = [(r["index"], pkg, r["output"]) for pkg, r in packages if r["status"] == "ok" and r.get("output")]
    if smoke:
        out.append("The executables that call into their package print:")
        out.append("")
        out.append("| # | Package | Last line of output |")
        out.append("|---|---|---|")
        for index, pkg, line in smoke:
            out.append("| {} | {} | `{}` |".format(index, pkg, line[:160].replace("|", "\\|")))
        out.append("")
    text = "\n".join(out)
    (work / "summary.md").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
