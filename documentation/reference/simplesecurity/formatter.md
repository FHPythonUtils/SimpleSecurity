# Formatter

> Auto-generated documentation for [simplesecurity.formatter](../../../simplesecurity/formatter.py) module.

Take our findings dictionary and give things a pretty format.

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../MODULES.md#simplesecurity-modules) / [Simplesecurity](index.md#simplesecurity) / Formatter
    - [ansi](#ansi)
    - [csv](#csv)
    - [formatEvidence](#formatevidence)
    - [json](#json)
    - [markdown](#markdown)
    - [sarif](#sarif)

finding dictionary

```json
{
 title: str
 description: str
 file: str
 evidence: list[Line]
 severity: Level
 confidence: Level
 line: int
 _other: {}
}
```

Formats

- markdown
- json
- csv
- ansi

## ansi

[[find in source code]](../../../simplesecurity/formatter.py#L162)

```python
def ansi(
    findings: list[Finding],
    heading: str | None = None,
    colourMode: int = 0,
) -> str:
```

Format to ansi.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [Finding](types.md#finding)

## csv

[[find in source code]](../../../simplesecurity/formatter.py#L120)

```python
def csv(
    findings: list[Finding],
    heading: str | None = None,
    colourMode: int = 0,
) -> str:
```

Format to CSV.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [Finding](types.md#finding)

## formatEvidence

[[find in source code]](../../../simplesecurity/formatter.py#L35)

```python
def formatEvidence(evidence: list[Line], newlineChar: bool = True) -> str:
```

Format evidence to plaintext.

#### Arguments

- `evidence` *list[Line]* - list of lines of code
- `newlineChar` *bool, optional* - use newline char. Defaults to true

#### Returns

- `str` - string representation of this

#### See also

- [Line](types.md#line)

## json

[[find in source code]](../../../simplesecurity/formatter.py#L97)

```python
def json(
    findings: list[Finding],
    heading: str | None = None,
    colourMode: int = 0,
) -> str:
```

Format to Json.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [Finding](types.md#finding)

## markdown

[[find in source code]](../../../simplesecurity/formatter.py#L51)

```python
def markdown(
    findings: list[Finding],
    heading: str | None = None,
    colourMode: int = 0,
) -> str:
```

Format to Markdown.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [Finding](types.md#finding)

## sarif

[[find in source code]](../../../simplesecurity/formatter.py#L253)

```python
def sarif(
    findings: list[Finding],
    heading: str | None = None,
    colourMode: int = 0,
) -> str:
```

Format to sarif https://sarifweb.azurewebsites.net/.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### See also

- [Finding](types.md#finding)
