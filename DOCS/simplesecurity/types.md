# types

> Auto-generated documentation for [simplesecurity.types](../../simplesecurity/types.py) module.

Types used by simplesecurity.

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / [simplesecurity](index.md#simplesecurity) / types
    - [Finding](#finding)
    - [Line](#line)

## Finding

[[find in source code]](../../simplesecurity/types.py#L12)

```python
class Finding(typing.TypedDict):
```

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

## Line

[[find in source code]](../../simplesecurity/types.py#L38)

```python
class Line(typing.TypedDict):
```

Line type.

{
 line: int
 content: str
 selected: bool
}
