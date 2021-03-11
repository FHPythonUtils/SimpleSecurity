# plugins

> Auto-generated documentation for [simplesecurity.plugins](../../simplesecurity/plugins.py) module.

Add plugins here.

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / [simplesecurity](index.md#simplesecurity) / plugins
    - [bandit](#bandit)
    - [dlint](#dlint)
    - [dodgy](#dodgy)
    - [extractEvidence](#extractevidence)
    - [pygraudit](#pygraudit)
    - [safety](#safety)
    - [safetyFast](#safetyfast)
    - [semgrep](#semgrep)

- bandit
- safety
- dodgy
- dlint
- pygraudit
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
 _other: {}
}
```

## bandit

[[find in source code]](../../simplesecurity/plugins.py#L92)

```python
def bandit() -> list[Finding]:
```

Generate list of findings using bandit. requires bandit on the system path.

#### Raises

- `RuntimeError` - if bandit is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## dlint

[[find in source code]](../../simplesecurity/plugins.py#L261)

```python
def dlint() -> list[Finding]:
```

Generate list of findings using dlint. Requires flake8 and dlint on the system path.

#### Raises

- `RuntimeError` - if flake8 is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## dodgy

[[find in source code]](../../simplesecurity/plugins.py#L229)

```python
def dodgy() -> list[Finding]:
```

Generate list of findings using dodgy. Requires dodgy on the system path.

#### Raises

- `RuntimeError` - if dodgy is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## extractEvidence

[[find in source code]](../../simplesecurity/plugins.py#L64)

```python
def extractEvidence(desiredLine: int, file: str) -> list[Line]:
```

Grab evidence from the source file.

#### Arguments

- `desiredLine` *int* - line to highlight
- `file` *str* - file to extract evidence from

#### Returns

- `list[Line]` - list of lines

## pygraudit

[[find in source code]](../../simplesecurity/plugins.py#L298)

```python
def pygraudit() -> list[Finding]:
```

Generate list of findings using pygraudit. Requires pygraudit on the system path.

#### Raises

- `RuntimeError` - if pygraudit is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## safety

[[find in source code]](../../simplesecurity/plugins.py#L166)

```python
def safety() -> list[Finding]:
```

Generate list of findings using safety. requires poetry and safety on the system path.

#### Raises

- `RuntimeError` - if safety is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## safetyFast

[[find in source code]](../../simplesecurity/plugins.py#L213)

```python
def safetyFast() -> list[Finding]:
```

Generate list of findings using safety. requires safety on the system path.

#### Raises

- `RuntimeError` - if safety is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## semgrep

[[find in source code]](../../simplesecurity/plugins.py#L331)

```python
def semgrep() -> list[Finding]:
```

Generate list of findings using for semgrep...

Requires semgrep on the system path (wsl in windows).

#### Raises

- `RuntimeError` - if semgrep is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary
