# Types

[Simplesecurity Index](../README.md#simplesecurity-index) /
[Simplesecurity](./index.md#simplesecurity) /
Types

> Auto-generated documentation for [simplesecurity.types](../../../simplesecurity/types.py) module.

- [Types](#types)
  - [Finding](#finding)
  - [Line](#line)

## Finding

[Show source in types.py:12](../../../simplesecurity/types.py#L12)

Finding type.

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

#### Signature

```python
class Finding(typing.TypedDict): ...
```



## Line

[Show source in types.py:38](../../../simplesecurity/types.py#L38)

Line type.

{
 line: int
 content: str
 selected: bool
}

#### Signature

```python
class Line(typing.TypedDict): ...
```