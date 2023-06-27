# Plugins

[Simplesecurity Index](../README.md#simplesecurity-index) /
[Simplesecurity](./index.md#simplesecurity) /
Plugins

> Auto-generated documentation for [simplesecurity.plugins](../../../simplesecurity/plugins.py) module.

- [Plugins](#plugins)
  - [bandit](#bandit)
  - [dlint](#dlint)
  - [dodgy](#dodgy)
  - [extractEvidence](#extractevidence)
  - [safety](#safety)
  - [semgrep](#semgrep)

## bandit

[Show source in plugins.py:90](../../../simplesecurity/plugins.py#L90)

Generate list of findings using bandit. requires bandit on the system path.

Params:
 scanDir(str): select a scan directory (useful for cicd etc)

#### Raises

- `RuntimeError` - if bandit is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### Signature

```python
def bandit(scanDir=".") -> list[Finding]:
    ...
```

#### See also

- [Finding](./types.md#finding)



## dlint

[Show source in plugins.py:247](../../../simplesecurity/plugins.py#L247)

Generate list of findings using _tool_. requires _tool_ on the system path.

Params:
 scanDir(str): select a scan directory (useful for cicd etc)

#### Raises

- `RuntimeError` - if flake8 is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### Signature

```python
def dlint(scanDir=".") -> list[Finding]:
    ...
```

#### See also

- [Finding](./types.md#finding)



## dodgy

[Show source in plugins.py:211](../../../simplesecurity/plugins.py#L211)

Generate list of findings using _tool_. requires _tool_ on the system path.

Params:
 scanDir(str): select a scan directory (useful for cicd etc)

#### Raises

- `RuntimeError` - if dodgy is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### Signature

```python
def dodgy(scanDir=".") -> list[Finding]:
    ...
```

#### See also

- [Finding](./types.md#finding)



## extractEvidence

[Show source in plugins.py:66](../../../simplesecurity/plugins.py#L66)

Grab evidence from the source file.

#### Arguments

- `desiredLine` *int* - line to highlight
- `file` *str* - file to extract evidence from

#### Returns

- `list[Line]` - list of lines

#### Signature

```python
def extractEvidence(desiredLine: int, file: str) -> list[Line]:
    ...
```

#### See also

- [Line](./types.md#line)



## safety

[Show source in plugins.py:172](../../../simplesecurity/plugins.py#L172)

Generate list of findings using _tool_. requires _tool_ on the system path.

Params:
 scanDir(str): select a scan directory (useful for cicd etc)

#### Raises

- `RuntimeError` - if safety is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### Signature

```python
def safety(scanDir=".") -> list[Finding]:
    ...
```

#### See also

- [Finding](./types.md#finding)



## semgrep

[Show source in plugins.py:302](../../../simplesecurity/plugins.py#L302)

Generate list of findings using for semgrep. Requires semgrep on the
system path (wsl in windows).

#### Raises

- `RuntimeError` - if semgrep is not on the system path, then throw this
error

#### Returns

- `list[Finding]` - our findings dictionary

#### Signature

```python
def semgrep(scanDir=".") -> list[Finding]:
    ...
```

#### See also

- [Finding](./types.md#finding)


