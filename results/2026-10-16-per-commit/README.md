# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392) on `master` aeac769eb, the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`4ed215d`](https://github.com/haskell/cabal/pull/11392/commits/4ed215d2ad96473f1b7312fb6e90800b0f0443e1) Build, install and register packages with MicroHs | [3/91](1-4ed215d/summary.md) |
| 2 | [`8a7f97a`](https://github.com/haskell/cabal/pull/11392/commits/8a7f97a33c60e09755ae5049557bea4da58ad5fc) Present the base of mhs at its Hackage versions | [39/91](2-8a7f97a/summary.md) |
| 3 | [`4df5f2e`](https://github.com/haskell/cabal/pull/11392/commits/4df5f2e304729436a18df8bdd152e906141f16f4) Pass the version macros of cabal_macros.h to mhs | [58/91](3-4df5f2e/summary.md) |
| 4 | [`cc06637`](https://github.com/haskell/cabal/pull/11392/commits/cc066373c4d01b3ebc6247cade0eaba124b6f771) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-cc06637/summary.md) |
| 5 | [`324a208`](https://github.com/haskell/cabal/pull/11392/commits/324a2080ac4ba2eef4afdd27afcda4ad35d7c597) Compile the C sources of libraries with mhs | [91/91](5-324a208/summary.md) |
| 6 | [`91138c9`](https://github.com/haskell/cabal/pull/11392/commits/91138c94a2e89869c9cd02a9eef1e80956b780d0) Install libraries for mhs with cabal install --lib | [91/91](6-91138c9/summary.md) |
