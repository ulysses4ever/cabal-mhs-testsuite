# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392) on `master` c433b3028, the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs. The cabal of each run was built from the same commit on `master` 27e758be0, before commit 1 dropped `GHCJS` from a line of `doc/cabal-package-description-file.rst`; that line and the bootstrap plans that `master` has changed since are all that differ, and no build of cabal reads them.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`cfced1d`](https://github.com/haskell/cabal/pull/11392/commits/cfced1dc001cbf7aa6eb4e923c504527334cedd4) Build, install and register packages with MicroHs | [3/91](1-cfced1d/summary.md) |
| 2 | [`cb3743e`](https://github.com/haskell/cabal/pull/11392/commits/cb3743ea6399fc8c9e16f182434d22b78ef56df5) Present the base of mhs at its Hackage versions | [39/91](2-cb3743e/summary.md) |
| 3 | [`373d4b4`](https://github.com/haskell/cabal/pull/11392/commits/373d4b42ac2a2d0e39f05df1a23c6ab838dcc886) Pass the version macros of cabal_macros.h to mhs | [58/91](3-373d4b4/summary.md) |
| 4 | [`9338e00`](https://github.com/haskell/cabal/pull/11392/commits/9338e00de8d6791b64781000f804f492e06ec3bd) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-9338e00/summary.md) |
| 5 | [`b743e6b`](https://github.com/haskell/cabal/pull/11392/commits/b743e6bb0b3c2192c24b0b1b01750d5e8448658e) Compile the C sources of libraries with mhs | [91/91](5-b743e6b/summary.md) |
| 6 | [`f62e6be`](https://github.com/haskell/cabal/pull/11392/commits/f62e6be7593f3a4c72cf8b774a003e552d876f78) Install libraries for mhs with cabal install --lib | [91/91](6-f62e6be/summary.md) |
