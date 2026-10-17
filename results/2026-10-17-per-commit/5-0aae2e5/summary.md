## Replay of MicroHs's package list

This run used cabal built at commit 5 of the 6 of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), 0aae2e509, *Compile the C sources of libraries with mhs*, on `master` aeac769eb.

**91 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-17T00:52:47Z` |

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 9 | time | `time zone EST, now 2026-10-17 04:56:11.674196 EST` |
| 30 | splitmix | `splitmix 13204658367577913699` |
| 31 | random | `random 2` |
| 32 | QuickCheck | `+++ OK, passed 100 tests.` |
| 36 | hspec | `1 example, 0 failures` |
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |
| 88 | binary | `binary (1099511627783,"binary") 42` |

