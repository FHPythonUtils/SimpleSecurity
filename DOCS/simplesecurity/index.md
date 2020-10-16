# simplesecurity

> Auto-generated documentation for [simplesecurity](../../simplesecurity/__init__.py) module.

Combine multiple popular python security tools and generate reports or output
into different formats

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../README.md#simplesecurity-modules) / simplesecurity
    - [cli](#cli)
    - [runAllPlugins](#runallplugins)
    - Modules
        - [\_\_main\_\_](module.md#__main__)
        - [filter](filter.md#filter)
        - [level](level.md#level)
        - [plugins](plugins.md#plugins)
        - [types](types.md#types)

## cli

[[find in source code]](../../simplesecurity/__init__.py#L45)

```python
def cli():
```

cli entry point

## runAllPlugins

[[find in source code]](../../simplesecurity/__init__.py#L20)

```python
def runAllPlugins(
    pluginMap: dict[(str, Any)],
    severity: int,
    confidence: int,
    fast: bool,
) -> list[Finding]:
```

Run each plugin. Optimise as much as we can

#### Arguments

pluginMap (dict[str, Any]): the plugin map
- `severity` *int* - the minimum severity to report on
- `confidence` *int* - the minimum confidence to report on

#### Returns

- `list[Finding]` - list of findings
