## Replay of MicroHs's package list

This run used an installation of mhs whose `base` and compiler cabal built from MicroHs v0.16.9.0, with [`microhs-cabal-fixes.patch`](../../microhs-cabal-fixes.patch) applied; see [Building MicroHs with cabal](../../README.md#building-microhs-with-cabal).

**91 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.17.0.0 of the Cabal library (in-tree)` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-13T15:36:56Z` |

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 9 | time | `time zone EST, now 2026-10-13 19:40:10.357629 EST` |
| 30 | splitmix | `splitmix 10094965696192921949` |
| 31 | random | `random 5` |
| 32 | QuickCheck | `+++ OK, passed 100 tests.` |
| 36 | hspec | `1 example, 0 failures` |
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |
| 88 | binary | `binary (1099511627783,"binary") 42` |

