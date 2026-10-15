# Inventory of mhs bugs and feature requests

What the work on [haskell/cabal#11392](https://github.com/haskell/cabal/pull/11392), cabal building packages with MicroHs, found outside cabal: in mhs, in the MicroHs repository, in MicroCabal, and in packages on Hackage. It comes from replaying MicroHs's package list with cabal ([`replay.py`](replay.py)), from running small programs with each package, and from building MicroHs itself with cabal.

Every bug comes with an example, what was expected, and what happens, and every item says whether users of mhs who do not use cabal, with plain `mhs` or with `mcabal`, are affected. The examples ran with MicroHs v0.16.9.0 and GCC 15 on Linux; outputs are cut to the lines that matter, and home directories are shortened to `~`. Item 1 is still on MicroHs master as of 2026-10-13; the others were not checked against master. None of it has been reported upstream yet.

## mhs

### Bugs

**1. An installed mhs never searches the package directory of the user.**

`mhs.conf` sets `packageDbPath = "$MHSPKG:$HOME/.mcabal-user/mhs-$VERSION"`: the package directory of the installation, where `base` is, then the package directory of the user. An mhs that runs from an installation expands `$MHSPKG` and `$HOME` right, but `$VERSION` to the directory of its installation instead of its version, so the second directory is a path that cannot exist.

Example, with mhs installed by `make minstall` into `~/.mcabal`, and the package and the program in separate directories:

```haskell
-- pkg/Hello.hs
module Hello (hello) where

hello :: String
hello = "hello from a package"

-- prog/Main.hs
module Main (main) where

import Hello (hello)

main :: IO ()
main = putStrLn hello
```

```
pkg$ mhs -Phello-1.0 -o hello-1.0.pkg Hello
pkg$ mhs -Q hello-1.0.pkg ~/.mcabal-user/mhs-0.16.9.0
prog$ mhs Main.hs -omain
```

Expected: `mhs` finds `Hello` in `~/.mcabal-user/mhs-0.16.9.0`, and `./main` prints `hello from a package`.

Actual:

```
mhs: uncaught exception: error: "Main.hs": line 3, col 8: Module not found: Hello
search path=["."]
package path=["~/.mcabal/bin/../mhs-0.16.9.0","~/.mcabal-user/mhs-~/.mcabal/bin/../mhs-0.16.9.0"]
```

The first entry of the package path is right: `$MHSPKG` is the package directory of the installation, `~/.mcabal/mhs-0.16.9.0`, which holds `packages/base-0.16.9.0.pkg`. The second should be `~/.mcabal-user/mhs-0.16.9.0`, but it is `~/.mcabal-user/mhs-` followed by that same installation directory. With `VERSION=0.16.9.0` set in the environment, the second entry is right and the example works; with `HOME` unset, `$HOME` becomes the installation directory too.

Why: `expandEnvLookup` in `MicroHs.Main` expands the variables of `packageDbPath`, and is given the installation directory when mhs runs from an installation:

```haskell
expandEnvLookup :: Maybe FilePath -> String -> IO String
expandEnvLookup (Just s) mpkg = fromMaybe s <$> lookupEnv mpkg
expandEnvLookup _ "VERSION" = return mhsVersion
expandEnvLookup _ name = fromMaybe "" <$> lookupEnv name
```

The first clause is meant for `MHSPKG`, but `mpkg` is a variable, not the string `"MHSPKG"`, so it matches every name: an installed mhs takes every variable from the environment, and falls back to its installation directory for those that are not set. `HOME` is set, `VERSION` is not, and the clause that gives the version is reached only by an mhs that runs from its source tree or with `MHSDIR` set, which have no installation directory.

Fix: match the names.

```haskell
expandEnvLookup _ "VERSION" = return mhsVersion
expandEnvLookup (Just s) "MHSPKG" = fromMaybe s <$> lookupEnv "MHSPKG"
expandEnvLookup _ name = fromMaybe "" <$> lookupEnv name
```

An installed mhs built with this change has the package path `["~/.mcabal/bin/../mhs-0.16.9.0","~/.mcabal-user/mhs-0.16.9.0"]`.

Without cabal: anyone who installs packages into the user directory that `mhs.conf` names, with `mhs -Q` or another tool, has to add it with `-a`. mcabal is not affected, as it installs elsewhere (item 18), and neither is `cabal install --lib`, which installs where mcabal does.

**2. mhs gives the C compiler the libraries of packages before the C files that use them.**

`mainCompileC` puts the linker options that a package keeps, those given with `-optl` to `mhs -P`, before the C files of the program. A linker that drops a library that nothing before it uses, as GCC's `--as-needed`, which is the default on Ubuntu, then drops them.

Example, with zlib, where `-optl -Wl,--as-needed` stands for Ubuntu's default:

```haskell
-- Z.hs
module Z (zlibVersion) where

import Foreign.C.String (CString)

foreign import capi "zlib.h zlibVersion" zlibVersion :: IO CString

-- prog/Main.hs
module Main (main) where

import Foreign.C.String (peekCString)
import Z (zlibVersion)

main :: IO ()
main = zlibVersion >>= peekCString >>= putStrLn
```

```
$ mhs -Pz-1.0 -o z-1.0.pkg -optl -lz Z
prog$ mhs -p../z-1.0.pkg Main.hs -omain && ./main
1.3.2
prog$ mhs -p../z-1.0.pkg -optl -Wl,--as-needed Main.hs -omain
```

Expected: as without `--as-needed`, `./main` prints the version of zlib.

Actual:

```
mhscB3EScE.c:(.text+0xc): undefined reference to `zlibVersion'
collect2: error: ld returned 1 exit status
```

Fix: put the linker options of packages after the C files, next to `cclibs`.

Without cabal: every user of mhs on Ubuntu whose program uses a package that links a C library, however the package was built. MicroCabal stores the `extra-libraries` of a package the same way, with `-optl -l<lib>`. With cabal: the same, for instance terminfo fails with `undefined reference to 'set_curterm'`; the replay links with `-optl -Wl,--no-as-needed` on Linux meanwhile.

**3. mhs declares no C function that a program imports.**

The C that mhs generates calls a function imported without a header, and takes the address of one imported with `&`, without declaring it.

Example, with `c.c`:

```c
int triple(int x) { return 3 * x; }

int counter = 14;

const char *greeting(void) { return "hello from C"; }
```

```haskell
-- Call.hs
module Main (main) where

import Foreign.C.Types (CInt (..))

foreign import ccall "triple" triple :: CInt -> CInt

main :: IO ()
main = print (triple 14)

-- Addr.hs
module Main (main) where

import Foreign.C.Types (CInt)
import Foreign.Ptr (Ptr)
import Foreign.Storable (peek)

foreign import ccall "&counter" counter :: Ptr CInt

main :: IO ()
main = peek counter >>= print

-- Ptr.hs
module Main (main) where

import Foreign.C.String (CString, peekCString)

foreign import ccall "greeting" greeting :: IO CString

main :: IO ()
main = greeting >>= peekCString >>= putStrLn
```

Expected, as with GHC: `mhs Call.hs c.c -oCall` builds a program that prints `42`, `Addr.hs` one that prints `14`, and `Ptr.hs` one that prints `hello from C`.

Actual:

```
$ mhs Call.hs c.c -oCall
mhscjASdt4.c:1653:54: error: implicit declaration of function 'triple' [-Wimplicit-function-declaration]
$ mhs Addr.hs c.c -oAddr
mhscgM55Qp.c:1659:61: error: 'counter' undeclared (first use in this function)
$ mhs -optc -fpermissive Ptr.hs c.c -oPtr && ./Ptr
Segmentation fault (core dumped)
```

GCC 14 and later reject the call. With `-fpermissive`, or with GCC 13 and earlier, which accept it, the result is taken to be an `int`, which truncates the pointer that `greeting` returns. With the import `"greet.h greeting"` and a header declaring `greeting`, `Ptr` prints `hello from C`.

Fix: declare the function from its Haskell type when the import names no header, as GHC does.

Without cabal: every user of mhs whose program reaches such an import, in their own code or in a package; terminfo and cpu are two (items 21 and 22).

**4. `foreign import ccall "wrapper"` and `"dynamic"` are not implemented.**

Example:

```haskell
-- Wrapper.hs
module Main (main) where

import Foreign.Ptr (FunPtr, freeHaskellFunPtr)

foreign import ccall "wrapper" mkCallback :: IO () -> IO (FunPtr (IO ()))

main :: IO ()
main = do
  callback <- mkCallback (putStrLn "called back")
  freeHaskellFunPtr callback
  putStrLn "made and freed a callback"

-- Dynamic.hs
module Main (main) where

import Foreign.C.Types (CInt (..))
import Foreign.Ptr (FunPtr)

foreign import ccall "stdlib.h &abs" absPtr :: FunPtr (CInt -> CInt)
foreign import ccall "dynamic" callIntFun :: FunPtr (CInt -> CInt) -> CInt -> CInt

main :: IO ()
main = print (callIntFun absPtr (-5))
```

Expected, as the FFI of Haskell 2010 specifies and GHC does: programs that print `made and freed a callback` and `5`.

Actual, for both `mhs Wrapper.hs -oWrapper` and `mhs Dynamic.hs -oDynamic`:

```
mhs: uncaught exception: error: Unimplemented FFI feature
```

The documentation of MicroHs does not mention it.

Without cabal: every user of mhs whose program reaches such an import; with terminfo, any program that calls `runTermOutput`.

### Feature requests

**5. Install the C files of a package with `mhs -Q`.** When it links a program, mhs compiles the `cbits/*.c` beside each package file and includes its `include` directory, but `mhs -Q` copies only the package file. Every tool that installs packages copies them itself, as MicroCabal and cabal do. Without cabal: users of `mhs -Q` whose packages have C sources.

**6. Keep the C compiler options of a package.** `mhs -P` keeps `-optl` options but not `-optc` ones, so the `cc-options` of a library cannot apply to its C sources, which are compiled with the options of each program that uses it. MicroCabal passes the C sources of a library to `mhs -P` with `-optc`, where they are ignored. Without cabal: the same for mcabal.

**7. Say which Hackage versions the packages bundled in base stand for.** base-0.16.9.0 bundles the modules of bytestring, text, deepseq, stm, directory, process, hashable and integer-logarithms. MicroCabal and cabal both hardcode the versions at which to present them to packages from Hackage, base-4.19.1.0, bytestring-0.12.1.0 and so on. A line in what `mhs -L<pkg>` prints, such as `provides: base-4.19.1.0 bytestring-0.12.1.0 ...`, would let both read them from mhs. Without cabal: mcabal keeps its own table.

**8. Print the package search path.** `mhs -L` lists only the directories of the search path that hold packages, so a tool cannot learn where the user directory is before something is installed there. cabal hardcodes `~/.mcabal-user/mhs-<version>` from the default `mhs.conf`. Without cabal: no effect.

**9. Pass a header to cpphs.** mhs passes only `-D` and `-I` options on to cpphs, so cabal defines the macros of `cabal_macros.h` one `-D` at a time instead of including the header. An `-include FILE` or `-optP` option would do. mhs also passes the same `-D` and `-I` options to the C compiler when it links a program, so cabal's version macros reach it too, which is harmless but noisy. Without cabal: mcabal passes its macros as `-D` too.

**10. `Data.Text.Lazy.Encoding`.** xhtml 3000.3 and later import it, and the base of mhs lacks it, so the replay constrains xhtml below 3000.3. Without cabal: mcabal takes the version of xhtml from Stackage, and fails if it is 3000.3 or later.

## The MicroHs repository

### Bugs

cabal builds `lib/base.cabal` and `MicroHs.cabal` with mhs once items 11 to 14 are fixed, as the [README](README.md#building-microhs-with-cabal) describes; [`microhs-cabal-fixes.patch`](microhs-cabal-fixes.patch) fixes them. Items 11 to 13 and 16 also show with a cabal that knows nothing of mhs. Without cabal, mcabal does not mind any of them.

**11. `lib/base.cabal`: `library base` should be `library`.**

Expected: `cabal check` in `lib` reports no errors. Actual:

```
Error: [illegal-library-name] Illegal internal library name base. Internal
libraries cannot have the same name as the package. Maybe you wanted a
non-internal library? If so, rewrite the section stanza from 'library: 'base'
to 'library'.
```

mcabal reads both stanzas the same way.

**12. `lib/base.cabal`: `Data.Float` is listed twice in `exposed-modules`.**

Expected: no error. Actual, from the same `cabal check`:

```
Error: [duplicate-modules] Duplicate modules in library: Data.Float
```

**13. `lib/base.cabal`: six of the modules it lists have no source.**

They are `Control.Exception.Internal.Map`, `.Set`, `.TVar` and `.TransactionLog`, apparently copied from the list of `Control.Concurrent.STM.Internal`, and `Data.Int.IntN` and `Data.Int.Instances`.

Expected: `cabal sdist --list-only` in `lib` lists the sources. Actual:

```
Error: [Cabal-6421]
Could not find module: Control.Exception.Internal.Map with any suffix: ["chs","hsc","x","y","ly","cpphs","hs","lhs","hsig","lhsig"].
```

**14. `MicroHs.cabal` lists for every compiler modules that only GHC needs.**

`Data.Double`, `Data.Integer`, `System.IO.MD5`, `System.IO.Serialize`, `System.IO.TimeMilli`, `System.IO.Transducers` and `System.Compress` are in the `other-modules` of the executable, but have sources only in `ghc/`; with mhs, base provides them.

Expected: `cabal build exe:mhs` with mhs, with cabal from #11392, builds mhs. Actual:

```
Error: [Cabal-7554]
can't find source for Data/Double in mhs, src, dist-newstyle/build/.../autogen, ...
```

Fix: list them under `if impl(ghc)`. MicroHs still builds with GHC then.

**15. `cabal install` does not give a working mhs.**

The README says "Doing `cabal install` will install the compiler." cabal installs the `data-files` of MicroHs, its runtime and the sources of base among them, in the data directory of the package, but mhs looks for them only through `MHSDIR`, in the source tree, or in the layout of its own installer beside its binary, `<bin>/../mhs-<version>`.

Example, with GHC and a cabal without the patches of #11392:

```
MicroHs$ cabal install exe:mhs
$ printf 'main :: IO ()\nmain = putStrLn "hello"\n' > Hello.hs
$ mhs Hello.hs -ohello
```

Expected: `./hello` prints `hello`. Actual:

```
Warning: cannot find config file: ~/.local/bin/../mhs-0.16.9.0/packages/mhs-0.16.9.0/data/mhs.conf
mhs: no location: Module not found: Prelude
search path=["."]
package path=["~/.local/bin/../mhs-0.16.9.0"]
```

With `MHSDIR` set to the data directory that cabal installed, `share` of the package in the store, the same mhs compiles and runs `Hello.hs`.

Fix: look in the data directory of `Paths_MicroHs` as a last resort, or say in the README that `MHSDIR` has to be set. The same holds for an mhs that cabal builds with mhs.

Without cabal: no effect; `make minstall` lays the installation out as mhs expects.

**16. Minor problems that `cabal check` reports in `lib/base.cabal`:** the `license-file`, `LICENSE`, is not in `lib`; `hs-source-dirs: gmp`, under the flag `gmp`, names a directory that does not exist; and there is no `default-language`.

Building base with cabal also takes `allow-boot-library-installs: True` in `cabal.project`, as base cannot be rebuilt otherwise; that is cabal's policy, not a bug.

## MicroCabal

These are inconsistencies rather than bugs: they make no visible difference with mcabal.

**17. hashable is presented at 1.0.0.0.** MicroCabal calls it "very rudimentary", but the `Data.Hashable` of mhs has the API of the 1.4 series, which unordered-containers and these require. mcabal ignores bounds, and no package of the list tests `MIN_VERSION_hashable`, so it makes no difference there. cabal presents it at 1.4.7.0.

**18. mcabal installs into `~/.mcabal/mhs-<version>`**, or `$CABALDIR`, which is the package directory of mhs itself after `make minstall`, rather than into the user directory that `mhs.conf` names, `~/.mcabal-user/mhs-<version>`. `cabal install --lib` installs where mcabal does, so that mhs finds what both install in spite of item 1. When mhs is installed elsewhere, plain `mhs` searches neither directory.

## Packages on Hackage

### Bugs

**19. hspec-core imports `Control.Concurrent.Async` without depending on async under mhs.**

It compiles its vendored copy of async only for GHC.

Expected: hspec-core 2.11.17 builds with mhs and the dependencies it declares. Actual, with cabal:

```
mhs: uncaught exception: error: "src/Test/Hspec/Core/Util.hs": line 34, col 18: Module not found: Control.Concurrent.Async
```

Fix: `build-depends: async` under `if impl(mhs)`, or in an `else` of `if impl(ghc)`. The replay patches a copy, see `PATCHED` in `replay.py`.

Without cabal: mcabal makes every installed package visible to mhs, so hspec-core builds as long as async is installed, as it is in MicroHs's list; otherwise mcabal fails the same way.

**20. time gets the time zone wrong under mhs.**

When `__MHS__` is defined, `HsTime.h` leaves out the results of the configure script, and `get_current_timezone_seconds` falls back to returning the C variable `timezone`, which counts seconds west of UTC, without negating it. It also names the zone after standard time during daylight saving time.

Example:

```haskell
module Main (main) where

import Data.Time (UTCTime (..), fromGregorian, getTimeZone, timeZoneMinutes, timeZoneName)

main :: IO ()
main = do
  -- Noon UTC on 1 July 2026, during daylight saving time in New York.
  zone <- getTimeZone (UTCTime (fromGregorian 2026 7 1) 43200)
  putStrLn (timeZoneName zone ++ " " ++ show (timeZoneMinutes zone))
```

| `TZ` | Expected, as with GHC | Actual, with mhs |
|---|---|---|
| `America/New_York` | `EDT -240` | `EST 240` |
| `Asia/Tokyo` | `JST 540` | `JST -540` |
| `UTC` | `UTC 0` | `UTC 0` |

Fix: negate it, as the branch for Windows does, and name the zone from `tzname[1]` when `tm_isdst` is set.

Without cabal: every user of mhs whose program uses time zones outside UTC, with mcabal too.

**21. terminfo imports most of its C functions without a header,** `setupterm`, `set_curterm`, `tigetnum` and `&del_curterm` among them, so mhs cannot compile a program that calls `setupTerm` (item 3).

Example, compiled with plain `mhs`, given the directory into which `cabal install --lib terminfo` installed it:

```haskell
module Main (main) where

import System.Console.Terminfo (getCapability, setupTerm, termColumns)

main :: IO ()
main = do
  term <- setupTerm "dumb"
  print (getCapability term termColumns)
```

Expected, as with GHC: `Just 80`. Actual:

```
mhscxAsTet.c:1766:56: error: implicit declaration of function 'tigetnum'; did you mean 'mhs_tigetnum'? [-Wimplicit-function-declaration]
mhscxAsTet.c:1767:78: error: 'del_curterm' undeclared (first use in this function)
mhscxAsTet.c:1768:31: error: implicit declaration of function 'setupterm'; did you mean 'mhs_setupterm'? [-Wimplicit-function-declaration]
mhscxAsTet.c:1769:59: error: implicit declaration of function 'set_curterm'; did you mean 'mhs_set_curterm'? [-Wimplicit-function-declaration]
```

A program that also uses `cursorAddress`, whose import of `tparm` names `term.h`, which declares the others, compiles and prints `Just 80`. Its output functions also need item 4.

Fix: imports with `capi "term.h ..."`, which would also check them against the header with GHC, or item 3.

Without cabal: every user of terminfo with mhs; the C is the same whichever tool built terminfo.

**22. cpu imports `cpuid` without a header.**

Example, compiled the same way:

```haskell
module Main (main) where

import System.Cpuid (cpuid)

main :: IO ()
main = cpuid 0 >>= print
```

Expected, as with GHC: the four registers that `cpuid 0` returns. Actual:

```
mhscd7ZoKX.c:1862:27: error: implicit declaration of function 'cpuid' [-Wimplicit-function-declaration]
```

GCC 13 and earlier only warn about implicit declarations. Fix: a header, or item 3.

Without cabal: every user of cpu with mhs and GCC 14 or later.

### Other

**23. Bounds.** The replay lifts a few, see [`project.extra`](project.extra): the indexed-traversable fork of MicroHs caps containers below 0.8, the first version that mhs can build, and hspec and hspec-core cap QuickCheck below 2.19, the version that the Makefile of MicroHs takes from git. Without cabal: mcabal ignores bounds.
