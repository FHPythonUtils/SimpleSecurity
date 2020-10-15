# plugins

> Auto-generated documentation for [simplesecurity.plugins](../../simplesecurity/plugins.py) module.

Add plugins here

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / [simplesecurity](index.md#simplesecurity) / plugins
    - [bandit](#bandit)
    - [dlint](#dlint)
    - [dodgy](#dodgy)
    - [extractEvidence](#extractevidence)
    - [safety](#safety)

- bandit
- safety
- dodgy
- dlint

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

[[find in source code]](../../simplesecurity/plugins.py#L73)

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

[[find in source code]](../../simplesecurity/plugins.py#L184)

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

[[find in source code]](../../simplesecurity/plugins.py#L156)

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

[[find in source code]](../../simplesecurity/plugins.py#L51)

```python
def extractEvidence(desiredLine: int, file: str) -> list[Line]:
```

Grab evidence from the source file

#### Arguments

- `desiredLine` *int* - line to highlight
- `file` *str* - file to extract evidence from

#### Returns

- `list[Line]` - list of lines

## safety

[[find in source code]](../../simplesecurity/plugins.py#L105)

```python
def safety() -> list[Finding]:
```

Wrapper for safety. requires poetry and safety on the system path

#### Raises

- `RuntimeError` - if saftey is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary
