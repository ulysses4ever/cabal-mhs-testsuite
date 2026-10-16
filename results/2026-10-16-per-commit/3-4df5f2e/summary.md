## Replay of MicroHs's package list

This run used cabal built at commit 3 of the 6 of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), 4df5f2e30, *Pass the version macros of cabal_macros.h to mhs*, on `master` aeac769eb.

**58 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-16T23:25:26Z` |

| # | Package | First package that fails | Cause | Evidence |
|---|---|---|---|---|
| 4 | array | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 5 | unordered-containers | unordered-containers-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 6 | async | unordered-containers-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 7 | call-stack | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 8 | containers | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 9 | time | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 11 | cpphs | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 14 | exceptions | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 15 | os-string | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 16 | filepath | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 19 | HUnit | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 20 | hspec-expectations | call-stack-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 30 | splitmix | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 31 | random | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 32 | QuickCheck | array-0 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 33 | quickcheck-io | array-0 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 34 | hspec-core | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 35 | hspec-discover | exceptions-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 36 | hspec | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 40 | tagsoup | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 46 | fgl | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 49 | edit-distance | array-0 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 52 | vault | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 61 | indexed-traversable | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 62 | parallel | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 64 | Diff | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 69 | comonad | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 71 | data-default | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 72 | data-default-class | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 74 | bimap | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Stack` |
| 81 | dlist | dlist-1 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 88 | binary | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 90 | these | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |

* a module of ghc-compat is missing: array, unordered-containers, async, call-stack, containers, time, cpphs, exceptions, os-string, filepath, HUnit, hspec-expectations, splitmix, random, QuickCheck, quickcheck-io, hspec-core, hspec-discover, hspec, tagsoup, fgl, edit-distance, vault, indexed-traversable, parallel, Diff, comonad, data-default, data-default-class, bimap, dlist, binary, these

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |

