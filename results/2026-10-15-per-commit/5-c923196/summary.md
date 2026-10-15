## Replay of MicroHs's package list

This run used cabal built at commit 5 of the 6 of [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41), c9231961b, *Compile the C sources of libraries with mhs*, on `master` 538d465eb.

**91 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-15T18:57:23Z` |

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 9 | time | `time zone EST, now 2026-10-15 23:00:48.596063 EST` |
| 30 | splitmix | `splitmix 2080433454648356691` |
| 31 | random | `random 2` |
| 32 | QuickCheck | `+++ OK, passed 100 tests.` |
| 36 | hspec | `1 example, 0 failures` |
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |
| 88 | binary | `binary (1099511627783,"binary") 42` |

