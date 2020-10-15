# types

> Auto-generated documentation for [simplesecurity.types](../../simplesecurity/types.py) module.

Types used by simplesecurity

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / [simplesecurity](index.md#simplesecurity) / types
    - [Finding](#finding)
    - [Line](#line)

## Finding

[[find in source code]](../../simplesecurity/types.py#L10)

```python
class Finding(typing.TypedDict):
```

Finding type

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

## Line

[[find in source code]](../../simplesecurity/types.py#L36)

```python
class Line(typing.TypedDict):
```

Line type

{
 line: int
 content: str
 selected: bool
}
