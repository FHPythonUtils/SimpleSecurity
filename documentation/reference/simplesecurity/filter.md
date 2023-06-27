# Filter

[Simplesecurity Index](../README.md#simplesecurity-index) /
[Simplesecurity](./index.md#simplesecurity) /
Filter

> Auto-generated documentation for [simplesecurity.filter](../../../simplesecurity/filter.py) module.

- [Filter](#filter)
  - [deduplicate](#deduplicate)
  - [filterSeverityAndConfidence](#filterseverityandconfidence)
  - [findingsEqual](#findingsequal)
  - [lookupId](#lookupid)

## deduplicate

[Show source in filter.py:58](../../../simplesecurity/filter.py#L58)

Deduplicate the list of findings.

#### Arguments

- `findings` *list[Finding]* - list of findings to deduplicate

#### Returns

- `list[Finding]` - new deduplicated list

#### Signature

```python
def deduplicate(findings: list[Finding]) -> list[Finding]:
    ...
```

#### See also

- [Finding](./types.md#finding)



## filterSeverityAndConfidence

[Show source in filter.py:78](../../../simplesecurity/filter.py#L78)

Filter the list of findings.

#### Arguments

- `findings` *list[Finding]* - list of findings to
- `severity` *int* - min severity
- `confidence` *int* - min confidence

#### Returns

- `list[Finding]` - new deduplicated list

#### Signature

```python
def filterSeverityAndConfidence(
    findings: list[Finding], severity: int, confidence: int
) -> list[Finding]:
    ...
```

#### See also

- [Finding](./types.md#finding)



## findingsEqual

[Show source in filter.py:36](../../../simplesecurity/filter.py#L36)

Basically and __eq__ method for findings.

#### Arguments

- `findingA` *Finding* - lhs
- `findingB` *Finding* - rhs

#### Returns

- `int` - 0 if not equal. 1 if lookup(left) is equal to right - bin left.
-1 if lookup(right) is equal to left - bin right

#### Signature

```python
def findingsEqual(findingA: Finding, findingB: Finding) -> int:
    ...
```

#### See also

- [Finding](./types.md#finding)



## lookupId

[Show source in filter.py:22](../../../simplesecurity/filter.py#L22)

Lookup an id in the id map.

#### Arguments

- `identifier` *str* - id to look up

#### Returns

- `str` - id that it equals

#### Signature

```python
def lookupId(identifier: str) -> list[str]:
    ...
```


