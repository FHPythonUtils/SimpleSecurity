# Plugins

> Auto-generated documentation for [simplesecurity.plugins](../../../simplesecurity/plugins.py) module.

Add plugins here.

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../MODULES.md#simplesecurity-modules) / [Simplesecurity](index.md#simplesecurity) / Plugins
    - [bandit](#bandit)
    - [dlint](#dlint)
    - [dodgy](#dodgy)
    - [extractEvidence](#extractevidence)
    - [safety](#safety)
    - [semgrep](#semgrep)

- bandit
- safety
- dodgy
- dlint
- semgrep

Functions return finding dictionary

```json
{
 title: str
 description: str
 file: str
 evidence: list[Line]
 severity: Level
 confidence: Level
 line: int
 _other: dict[str, str]
}
```

## bandit

[[find in source code]](../../../simplesecurity/plugins.py#L100)

```python
def bandit() -> list[Finding]:
```

Generate list of findings using bandit. requires bandit on the system path.

#### Raises

- `RuntimeError` - if bandit is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### See also

- [Finding](types.md#finding)

## dlint

[[find in source code]](../../../simplesecurity/plugins.py#L244)

```python
def dlint() -> list[Finding]:
```

Generate list of findings using dlint. Requires flake8 and dlint on the system path.

#### Raises

- `RuntimeError` - if flake8 is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### See also

- [Finding](types.md#finding)

## dodgy

[[find in source code]](../../../simplesecurity/plugins.py#L212)

```python
def dodgy() -> list[Finding]:
```

Generate list of findings using dodgy. Requires dodgy on the system path.

#### Raises

- `RuntimeError` - if dodgy is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### See also

- [Finding](types.md#finding)

## extractEvidence

[[find in source code]](../../../simplesecurity/plugins.py#L76)

```python
def extractEvidence(desiredLine: int, file: str) -> list[Line]:
```

Grab evidence from the source file.

#### Arguments

- `desiredLine` *int* - line to highlight
- `file` *str* - file to extract evidence from

#### Returns

- `list[Line]` - list of lines

#### See also

- [Line](types.md#line)

## safety

[[find in source code]](../../../simplesecurity/plugins.py#L177)

```python
def safety() -> list[Finding]:
```

Generate list of findings using safety.

#### Raises

- `RuntimeError` - if safety is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### See also

- [Finding](types.md#finding)

## semgrep

[[find in source code]](../../../simplesecurity/plugins.py#L282)

```python
def semgrep() -> list[Finding]:
```

Generate list of findings using for semgrep. Requires semgrep on the
system path (wsl in windows).

#### Raises

- `RuntimeError` - if semgrep is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### See also

- [Finding](types.md#finding)
