# level

> Auto-generated documentation for [simplesecurity.level](../../simplesecurity/level.py) module.

Levels for confidence and severity
UNKNOWN = 0
LOW = 1
MED = 2
HIGH = 3

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / [simplesecurity](index.md#simplesecurity) / level
    - [Level](#level)
        - [Level().toSarif](#leveltosarif)

## Level

[[find in source code]](../../simplesecurity/level.py#L10)

```python
class Level(IntEnum):
```

Levels for confidence and severity
UNKNOWN = 0
LOW = 1
MED = 2
HIGH = 3

### Level().toSarif

[[find in source code]](../../simplesecurity/level.py#L30)

```python
def toSarif() -> str:
```

Convert to sarif representation
