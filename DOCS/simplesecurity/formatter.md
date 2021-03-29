# formatter

> Auto-generated documentation for [simplesecurity.formatter](../../simplesecurity/formatter.py) module.

Take our findings dictionary and give things a pretty format.

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / [simplesecurity](index.md#simplesecurity) / formatter
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

[[find in source code]](../../simplesecurity/formatter.py#L154)

```python
def ansi(
    findings: list[Finding],
    heading: Optional[str] = None,
    colourMode: int = 0,
) -> str:
```

Format to ansi.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## csv

[[find in source code]](../../simplesecurity/formatter.py#L115)

```python
def csv(
    findings: list[Finding],
    heading: Optional[str] = None,
    colourMode: int = 0,
) -> str:
```

Format to CSV.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## formatEvidence

[[find in source code]](../../simplesecurity/formatter.py#L36)

```python
def formatEvidence(evidence: list[Line], newlineChar: bool = True) -> str:
```

Format evidence to plaintext.

#### Arguments

- `evidence` *list[Line]* - list of lines of code
- `newlineChar` *bool, optional* - use newline char. Defaults to true

#### Returns

- `str` - string representation of this

## json

[[find in source code]](../../simplesecurity/formatter.py#L95)

```python
def json(
    findings: list[Finding],
    heading: Optional[str] = None,
    colourMode: int = 0,
) -> str:
```

Format to Json.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## markdown

[[find in source code]](../../simplesecurity/formatter.py#L52)

```python
def markdown(
    findings: list[Finding],
    heading: Optional[str] = None,
    colourMode: int = 0,
) -> str:
```

Format to Markdown.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout

## sarif

[[find in source code]](../../simplesecurity/formatter.py#L243)

```python
def sarif(
    findings: list[Finding],
    heading: Optional[str] = None,
    colourMode: int = 0,
) -> str:
```

Format to sarif https://sarifweb.azurewebsites.net/.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.

#### Returns

- `str` - String to write to a file of stdout
