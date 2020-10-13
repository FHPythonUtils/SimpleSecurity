# Changelog
All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2020.1.4 - 2020/10/13
- Utf8 is not always the answer. But it is most of the time so use
  `errors="ignore"` for chars that we can't decode


## 2020.1.2/3 - 2020/10/13
- Windows makes me want to cry 😢 - specify utf-8 in more places...

## 2020.1.1 - 2020/10/12
- fix error with poetry show
- set stdout to utf-8 to work with fhmake

## 2020.1 - 2020/10/12
- now works on linux (tested on wsl)
- extract evidence from the source file using the desired line number
- use utf-8 encoding in files
- update to ansi formatting
  - reduce redundancy and therefore save scrolling
  - use box drawing chars to make nice pretty tables
  - update code snippet formatting
- update to csv formatting
  - integrate with new evidence type
- update to markdown formatting
  - integrate with new evidence type
- update to md formatting
  - integrate with new evidence type

## 2020.0.5 - 2020/10/10
- fix python 3.7 and 3.8

## 2020.0.4 - 2020/10/09
- Update typing
- bugfix to csv formatter

## 2020.0.3 - 2020/10/09
- Add full build with all dependencies

## 2020.0.2 - 2020/10/09
- Bugfixes
- Safety will now interrogate dependents of dependencies (via poetry show)

## 2020.0.1 - 2020/10/08
- Bugfix in markdown formatter
- Overview table for markdown and ansi

## 2020 - 2020/10/08
- First release
