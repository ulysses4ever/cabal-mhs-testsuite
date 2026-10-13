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

## What running the programs shows about mhs

Running the programs found three problems outside cabal. mcabal has them too, since mhs generates the same C and the same command line for the C compiler, whichever tool builds a package.

* **mhs puts the libraries of packages before the C files that use them.** The package file of `terminfo` keeps `-ltinfo`, the curses library that its configure script finds, and mhs passes it to the C compiler before the C files of the program. GCC links with `--as-needed` by default on Debian and Ubuntu, which drops a library that nothing before it uses, so a program calling into `terminfo` fails to link there with `undefined reference to 'set_curterm'`. The replay links its executables with `--no-as-needed` on Linux (`CORPUS_OPTIONS` in `replay.py`), through the `mhs-options` of the project.
* **mhs declares no imported C function.** A function imported without a header, as in `foreign import ccall "f"`, is undeclared where the C that mhs generates calls it. GCC 14 and later reject the call, and older compilers assume that it returns an `int`, which truncates a pointer. Taking the address of such a function, as in `foreign import ccall "&f"`, fails with any compiler. `terminfo` imports most of its C functions that way, so a program calling `setupTerm` compiles only if it also uses an import naming `term.h`, which declares them all; its smoke program uses `cursorAddress` for that. `cpu` imports `cpuid` that way, so the replay does not call it.
* **`time` gets the sign of the time zone wrong under mhs.** With mhs, `HsTime.h` skips the results of the configure script, and `get_current_timezone_seconds` falls back to the C variable `timezone`, which counts seconds west of UTC, without negating it. It also names the zone after standard time. On a machine on US Eastern time in October, `getZonedTime` is eight hours ahead and calls the zone EST. CI runs in UTC, where this does not show.

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
