# filter

> Auto-generated documentation for [simplesecurity.filter](../../simplesecurity/filter.py) module.

Some of our analysis tools overlap one-another so lets remove duplicates

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / [simplesecurity](index.md#simplesecurity) / filter
    - [deduplicate](#deduplicate)
    - [filterSeverityAndConfidence](#filterseverityandconfidence)
    - [findingsEqual](#findingsequal)
    - [lookupId](#lookupid)

## deduplicate

[[find in source code]](../../simplesecurity/filter.py#L56)

```python
def deduplicate(findings: list[Finding]) -> list[Finding]:
```

Deduplicate the list of findings

#### Arguments

- `findings` *list[Finding]* - list of findings to deduplicate

#### Returns

- `list[Finding]` - new deduplicated list

## filterSeverityAndConfidence

[[find in source code]](../../simplesecurity/filter.py#L76)

```python
def filterSeverityAndConfidence(
    findings: list[Finding],
    severity: int,
    confidence: int,
) -> list[Finding]:
```

filters the list of findings

#### Arguments

- `findings` *list[Finding]* - list of findings to
- `severity` *int* - min severity
- `confidence` *int* - min confidence

#### Returns

- `list[Finding]` - new deduplicated list

## findingsEqual

[[find in source code]](../../simplesecurity/filter.py#L36)

```python
def findingsEqual(findingA: Finding, findingB: Finding) -> int:
```

Basically and __eq__ method for findings

#### Arguments

- `findingA` *Finding* - lhs
- `findingB` *Finding* - rhs

#### Returns

- `int` - 0 if not equal. 1 if lookup(left) is equal to right - bin left.
-1 if lookup(right) is equal to left - bin right

#### See also

- [Finding](types.md#finding)

## lookupId

[[find in source code]](../../simplesecurity/filter.py#L22)

```python
def lookupId(identifier: str) -> str:
```

Lookup an id in the id map

#### Arguments

- `id` *str* - id to look up

#### Returns

- `str` - id that it equals
