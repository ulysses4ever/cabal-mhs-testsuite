# cabal-mhs-testsuite

[![replay](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/workflows/ci.yml/badge.svg)](https://github.com/ulysses4ever/cabal-mhs-testsuite/actions/workflows/ci.yml)

This tests the support for [MicroHs](https://github.com/augustss/MicroHs) (`mhs`) in cabal, [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), on the packages that MicroHs itself is tested with.

## What it does

MicroHs's [`Makefile.packages`](https://github.com/augustss/MicroHs/blob/master/Makefile.packages) lists the Hackage packages that its `hackage-ci` workflow installs, on every push, with `mcabal`, the package manager of MicroHs. `replay.py` builds the same packages with cabal driving mhs, one at a time and in the same order: for each package, it builds a tiny executable that depends on it, into a store shared by all the steps. A package counts as built when that succeeds: as with mcabal, its library compiles, and nothing is run.

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

The summary page of every CI run lists which packages build, with the inputs of the run, and why each of the others fails; the logs of all the steps are attached to it.

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
