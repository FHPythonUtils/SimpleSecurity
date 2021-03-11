# Changelog
All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2021.2.1 - 2021/03/11
- Fix bandit ignore paths.
- Reformat with black + tabs

## 2021.2 - 2021/03/01
- Added `--zero/-0` flag to return non-zero exit code if any security
  vulnerabilities are found

## 2021.1.1 - 2021/02/27
- Tweak safety plugin so it reads from the local requirements file if possible


## 2021.1 - 2021/02/21
- Fix `_doSafetyProcessing` findings/evidence
- Update semgrep rules 2021/01/19 e74345b
  https://github.com/returntocorp/semgrep-rules/tree/e74345bda4b1e080a7c72d383d06f1d110dedbce

## 2021 - 2021/01/04
- Bandit broke things! Now fixed

## 2020.5.0 - 2020/10/18
- Added sarif format https://sarifweb.azurewebsites.net/

## 2020.4.1 - 2020/10/17
- Bugfixes with deduplication and erroneous print

## 2020.4 - 2020/10/16
- Add PyGraudit https://github.com/FHPythonUtils/PyGraudit
  - Pretty fast
  - Not particularly accurate - lots of false negatives
- semgrep https://github.com/returntocorp/semgrep
  - Pretty slow (looking at 30s to run 110 tests)
  - Pretty good (probably on par with bandit)
- Added `--fast/--skip` to skip past slow plugins when running all plugins
  - This will skip `semgrep` (saving 30s of 35s in tests)
  - This will run a less reliable instance of `dodgy` (saving 3s of 5s in tests)
  - ...so runtime is taken down from around 35s to 2s
- Using semgrep rules 2020/10/16 52d7424
  https://github.com/returntocorp/semgrep-rules/commit/52d74240dd3ece8d54a626aae89cb13af4b4d224

## 2020.3.1 - 2020/10/15
- Added mode to seperate stdout and stderr (bandit plugin uses this)

## 2020.3 - 2020/10/14
- Deduplicator has moved to filter - Use
  `from simplesecurity.filter import deduplicate` to use the deduplicator
- Added `filterSeverityAndConfidence` to `simplesecurity.filter`
  - Filter level/ severity and confidence from the command line with -l INT
    and -s INT
- Added colour modes: 0 for no colour, 1 for colour, 2 for high contrast
  - Use -Z from the command line for high contrast and -z for no colour
- Minor tweaks

## 2020.2 - 2020/10/13
- New deduplication engine - So no more duplicates when running from the command
  line! Use `from simplesecurity.deduplicate import deduplicate` to use the
  deduplicator downstream.
- `id`s are now included in findings and are included in json and csv output

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
