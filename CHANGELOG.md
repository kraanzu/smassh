# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### 3.1.8

- Fix inaccurate accuracy calculation after the incorrect letters were fixed (#99)

### 3.1.7

This release does not change any functionalities, just bumps the underlying tui and fixes upstream nixpkgs

## 3.1.5

This release does not change any functionalities, just bumps the underlying tui and fixes all breaking changes

## 3.1.4

## Fixed

- ZeroDivisionError by @eklairs (closes https://github.com/kraanzu/smassh/issues/86)
- Indication for incorrect space (closes https://github.com/kraanzu/smassh/issues/90)

## 3.1.3

## Fixed
- Crash for python build as root user
- Temp style/tcss files are now stored in cache dir instead of project\
This can be viewed using this command

```bash
python -c "import platformdirs; print(platformdirs.user_cache_dir('smassh'))"
```

## 3.1.2

## Fixed
- Fix bug when creating/saving a new user config

## 3.1.1

## Fixed
- Double Keypress on typing screen (#82)
- Keypress not working after resetting config

## 3.1.0

## Added
- More Everforest Themes (https://github.com/kraanzu/smassh/pull/77)
- Header auto resize for large font sizes (https://github.com/kraanzu/smassh/issues/76)
- Cool Setting Section Separators
- Strip in settings to directly jump to a specific section
- `Reset Config` option in settings

## Fixed
- Blind Mode not working (https://github.com/kraanzu/smassh/issues/72)
- App crash when cursor buddy finishes the test before you (https://github.com/kraanzu/smassh/issues/78)
- Added delay for restrictions because the initial calculation is highly variable (https://github.com/kraanzu/smassh/issues/75)
- Fix Permanent blind mode by (https://github.com/kraanzu/smassh/issues/73)
- --version crash for binary formats

## 3.0.4

## Fixed
- `ctrl+w` when pressed on first letter crashes smassh
- Clicking on setting option won't change setting (https://github.com/kraanzu/smassh/issues/67)

## Added
- `TokyoNight` theme
- 'EveryForest Dark' theme

## 3.0.3

## Fixed
- Fixes backpace color rendering issues (https://github.com/kraanzu/smassh/issues/64)

## 3.0.2

## Added
- Language packs are now stored at user's local data dir
- The first startup might be slow because english lang pack is downloaded and added

## Fixed
- Language pack addition was not working for binaries

## 3.0.1

This new version completely changes the UI so can't really cover in a changelog but I'll \
mention some important changes that users might notice
And ofcourse, the name now is `SMASSH` because `termtyper` was too generic

### Added

- Add support for multiple languages. See WIKI
- Add support for multiple themes

### Removed

- Removed mechanical sounds (I'll work on this in the later versions)
