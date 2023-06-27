# Formatter

[Simplesecurity Index](../README.md#simplesecurity-index) /
[Simplesecurity](./index.md#simplesecurity) /
Formatter

> Auto-generated documentation for [simplesecurity.formatter](../../../simplesecurity/formatter.py) module.

- [Formatter](#formatter)
  - [ansi](#ansi)
  - [csv](#csv)
  - [formatEvidence](#formatevidence)
  - [json](#json)
  - [markdown](#markdown)
  - [sarif](#sarif)

## ansi

[Show source in formatter.py:162](../../../simplesecurity/formatter.py#L162)

Format to ansi.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### Signature

```python
def ansi(
    findings: list[Finding], heading: str | None = None, colourMode: int = 0
) -> str:
    ...
```

#### See also

- [Finding](./types.md#finding)



## csv

[Show source in formatter.py:120](../../../simplesecurity/formatter.py#L120)

Format to CSV.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### Signature

```python
def csv(findings: list[Finding], heading: str | None = None, colourMode: int = 0) -> str:
    ...
```

#### See also

- [Finding](./types.md#finding)



## formatEvidence

[Show source in formatter.py:35](../../../simplesecurity/formatter.py#L35)

Format evidence to plaintext.

#### Arguments

- `evidence` *list[Line]* - list of lines of code
- `newlineChar` *bool, optional* - use newline char. Defaults to true

#### Returns

- `str` - string representation of this

#### Signature

```python
def formatEvidence(evidence: list[Line], newlineChar: bool = True) -> str:
    ...
```

#### See also

- [Line](./types.md#line)



## json

[Show source in formatter.py:97](../../../simplesecurity/formatter.py#L97)

Format to Json.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### Signature

```python
def json(
    findings: list[Finding], heading: str | None = None, colourMode: int = 0
) -> str:
    ...
```

#### See also

- [Finding](./types.md#finding)



## markdown

[Show source in formatter.py:51](../../../simplesecurity/formatter.py#L51)

Format to Markdown.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### Signature

```python
def markdown(
    findings: list[Finding], heading: str | None = None, colourMode: int = 0
) -> str:
    ...
```

#### See also

- [Finding](./types.md#finding)



## sarif

[Show source in formatter.py:253](../../../simplesecurity/formatter.py#L253)

Format to sarif https://sarifweb.azurewebsites.net/.

#### Arguments

- `findings` *list[Finding]* - Findings to format
- `heading` *str, optional* - Optional heading to include. Defaults to None.
- `colourMode` *int, optional* - Output with a given colour mode 0: no colour,
 - `1` - default, 2: high contrast. Defaults to 0.

#### Returns

- `str` - String to write to a file of stdout

#### Signature

```python
def sarif(
    findings: list[Finding], heading: str | None = None, colourMode: int = 0
) -> str:
    ...
```

#### See also

- [Finding](./types.md#finding)


