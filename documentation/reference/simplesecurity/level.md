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

#### Signature

```python
class Level(IntEnum):
    ...
```

### Level().__repr__

[Show source in level.py:22](../../../simplesecurity/level.py#L22)

__repr__ method.

#### Returns

- `str` - string representation of a level

#### Signature

```python
def __repr__(self) -> str:
    ...
```

### Level().__str__

[Show source in level.py:30](../../../simplesecurity/level.py#L30)

__str__ method (tostring).

#### Returns

- `str` - string representation of a level

#### Signature

```python
def __str__(self) -> str:
    ...
```

### Level().toSarif

[Show source in level.py:45](../../../simplesecurity/level.py#L45)

Convert to sarif representation.

#### Signature

```python
def toSarif(self) -> str:
    ...
```


