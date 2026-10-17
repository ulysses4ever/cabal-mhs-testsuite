# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392) on `master` aeac769eb, the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`7847f3d`](https://github.com/haskell/cabal/pull/11392/commits/7847f3dd1c3097673b8265ca8112b51cc414c3aa) Build, install and register packages with MicroHs | [3/91](1-7847f3d/summary.md) |
| 2 | [`2b2f1e7`](https://github.com/haskell/cabal/pull/11392/commits/2b2f1e729364457b34728b81d7592be6d2bed02b) Present the base of mhs at its Hackage versions | [39/91](2-2b2f1e7/summary.md) |
| 3 | [`48f2e33`](https://github.com/haskell/cabal/pull/11392/commits/48f2e338b9c4f7b4b322a9497f1416838745cda5) Pass the version macros of cabal_macros.h to mhs | [58/91](3-48f2e33/summary.md) |
| 4 | [`d918f31`](https://github.com/haskell/cabal/pull/11392/commits/d918f3181d80183a275811ceafcfaf7fc9c21c41) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-d918f31/summary.md) |
| 5 | [`9ba7762`](https://github.com/haskell/cabal/pull/11392/commits/9ba77627e64d95e67ad18fa10939c662df078992) Compile the C sources of libraries with mhs | [91/91](5-9ba7762/summary.md) |
| 6 | [`44f201e`](https://github.com/haskell/cabal/pull/11392/commits/44f201e4af9ff274ecfd5f16421ae445dde6158a) Install libraries for mhs with cabal install --lib | [91/91](6-44f201e/summary.md) |
