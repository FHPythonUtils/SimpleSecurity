# Level

> Auto-generated documentation for [simplesecurity.level](../../../simplesecurity/level.py) module.

Levels for confidence and severity.

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../MODULES.md#simplesecurity-modules) / [Simplesecurity](index.md#simplesecurity) / Level
    - [Level](#level)
        - [Level().\_\_repr\_\_](#level__repr__)
        - [Level().\_\_str\_\_](#level__str__)
        - [Level().toSarif](#leveltosarif)

UNKNOWN = 0
LOW = 1
MED = 2
HIGH = 3

## Level

[[find in source code]](../../../simplesecurity/level.py#L13)

```python
class Level(IntEnum):
```

Levels for confidence and severity.

UNKNOWN = 0
LOW = 1
MED = 2
HIGH = 3

### Level().\_\_repr\_\_

[[find in source code]](../../../simplesecurity/level.py#L27)

```python
def __repr__() -> str:
```

__repr__ method.

#### Returns

- `str` - string representation of a level

### Level().\_\_str\_\_

[[find in source code]](../../../simplesecurity/level.py#L35)

```python
def __str__() -> str:
```

__str__ method (tostring).

#### Returns

- `str` - string representation of a level

### Level().toSarif

[[find in source code]](../../../simplesecurity/level.py#L49)

```python
def toSarif() -> str:
```

Convert to sarif representation.
