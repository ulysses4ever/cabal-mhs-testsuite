# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41), the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

The commits were replayed on `master` 538d465eb. Rebasing them onto 27789667b changed only the CI workflows of the repository, not the sources that cabal is built from, so the counts hold for the commits as they are in the PR, which the table lists.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`8908750`](https://github.com/ulysses4ever/cabal/pull/41/commits/89087500a2301fe22b96dac8c7278b6976bfd313) Build, install and register packages with MicroHs | [3/91](1-8908750/summary.md) |
| 2 | [`44ad1d3`](https://github.com/ulysses4ever/cabal/pull/41/commits/44ad1d31cc5506fb5a40ce7becab022d627c4e3f) Present the base of mhs at its Hackage versions | [39/91](2-44ad1d3/summary.md) |
| 3 | [`7e91066`](https://github.com/ulysses4ever/cabal/pull/41/commits/7e9106653f91387ad6445c4e6ad00f07d69d4e2e) Pass the version macros of cabal_macros.h to mhs | [58/91](3-7e91066/summary.md) |
| 4 | [`e9b6438`](https://github.com/ulysses4ever/cabal/pull/41/commits/e9b64386f85d74e1819a02b3cb732a0becf16d45) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-e9b6438/summary.md) |
| 5 | [`c16a8c5`](https://github.com/ulysses4ever/cabal/pull/41/commits/c16a8c536ba3c5794f9dc6ea3d899df208d3bde9) Compile the C sources of libraries with mhs | [91/91](5-c16a8c5/summary.md) |
| 6 | [`b9bb698`](https://github.com/ulysses4ever/cabal/pull/41/commits/b9bb69886cc49d1ace8065d20b893ab0ef369464) Install libraries for mhs with cabal install --lib | [91/91](6-b9bb698/summary.md) |
