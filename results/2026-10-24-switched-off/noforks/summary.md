## Replay of MicroHs's package list

This run used cabal built at the head of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), f62e6be75, with [`switches.patch`](../switches.patch) and `MHS_ABLATE=noforks`: array and random kept, rather than replaced with array-mhs and random-mhs (`forkedPackages`).

**71 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-24T21:54:37Z` |

| # | Package | First package that fails | Cause | Evidence |
|---|---|---|---|---|
| 4 | array | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 8 | containers | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 31 | random | random-1 | undefined name | `undefined value: ByteArray` |
| 32 | QuickCheck | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 33 | quickcheck-io | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 34 | hspec-core | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 36 | hspec | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 40 | tagsoup | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 46 | fgl | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 49 | edit-distance | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 52 | vault | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 61 | indexed-traversable | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 62 | parallel | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 64 | Diff | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 69 | comonad | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 71 | data-default | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 72 | data-default-class | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 74 | bimap | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 88 | binary | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 90 | these | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |

* a module of ghc-compat is missing: array, containers, QuickCheck, quickcheck-io, hspec-core, hspec, tagsoup, fgl, edit-distance, vault, indexed-traversable, parallel, Diff, comonad, data-default, data-default-class, bimap, binary, these
* undefined name: random

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 9 | time | `time zone EST, now 2026-10-25 01:56:55.138297 EST` |
| 30 | splitmix | `splitmix 4239699801111023619` |
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |

