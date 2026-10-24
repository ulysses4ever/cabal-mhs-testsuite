# Replay with each rewrite switched off

MicroHs's package list, replayed with cabal built at the head of [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), [`f62e6be`](https://github.com/haskell/cabal/pull/11392/commits/f62e6be7593f3a4c72cf8b774a003e552d876f78), with each of the three things it does for packages from Hackage under mhs switched off in turn, the same way as the [replay of each commit](../2026-10-24-per-commit), where all 91 build with all three. [`switches.patch`](switches.patch) adds the switches, read from `MHS_ABLATE`, to `Cabal/src/Distribution/Simple/MHS.hs`; it is for this measurement only and not part of the PR.

| Switched off | `MHS_ABLATE` | Build and run |
|---|---|---:|
| Base of mhs presented as itself, base-0.16.9.0, without the packages it bundles (`compatPackages`) | `nocompat` | [0/91](nocompat/summary.md) |
| Array and random kept, rather than replaced with array-mhs and random-mhs (`forkedPackages`) | `noforks` | [71/91](noforks/summary.md) |
| No ghc-compat added to the components | `noghccompat` | [67/91](noghccompat/summary.md) |
