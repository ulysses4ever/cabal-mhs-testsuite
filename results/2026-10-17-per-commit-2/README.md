# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392) on `master` aeac769eb, since rebased onto 9cd921b60 with the same sources, the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`efeae1a`](https://github.com/haskell/cabal/pull/11392/commits/efeae1aab1dad77f21e662cfdd8a0d7dbd8508a3) Build, install and register packages with MicroHs | [3/91](1-efeae1a/summary.md) |
| 2 | [`48885db`](https://github.com/haskell/cabal/pull/11392/commits/48885db9da5258e7e3aa20641e3894e9cd565537) Present the base of mhs at its Hackage versions | [39/91](2-48885db/summary.md) |
| 3 | [`1d44372`](https://github.com/haskell/cabal/pull/11392/commits/1d44372653cc5a266b024d4e212376db353dd7b4) Pass the version macros of cabal_macros.h to mhs | [58/91](3-1d44372/summary.md) |
| 4 | [`6eeb10c`](https://github.com/haskell/cabal/pull/11392/commits/6eeb10cb672f540a1945241f190584f1dde9b181) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-6eeb10c/summary.md) |
| 5 | [`215b63c`](https://github.com/haskell/cabal/pull/11392/commits/215b63c8d4b764ddc164fb9cd5ba5dca881951ab) Compile the C sources of libraries with mhs | [91/91](5-215b63c/summary.md) |
| 6 | [`7ea4b19`](https://github.com/haskell/cabal/pull/11392/commits/7ea4b1949fd3b330ead3e1803eebed08b1b935e1) Install libraries for mhs with cabal install --lib | [91/91](6-7ea4b19/summary.md) |
