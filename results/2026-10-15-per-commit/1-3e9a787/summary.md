## Replay of MicroHs's package list

This run used cabal built at commit 1 of the 6 of [ulysses4ever/cabal#41](https://github.com/ulysses4ever/cabal/pull/41), 3e9a787cd, *Build, install and register packages with MicroHs*, on `master` 538d465eb.

**3 of 91 packages build and run.**

| Input | Value |
|---|---|
| cabal | `compiled using version 3.19.0.0 of the Cabal library` |
| mhs | `0.16.9.0` |
| mhs packages | `base-0.16.9.0` |
| cc | `gcc (GCC) 15.3.0` |
| MicroHs commit | `23525f5bf600cd8c80df2cf611ce3d30c84eac41` |
| index-state | `2026-07-16T00:00:00Z` |
| date | `2026-10-15T19:05:02Z` |

| # | Package | First package that fails | Cause | Evidence |
|---|---|---|---|---|
| 0 | ghc-compat | ghc-compat | the solver finds no plan | `Could not resolve dependencies` |
| 1 | colour | colour-2 | type error | `Cannot satisfy constraint: Semigroup (Colour a)` |
| 2 | ansi-terminal-types | ansi-terminal-types | the solver finds no plan | `Could not resolve dependencies` |
| 3 | ansi-terminal | unix-2 | other | `` |
| 4 | array | syb-0 | mhs error | `uncaught exception: error: "./Data/Generics/Instances.hs": line 88, col 1:` |
| 5 | unordered-containers | unordered-containers | the solver finds no plan | `Could not resolve dependencies` |
| 6 | async | async | the solver finds no plan | `Could not resolve dependencies` |
| 7 | call-stack | call-stack | the solver finds no plan | `Could not resolve dependencies` |
| 8 | containers | syb-0 | mhs error | `uncaught exception: error: "./Data/Generics/Instances.hs": line 88, col 1:` |
| 9 | time | time | the solver finds no plan | `Could not resolve dependencies` |
| 10 | polyparse | polyparse-1 | type error | `superflous instance binding` |
| 11 | cpphs | syb-0 | mhs error | `uncaught exception: error: "./Data/Generics/Instances.hs": line 88, col 1:` |
| 12 | transformers | transformers-0 | type error | `Cannot satisfy constraint: Applicative Identity` |
| 13 | mtl | mtl-1 | a module is missing | `Module not found: Control.Monad.Instances` |
| 14 | exceptions | exceptions | the solver finds no plan | `Could not resolve dependencies` |
| 17 | granite | granite | the solver finds no plan | `Could not resolve dependencies` |
| 19 | HUnit | HUnit-1 | mhs error | `uncaught exception: error: "./Test/HUnit/Lang.lhs": line 13, col 46: not exported: try` |
| 20 | hspec-expectations | HUnit-1 | mhs error | `uncaught exception: error: "./Test/HUnit/Lang.lhs": line 13, col 46: not exported: try` |
| 21 | monad-loops | syb-0 | mhs error | `uncaught exception: error: "./Data/Generics/Instances.hs": line 88, col 1:` |
| 22 | nanospec | nanospec | the solver finds no plan | `Could not resolve dependencies` |
| 23 | parsec | mtl-1 | a module is missing | `Module not found: Control.Monad.Instances` |
| 24 | pretty | pretty | the solver finds no plan | `Could not resolve dependencies` |
| 25 | prettyprinter | prettyprinter | the solver finds no plan | `Could not resolve dependencies` |
| 26 | prettyprinter-ansi-terminal | prettyprinter-ansi-terminal | the solver finds no plan | `Could not resolve dependencies` |
| 27 | prettyprinter-compat-annotated-wl-pprint | prettyprinter-compat-annotated-wl-pprint | the solver finds no plan | `Could not resolve dependencies` |
| 28 | prettyprinter-compat-ansi-wl-pprint | prettyprinter-compat-ansi-wl-pprint | the solver finds no plan | `Could not resolve dependencies` |
| 29 | prettyprinter-compat-wl-pprint | prettyprinter-compat-wl-pprint | the solver finds no plan | `Could not resolve dependencies` |
| 30 | splitmix | splitmix | the solver finds no plan | `Could not resolve dependencies` |
| 31 | random | old-time-1 | #error | `#error "Don't know how to get at timezone name on your OS."` |
| 32 | QuickCheck | QuickCheck | the solver finds no plan | `Could not resolve dependencies` |
| 33 | quickcheck-io | quickcheck-io | the solver finds no plan | `Could not resolve dependencies` |
| 34 | hspec-core | hspec-core | the solver finds no plan | `Could not resolve dependencies` |
| 35 | hspec-discover | hspec-discover | the solver finds no plan | `Could not resolve dependencies` |
| 36 | hspec | hspec | the solver finds no plan | `Could not resolve dependencies` |
| 37 | simple-affine-space | simple-affine-space | the solver finds no plan | `Could not resolve dependencies` |
| 38 | split | split | the solver finds no plan | `Could not resolve dependencies` |
| 39 | tagged | tagged | the solver finds no plan | `Could not resolve dependencies` |
| 40 | tagsoup | tagsoup | the solver finds no plan | `Could not resolve dependencies` |
| 41 | optparse-applicative | optparse-applicative | the solver finds no plan | `Could not resolve dependencies` |
| 42 | semigroups | semigroups | the solver finds no plan | `Could not resolve dependencies` |
| 43 | xhtml | xhtml | the solver finds no plan | `Could not resolve dependencies` |
| 44 | heaps | heaps | the solver finds no plan | `Could not resolve dependencies` |
| 45 | fingertree | fingertree | the solver finds no plan | `Could not resolve dependencies` |
| 46 | fgl | fgl | the solver finds no plan | `Could not resolve dependencies` |
| 47 | psqueues | psqueues | the solver finds no plan | `Could not resolve dependencies` |
| 48 | PSQueue | PSQueue | the solver finds no plan | `Could not resolve dependencies` |
| 49 | edit-distance | edit-distance | the solver finds no plan | `Could not resolve dependencies` |
| 50 | StateVar | StateVar | the solver finds no plan | `Could not resolve dependencies` |
| 51 | unliftio-core | unliftio-core | the solver finds no plan | `Could not resolve dependencies` |
| 52 | vault | vault | the solver finds no plan | `Could not resolve dependencies` |
| 53 | js-dgtable | js-dgtable | the solver finds no plan | `Could not resolve dependencies` |
| 54 | js-flot | js-flot | the solver finds no plan | `Could not resolve dependencies` |
| 55 | js-jquery | js-jquery | the solver finds no plan | `Could not resolve dependencies` |
| 56 | transformers-compat | transformers-compat | the solver finds no plan | `Could not resolve dependencies` |
| 57 | mmorph | mmorph | the solver finds no plan | `Could not resolve dependencies` |
| 58 | base-orphans | base-orphans | the solver finds no plan | `Could not resolve dependencies` |
| 59 | foldable1-classes-compat | foldable1-classes-compat | the solver finds no plan | `Could not resolve dependencies` |
| 60 | bifunctor-classes-compat | bifunctor-classes-compat | the solver finds no plan | `Could not resolve dependencies` |
| 61 | indexed-traversable | indexed-traversable | the solver finds no plan | `Could not resolve dependencies` |
| 62 | parallel | parallel | the solver finds no plan | `Could not resolve dependencies` |
| 63 | newtype | newtype | the solver finds no plan | `Could not resolve dependencies` |
| 64 | Diff | Diff | the solver finds no plan | `Could not resolve dependencies` |
| 65 | void | void | the solver finds no plan | `Could not resolve dependencies` |
| 66 | character-ps | character-ps | the solver finds no plan | `Could not resolve dependencies` |
| 67 | contravariant | contravariant | the solver finds no plan | `Could not resolve dependencies` |
| 68 | distributive | distributive | the solver finds no plan | `Could not resolve dependencies` |
| 69 | comonad | comonad | the solver finds no plan | `Could not resolve dependencies` |
| 70 | parser-combinators | parser-combinators | the solver finds no plan | `Could not resolve dependencies` |
| 71 | data-default | data-default | the solver finds no plan | `Could not resolve dependencies` |
| 72 | data-default-class | data-default-class | the solver finds no plan | `Could not resolve dependencies` |
| 73 | terminfo | terminfo | the solver finds no plan | `Could not resolve dependencies` |
| 74 | bimap | bimap | the solver finds no plan | `Could not resolve dependencies` |
| 75 | byteable | byteable | the solver finds no plan | `Could not resolve dependencies` |
| 76 | bytestring-builder | bytestring-builder | the solver finds no plan | `Could not resolve dependencies` |
| 77 | casing | casing | the solver finds no plan | `Could not resolve dependencies` |
| 78 | composition | composition | the solver finds no plan | `Could not resolve dependencies` |
| 79 | cpu | cpu | the solver finds no plan | `Could not resolve dependencies` |
| 80 | data-ordlist | data-ordlist | the solver finds no plan | `Could not resolve dependencies` |
| 81 | dlist | dlist | the solver finds no plan | `Could not resolve dependencies` |
| 82 | time-units | time-units | the solver finds no plan | `Could not resolve dependencies` |
| 83 | xml | xml | the solver finds no plan | `Could not resolve dependencies` |
| 84 | numbers | numbers | the solver finds no plan | `Could not resolve dependencies` |
| 85 | timeit | timeit | the solver finds no plan | `Could not resolve dependencies` |
| 86 | transformers-base | transformers-base | the solver finds no plan | `Could not resolve dependencies` |
| 87 | tardis | tardis | the solver finds no plan | `Could not resolve dependencies` |
| 88 | binary | binary | the solver finds no plan | `Could not resolve dependencies` |
| 89 | assoc | assoc | the solver finds no plan | `Could not resolve dependencies` |
| 90 | these | these | the solver finds no plan | `Could not resolve dependencies` |

* the solver finds no plan: ghc-compat, ansi-terminal-types, unordered-containers, async, call-stack, time, exceptions, granite, nanospec, pretty, prettyprinter, prettyprinter-ansi-terminal, prettyprinter-compat-annotated-wl-pprint, prettyprinter-compat-ansi-wl-pprint, prettyprinter-compat-wl-pprint, splitmix, QuickCheck, quickcheck-io, hspec-core, hspec-discover, hspec, simple-affine-space, split, tagged, tagsoup, optparse-applicative, semigroups, xhtml, heaps, fingertree, fgl, psqueues, PSQueue, edit-distance, StateVar, unliftio-core, vault, js-dgtable, js-flot, js-jquery, transformers-compat, mmorph, base-orphans, foldable1-classes-compat, bifunctor-classes-compat, indexed-traversable, parallel, newtype, Diff, void, character-ps, contravariant, distributive, comonad, parser-combinators, data-default, data-default-class, terminfo, bimap, byteable, bytestring-builder, casing, composition, cpu, data-ordlist, dlist, time-units, xml, numbers, timeit, transformers-base, tardis, binary, assoc, these
* mhs error: array, containers, cpphs, HUnit, hspec-expectations, monad-loops
* type error: colour, polyparse, transformers
* a module is missing: mtl, parsec
* other: ansi-terminal
* #error: random

