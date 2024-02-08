# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.2.0

## Added
- Header auto resize for large font sizes (https://github.com/kraanzu/smassh/issues/76)

## Fixed
- Blind Mode not working (https://github.com/kraanzu/smassh/issues/72)
- [WIP] App crash when cursor buddy finishes the test before you (https://github.com/kraanzu/smassh/issues/78)
- [WIP] Added delay for restrictions because the initial calculation is highly variable (https://github.com/kraanzu/smassh/issues/75)

## 3.1.0

## Added
- More Everforest Themes (https://github.com/kraanzu/smassh/pull/77)

## Fixed
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
