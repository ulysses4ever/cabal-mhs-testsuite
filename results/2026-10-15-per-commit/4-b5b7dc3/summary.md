## Replay of MicroHs's package list

This run used cabal built at commit 4 of the 6 of [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41), b5b7dc3e4, *Rewrite packages for mhs as MicroCabal does, before solving*, on `master` 538d465eb.

**88 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-15T18:58:54Z` |

| # | Package | First package that fails | Cause | Evidence |
|---|---|---|---|---|
| 9 | time | exe:corpus | mhs error | `uncaught exception: error: command failed: cc -w -Wall -O3  -I/tmp/claude-mhs/mcabal-clean/bin/../mhs-0.16.9.0/packages/mhs-0.16.9.0/data/src/runtime -I/tmp/cla` |
| 88 | binary | exe:corpus | mhs error | `uncaught exception: error: command failed: cc -w -Wall -O3  -I/tmp/claude-mhs/mcabal-clean/bin/../mhs-0.16.9.0/packages/mhs-0.16.9.0/data/src/runtime -I/tmp/cla` |
| 90 | these | binary-0 | a module is missing | `Module not found: Data.ByteString.Builder.Prim` |

* mhs error: time, binary
* a module is missing: these

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 30 | splitmix | `splitmix 14252819447625030081` |
| 31 | random | `random 4` |
| 32 | QuickCheck | `+++ OK, passed 100 tests.` |
| 36 | hspec | `1 example, 0 failures` |
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |

