## Replay of MicroHs's package list

This run used cabal built from the commits of haskell/cabal#11392 rebased on `master` 59f735663, as in [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41) at 5214c89d8, which rewrites packages for mhs before solving only, rather than the patches of this repository.

**91 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-14T22:45:50Z` |

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 9 | time | `time zone EST, now 2026-10-15 02:48:49.834008 EST` |
| 30 | splitmix | `splitmix 4798408984149415219` |
| 31 | random | `random 1` |
| 32 | QuickCheck | `+++ OK, passed 100 tests.` |
| 36 | hspec | `1 example, 0 failures` |
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |
| 88 | binary | `binary (1099511627783,"binary") 42` |

