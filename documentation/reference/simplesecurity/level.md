# Level

[Simplesecurity Index](../README.md#simplesecurity-index) /
[Simplesecurity](./index.md#simplesecurity) /
Level

> Auto-generated documentation for [simplesecurity.level](../../../simplesecurity/level.py) module.

- [Level](#level)
  - [Level](#level-1)
    - [Level().__repr__](#level()__repr__)
    - [Level().__str__](#level()__str__)
    - [Level().toSarif](#level()tosarif)

## Level

[Show source in level.py:13](../../../simplesecurity/level.py#L13)

Levels for confidence and severity.

UNKNOWN = 0
LOW = 1
MED = 2
HIGH = 3

#### Signature

```python
class Level(IntEnum):
    ...
```

### Level().__repr__

[Show source in level.py:27](../../../simplesecurity/level.py#L27)

__repr__ method.

#### Returns

- `str` - string representation of a level

#### Signature

```python
def __repr__(self) -> str:
    ...
```

### Level().__str__

[Show source in level.py:35](../../../simplesecurity/level.py#L35)

__str__ method (tostring).

#### Returns

- `str` - string representation of a level

#### Signature

```python
def __str__(self) -> str:
    ...
```

### Level().toSarif

[Show source in level.py:49](../../../simplesecurity/level.py#L49)

Convert to sarif representation.

#### Signature

```python
def toSarif(self) -> str:
    ...
```


