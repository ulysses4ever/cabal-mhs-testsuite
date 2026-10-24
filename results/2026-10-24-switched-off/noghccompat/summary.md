## Replay of MicroHs's package list

This run used cabal built at the head of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), f62e6be75, with [`switches.patch`](../switches.patch) and `MHS_ABLATE=noghccompat`: no ghc-compat added to the components.

**67 of 91 packages build and run.**

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
| 5 | unordered-containers | unordered-containers-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 6 | async | unordered-containers-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 7 | call-stack | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 9 | time | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 11 | cpphs | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 14 | exceptions | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 15 | os-string | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 16 | filepath | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 19 | HUnit | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 20 | hspec-expectations | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 30 | splitmix | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 31 | random | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 32 | QuickCheck | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 33 | quickcheck-io | call-stack-0 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 34 | hspec-core | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 35 | hspec-discover | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 36 | hspec | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 40 | tagsoup | tagsoup-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 49 | edit-distance | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 52 | vault | unordered-containers-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 74 | bimap | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 81 | dlist | dlist-1 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 88 | binary | binary-0 | a module of ghc-compat is missing | `Module not found: GHC.Fingerprint` |
| 90 | these | binary-0 | a module is missing | `Module not found: Data.ByteString.Builder.Prim` |

* a module of ghc-compat is missing: unordered-containers, async, call-stack, time, cpphs, exceptions, os-string, filepath, HUnit, hspec-expectations, splitmix, random, QuickCheck, quickcheck-io, hspec-core, hspec-discover, hspec, tagsoup, edit-distance, vault, bimap, dlist, binary
* a module is missing: these

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |

