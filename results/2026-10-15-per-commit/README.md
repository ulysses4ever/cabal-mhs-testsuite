# Replay of each commit

MicroHs's package list, replayed with cabal built at each commit of [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41), the same way for every commit: with mhs 0.16.9.0 built from source and nothing installed for it besides `base`, and the inputs of [`replay.py`](../../replay.py), which each summary lists. A package counts when it builds and the small program of its step runs.

The commits were replayed on `master` 538d465eb. Since then they were rebased onto 27789667b, which changed only the CI workflows of the repository, and the first commit gained the regenerated help texts under `doc/`; neither changes the sources that cabal is built from, so the counts hold for the commits as they are in the PR, which the table lists.

| # | Commit | Build and run |
|---|---|---:|
| 1 | [`9306792`](https://github.com/ulysses4ever/cabal/pull/41/commits/9306792541549d66cb6a2ded3c325b6751198e1f) Build, install and register packages with MicroHs | [3/91](1-9306792/summary.md) |
| 2 | [`d2d0da9`](https://github.com/ulysses4ever/cabal/pull/41/commits/d2d0da97477d8afbecf1144de54b2932b981930a) Present the base of mhs at its Hackage versions | [39/91](2-d2d0da9/summary.md) |
| 3 | [`c64d777`](https://github.com/ulysses4ever/cabal/pull/41/commits/c64d7778af36c128636234fd152278fb4ddb494f) Pass the version macros of cabal_macros.h to mhs | [58/91](3-c64d777/summary.md) |
| 4 | [`a097431`](https://github.com/ulysses4ever/cabal/pull/41/commits/a09743143758480f6d28aec939efe220556dc29f) Rewrite packages for mhs as MicroCabal does, before solving | [88/91](4-a097431/summary.md) |
| 5 | [`7bc8204`](https://github.com/ulysses4ever/cabal/pull/41/commits/7bc82042887703aa0b25c6ed9f00d8b3a72aa7a1) Compile the C sources of libraries with mhs | [91/91](5-7bc8204/summary.md) |
| 6 | [`eaf6002`](https://github.com/ulysses4ever/cabal/pull/41/commits/eaf600281531195449b0b463929cbd7cf96deb35) Install libraries for mhs with cabal install --lib | [91/91](6-eaf6002/summary.md) |
