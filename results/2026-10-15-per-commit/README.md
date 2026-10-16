# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41) on `master` 538d465eb, the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`3e9a787`](https://github.com/ulysses4ever/cabal/pull/41/commits/3e9a787cd9bcace28e485ffe70416c95459c85bc) Build, install and register packages with MicroHs | [3/91](1-3e9a787/summary.md) |
| 2 | [`85bcb8d`](https://github.com/ulysses4ever/cabal/pull/41/commits/85bcb8dc45e22ae2f924a36c3bbe77d68e0ffb72) Present the base of mhs at its Hackage versions | [39/91](2-85bcb8d/summary.md) |
| 3 | [`7c5fe93`](https://github.com/ulysses4ever/cabal/pull/41/commits/7c5fe93d9ae5cf76b24e0b7c6f90090b81c0ec47) Pass the version macros of cabal_macros.h to mhs | [58/91](3-7c5fe93/summary.md) |
| 4 | [`b5b7dc3`](https://github.com/ulysses4ever/cabal/pull/41/commits/b5b7dc3e4f91f2817e4485efaa97e441097d7c29) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-b5b7dc3/summary.md) |
| 5 | [`c923196`](https://github.com/ulysses4ever/cabal/pull/41/commits/c9231961bd78c946ca9164494b29c6ca3006cd0d) Compile the C sources of libraries with mhs | [91/91](5-c923196/summary.md) |
| 6 | [`351abd9`](https://github.com/ulysses4ever/cabal/pull/41/commits/351abd99ef92248a6b6479fd209510a692fc564b) Install libraries for mhs with cabal install --lib | [91/91](6-351abd9/summary.md) |
