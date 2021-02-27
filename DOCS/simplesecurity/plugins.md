# plugins

> Auto-generated documentation for [simplesecurity.plugins](../../simplesecurity/plugins.py) module.

Add plugins here

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

[[find in source code]](../../simplesecurity/plugins.py#L78)

```python
def bandit() -> list[Finding]:
```

Wrapper for bandit. requires bandit on the system path

#### Raises

- `RuntimeError` - if bandit is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## dlint

[[find in source code]](../../simplesecurity/plugins.py#L224)

```python
def dlint() -> list[Finding]:
```

Wrapper for dlint. requires flake8 and dlint on the system path

#### Raises

- `RuntimeError` - if flake8 is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## dodgy

[[find in source code]](../../simplesecurity/plugins.py#L196)

```python
def dodgy() -> list[Finding]:
```

Wrapper for dodgy. requires dodgy on the system path

#### Raises

- `RuntimeError` - if dodgy is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## extractEvidence

[[find in source code]](../../simplesecurity/plugins.py#L56)

```python
def extractEvidence(desiredLine: int, file: str) -> list[Line]:
```

Grab evidence from the source file

#### Arguments

- `desiredLine` *int* - line to highlight
- `file` *str* - file to extract evidence from

#### Returns

- `list[Line]` - list of lines

## pygraudit

[[find in source code]](../../simplesecurity/plugins.py#L256)

```python
def pygraudit() -> list[Finding]:
```

Wrapper for pygraudit. requires pygraudit on the system path

#### Raises

- `RuntimeError` - if pygraudit is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## safety

[[find in source code]](../../simplesecurity/plugins.py#L132)

```python
def safety() -> list[Finding]:
```

Wrapper for safety. requires poetry and safety on the system path

#### Raises

- `RuntimeError` - if saftey is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## safetyFast

[[find in source code]](../../simplesecurity/plugins.py#L179)

```python
def safetyFast() -> list[Finding]:
```

Wrapper for safety. requires safety on the system path

#### Raises

- `RuntimeError` - if saftey is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

## semgrep

[[find in source code]](../../simplesecurity/plugins.py#L284)

```python
def semgrep() -> list[Finding]:
```

Wrapper for semgrep. requires semgrep on the system path (wsl in windows)

#### Raises

- `RuntimeError` - if semgrep is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary
