# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392) on `master` aeac769eb, since rebased onto 9cd921b60 and given a CI step that installs MicroHs, with the same Haskell sources, the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`723681e`](https://github.com/haskell/cabal/pull/11392/commits/723681ee89e0cfbc00d3a0cefe23eed826f094ef) Build, install and register packages with MicroHs | [3/91](1-723681e/summary.md) |
| 2 | [`9fdf14c`](https://github.com/haskell/cabal/pull/11392/commits/9fdf14c2e37188f25128b20a11834e87339f46bc) Present the base of mhs at its Hackage versions | [39/91](2-9fdf14c/summary.md) |
| 3 | [`cf44e94`](https://github.com/haskell/cabal/pull/11392/commits/cf44e9421c7b857c5e55dce785e25fa4bd6da252) Pass the version macros of cabal_macros.h to mhs | [58/91](3-cf44e94/summary.md) |
| 4 | [`5a8dc7b`](https://github.com/haskell/cabal/pull/11392/commits/5a8dc7b039e549674e10d622c426e4d408e2f0e1) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-5a8dc7b/summary.md) |
| 5 | [`4c495b5`](https://github.com/haskell/cabal/pull/11392/commits/4c495b55847b57ce66b484bd8b8697892e67c961) Compile the C sources of libraries with mhs | [91/91](5-4c495b5/summary.md) |
| 6 | [`f303670`](https://github.com/haskell/cabal/pull/11392/commits/f3036708eefdd11b1aaace246b35af746a2a20dd) Install libraries for mhs with cabal install --lib | [91/91](6-f303670/summary.md) |
