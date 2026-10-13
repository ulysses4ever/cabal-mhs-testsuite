# cabal-mhs-testsuite

[![replay](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/workflows/ci.yml/badge.svg)](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/workflows/ci.yml)

This tests the support for [MicroHs](https://github.com/augustss/MicroHs) (`mhs`) in cabal, [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), on the packages that MicroHs itself is tested with.

## What it does

MicroHs's [`Makefile.packages`](https://github.com/augustss/MicroHs/blob/master/Makefile.packages) lists the Hackage packages that its `hackage-ci` workflow installs, on every push, with `mcabal`, the package manager of MicroHs. `replay.py` builds the same packages with cabal driving mhs, one at a time and in the same order: for each package, it builds a tiny executable that depends on it, into a store shared by all the steps, and runs it. A package counts when both succeed. MicroHs's CI only installs the packages.

mhs compiles the C sources of the libraries a program uses when it links the program, so even an executable that does nothing compiles the C sources of the package and of its dependencies. For the packages whose C code a program can call (`time`, `terminfo`, `binary`), for those that seed random numbers from the clock (`splitmix`, `random`), and for the test frameworks `QuickCheck` and `hspec`, which use much of the list, the executable calls into the package (`SMOKE` in `replay.py`).

Where mcabal behaves differently from cabal, the replay does what mcabal does:

* The `--git` overrides of the Makefile become `source-repository-package` stanzas, kept in the projects of the later steps once the package builds.
* mcabal ignores version bounds. [`project.extra`](project.extra), which is added to the project of every step, lifts the few bounds that stand between a package of the list and the versions of its dependencies that support mhs, and says why for each.
* mhs sees every package that mcabal has installed, and `hspec-core` relies on that: it imports `async` without depending on it, as it compiles its vendored copy of `async` only for GHC. The replay adds `if impl(mhs)` / `build-depends: async` to a copy of `hspec-core` (`PATCHED` in `replay.py`), which is the fix that belongs upstream.
* mcabal adds `ghc-compat` to the dependencies of every package, and uses the forks `array-mhs` and `random-mhs` wherever a package depends on `array` or `random`. With the PR, cabal rewrites the packages the same way before solving, so it builds `ghc-compat` and the forks from Hackage like any other dependency, and mhs needs nothing installed besides what `make minstall` installs.

The packages come from Hackage as it was at the `index-state` set in `replay.py`, so that every run chooses the same versions.

## The cabal under test

[`patches/`](patches) holds the commits that make the PR work, on top of its head, [`1f2da2d`](https://github.com/haskell/cabal/commit/1f2da2dce875050e1ea9bc0b37972732094125d9), until they are pushed to the PR. CI checks out haskell/cabal at that commit and applies them. A run started by hand can build another repository and commit of cabal, with or without the patches, and another tag of MicroHs.

CI also runs the tests of the PR in `cabal-testsuite/PackageTests/MHS`.

## Results

The summary page of every CI run lists which packages build and run, with the inputs of the run, why each of the others fails, and what the executables that call into their package print; the logs of all the steps are attached to it.

All the counts are for compiling each package as it is published, with no settings of its own: the project file of a step sets no flags and no compiler options for any package of the list. What it does set chooses versions and sources, as described above: the `index-state`, the git repositories that MicroHs's Makefile builds some packages from, the three bounds that `project.extra` lifts and its one constraint, and the copy of `hspec-core` with its missing dependency added. The tiny executable of each step, which is not one of the packages, is linked with `--no-as-needed` on Linux.

While the patches were written, the replay of the 91 packages measured each step (on MicroHs's list at its master of 2026-10-10, before the bounds of `project.extra`):

| cabal | Packages that build |
|---|---|
| patches 1 and 2: building with mhs, `base` and its bundled packages at their Hackage versions | 39 |
| patch 3: every extension and `reexported-modules` accepted | 42 |
| patch 4: the version macros of `cabal_macros.h` | 62 |
| patch 5: what is specific to mhs kept in `Distribution.Simple.MHS`, and `ghc-compat` installed with mcabal (an earlier version of patch 7) | 80 |
| patch 6, `hashable` at 1.4.7.0, and `project.extra`, on MicroHs's list at v0.16.9.0 with a pinned index ([CI run](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/runs/38328073444)) | 89: `hspec-core` and `hspec` fail on the undeclared `async` |
| the forks of `array` and `random` installed with mcabal, and the fix of `hspec-core` ([CI run](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/runs/38333639295), [local run](results/2026-10-13-local/summary.md)) | 91 |
| patch 7: packages rewritten for mhs before solving, so that `ghc-compat` and the forks come from Hackage and mhs needs nothing installed ([CI run](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/runs/38363564839), [local run](results/2026-10-13-local-base-only/summary.md)) | 91 |
| patch 8: the C sources of libraries; from here on, every executable is also run, and seven of them call into their package ([CI run](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/runs/38396355580), with GCC 13; [local run](results/2026-10-13-local-csources/summary.md), with GCC 15) | 91 build and run |
| patch 9: `cabal install --lib` installs libraries for plain mhs, which CI tests with `MHS/InstallLib` ([CI run](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/runs/38403646037)) | 91 build and run |

## Building MicroHs with cabal

MicroHs builds its `base` with `mcabal build` in `lib`, and compiles mhs with mhs directly. cabal builds both with mhs, once [`microhs-cabal-fixes.patch`](microhs-cabal-fixes.patch) fixes four problems of their cabal files that mcabal does not mind, items 11 to 14 of the [inventory](INVENTORY.md):

```
git -C MicroHs apply "$PWD/cabal-mhs-testsuite/microhs-cabal-fixes.patch"
cd MicroHs/lib
printf 'packages: .\ncompiler: mhs\nwith-compiler: mhs\nallow-boot-library-installs: True\n' > cabal.project
cabal build                    # base-0.16.9.0.pkg
cd ..
printf 'packages: .\ncompiler: mhs\nwith-compiler: mhs\n' > cabal.project
cabal build exe:mhs            # the compiler
```

cabal is no slower than the usual way. Measured once each, with the same mhs, from clean trees:

| Build | Usual way | Time | cabal | Time |
|---|---|---|---|---|
| `base` | `mcabal build` in `lib` | 68 s | `cabal build` in `lib` | 69 s |
| the compiler | the Makefile's `mhs -z -i -imhs -isrc -ilib MicroHs.Main` | 68 s | `cabal build exe:mhs` | 39 s |

The Makefile's command compiles the sources of `base` again, with `-ilib`, while cabal compiles the compiler against the installed `base`, as mhs run directly would, in 38 s.

What they build:

| Output | Usual way | Size | cabal | Size |
|---|---|---|---|---|
| `base-0.16.9.0.pkg` | `mcabal build` | 830,417 bytes | `cabal build` | 830,285 bytes |
| `mhs` | the Makefile, which passes `-z` | 526,864 bytes | `cabal build exe:mhs` | 1,104,400 bytes |
| `mhs` | | | `cabal build exe:mhs --mhs-options=-z` | 526,864 bytes |

mhs always compresses package files, so the two `base` packages are the same size but for 132 bytes, and `mhs -v -v -L` prints the same modules, exports and definitions for both. For programs, compression is the option `-z`, which the Makefile passes for `mhs` and mcabal passes for every executable, and which cabal passes only when asked: with `--mhs-options=-z`, or with `mhs-options: -z` under `package MicroHs` in `cabal.project`. Given it, cabal builds an `mhs` of exactly the Makefile's size, in 34 s. Their machine code and data are identical, and their combinator code differs only in how 52 source locations of `base` are spelled, such as `lib/Text/Printf.hs` against `./Text/Printf.hs`, since the Makefile compiles the sources of `base` again.

The `base` that cabal builds has the same modules as the one that MicroHs ships, as `mhs -L` describes them. An installation of mhs whose `base` and compiler are those that cabal built passes the tests of `cabal-testsuite/PackageTests/MHS`, and the replay with it builds and runs all 91 packages ([local run](results/2026-10-13-local-self-built/summary.md)). CI builds both and compiles a program with them ([CI run](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/runs/38427367498)). `cabal install exe:mhs` does not give a working mhs, which looks for its packages and runtime only beside its binary (item 15 of the inventory).

## Problems outside cabal

[`INVENTORY.md`](INVENTORY.md) lists the bugs and missing features of mhs, and the problems of the MicroHs repository, of MicroCabal and of packages on Hackage, that this work found, with reproductions, and says for each whether users of mhs who do not use cabal are affected. Running the programs of the replay found several, which mcabal has too, since mhs generates the same C and the same command line for the C compiler whichever tool builds a package. The replay works around two of them: it links its executables with `--no-as-needed` on Linux (`CORPUS_OPTIONS` in `replay.py`), as mhs gives the C compiler the libraries of packages before the C files that use them (item 2), and the program for `terminfo` uses `cursorAddress`, whose import of `tparm` names `term.h`, which declares the C functions that `terminfo` imports without a header (items 3 and 21).

## Running it locally

```
# MicroHs from source; ~/.mcabal/bin must be on the PATH
git clone --branch v0.16.9.0 https://github.com/augustss/MicroHs
make -C MicroHs minstall

# cabal with the patches
git clone https://github.com/haskell/cabal
git -C cabal checkout 1f2da2dce875050e1ea9bc0b37972732094125d9
git -C cabal am "$PWD/cabal-mhs-testsuite/patches/"*.patch
(cd cabal && cabal build cabal-install:exe:cabal)

# the replay, about half an hour
python3 cabal-mhs-testsuite/replay.py --cabal "$(cd cabal && cabal list-bin cabal-install:exe:cabal)" \
  --makefile MicroHs/Makefile.packages --work work
python3 cabal-mhs-testsuite/classify.py --work work
```

`terminfo` needs the curses C library, `libncurses-dev` on Debian and Ubuntu. `replay.py --first N --last M` replays part of the list; the log of every step is in `work/logs`, and `classify.py` says why each failing package fails.
