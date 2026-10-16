## Replay of MicroHs's package list

This run used cabal built at commit 2 of the 6 of [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41), *Present the base of mhs at its Hackage versions*, at 85bcb8dc4 on `master` 538d465eb. Rebased onto 27789667b, which changes only CI workflows, and with the help texts under `doc/` regenerated in the first commit, the commit is d2d0da974; cabal is built from the same sources.

**39 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-15T19:02:58Z` |

| # | Package | First package that fails | Cause | Evidence |
|---|---|---|---|---|
| 4 | array | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 5 | unordered-containers | unordered-containers-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 6 | async | unordered-containers-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 7 | call-stack | call-stack-0 | undefined name | `undefined type: HasCallStack` |
| 8 | containers | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 9 | time | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 10 | polyparse | polyparse-1 | type error | `superflous instance binding` |
| 11 | cpphs | polyparse-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 12 | transformers | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 13 | mtl | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 14 | exceptions | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 15 | os-string | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 16 | filepath | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 20 | hspec-expectations | hspec-expectations-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 22 | nanospec | nanospec-0 | type error | `Cannot satisfy constraint: Semigroup Summary` |
| 23 | parsec | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 25 | prettyprinter | prettyprinter-1 | #error | `#error "MIN_VERSION_base macro not defined!"` |
| 26 | prettyprinter-ansi-terminal | prettyprinter-1 | #error | `#error "MIN_VERSION_base macro not defined!"` |
| 27 | prettyprinter-compat-annotated-wl-pprint | prettyprinter-1 | #error | `#error "MIN_VERSION_base macro not defined!"` |
| 28 | prettyprinter-compat-ansi-wl-pprint | prettyprinter-1 | #error | `#error "MIN_VERSION_base macro not defined!"` |
| 29 | prettyprinter-compat-wl-pprint | prettyprinter-1 | #error | `#error "MIN_VERSION_base macro not defined!"` |
| 30 | splitmix | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 31 | random | time-1 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 32 | QuickCheck | array-0 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 33 | quickcheck-io | array-0 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 34 | hspec-core | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 35 | hspec-discover | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 36 | hspec | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 40 | tagsoup | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 41 | optparse-applicative | prettyprinter-1 | #error | `#error "MIN_VERSION_base macro not defined!"` |
| 45 | fingertree | fingertree-0 | type error | `Cannot satisfy constraint: Semigroup (FingerTree v a)` |
| 46 | fgl | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 49 | edit-distance | array-0 | a module of ghc-compat is missing | `Module not found: Language.Haskell.TH.Syntax` |
| 50 | StateVar | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 51 | unliftio-core | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 52 | vault | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 56 | transformers-compat | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 57 | mmorph | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 61 | indexed-traversable | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 62 | parallel | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 64 | Diff | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 67 | contravariant | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 68 | distributive | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 69 | comonad | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 71 | data-default | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 72 | data-default-class | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 74 | bimap | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 81 | dlist | dlist-1 | a module of ghc-compat is missing | `Module not found: GHC.Exts` |
| 86 | transformers-base | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 87 | tardis | transformers-0 | type error | `Cannot satisfy constraint: Semigroup (Constant a b)` |
| 88 | binary | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |
| 90 | these | array-0 | a module of ghc-compat is missing | `Module not found: GHC.Arr` |

* a module of ghc-compat is missing: array, unordered-containers, async, containers, time, cpphs, hspec-expectations, splitmix, random, QuickCheck, quickcheck-io, hspec-core, hspec, tagsoup, fgl, edit-distance, vault, indexed-traversable, parallel, Diff, comonad, data-default, data-default-class, bimap, dlist, binary, these
* type error: polyparse, transformers, mtl, exceptions, os-string, filepath, nanospec, parsec, hspec-discover, fingertree, StateVar, unliftio-core, transformers-compat, mmorph, contravariant, distributive, transformers-base, tardis
* #error: prettyprinter, prettyprinter-ansi-terminal, prettyprinter-compat-annotated-wl-pprint, prettyprinter-compat-ansi-wl-pprint, prettyprinter-compat-wl-pprint, optparse-applicative
* undefined name: call-stack

The executables that call into their package print:

| # | Package | Last line of output |
|---|---|---|
| 73 | terminfo | `terminfo columns Just 80, cursor addressing False` |

