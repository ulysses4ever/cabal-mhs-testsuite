# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392) on `master` aeac769eb, the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`7847f3d`](https://github.com/haskell/cabal/pull/11392/commits/7847f3dd1c3097673b8265ca8112b51cc414c3aa) Build, install and register packages with MicroHs | [3/91](1-7847f3d/summary.md) |
| 2 | [`1dc1c07`](https://github.com/haskell/cabal/pull/11392/commits/1dc1c075474a5b5d7027109aa81838f082e400de) Present the base of mhs at its Hackage versions | [39/91](2-1dc1c07/summary.md) |
| 3 | [`0cf76ad`](https://github.com/haskell/cabal/pull/11392/commits/0cf76ad68738e59ded62d34e63ec7d4d2a4019af) Pass the version macros of cabal_macros.h to mhs | [58/91](3-0cf76ad/summary.md) |
| 4 | [`3dd4140`](https://github.com/haskell/cabal/pull/11392/commits/3dd414027230f338466c7708ae20d58742e88a07) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-3dd4140/summary.md) |
| 5 | [`0aae2e5`](https://github.com/haskell/cabal/pull/11392/commits/0aae2e5095741bf8718cf26ca65d476cb7276e7a) Compile the C sources of libraries with mhs | [91/91](5-0aae2e5/summary.md) |
| 6 | [`7dd5b19`](https://github.com/haskell/cabal/pull/11392/commits/7dd5b19674b3606cdf662fb292229bfe05d3f7c2) Install libraries for mhs with cabal install --lib | [91/91](6-7dd5b19/summary.md) |
