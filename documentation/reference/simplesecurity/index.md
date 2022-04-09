# Simplesecurity

> Auto-generated documentation for [simplesecurity](../../../simplesecurity/__init__.py) module.

Combine multiple popular python security tools and generate reports or output
into different formats

- [Simplesecurity](../README.md#simplesecurity-index) / [Modules](../MODULES.md#simplesecurity-modules) / Simplesecurity
    - [cli](#cli)
    - [runAllPlugins](#runallplugins)
    - Modules
        - [Module](module.md#module)
        - [Filter](filter.md#filter)
        - [Formatter](formatter.md#formatter)
        - [Level](level.md#level)
        - [Plugins](plugins.md#plugins)
        - [Types](types.md#types)

Plugins (these require the plugin executable in the system path. e.g. bandit
requires bandit to be in the system path...)

- bandit
- safety
- dodgy
- dlint
- semgrep

Formats

- ansi (for terminal)
- json
- markdown
- csv
- sarif

## cli

[[find in source code]](../../../simplesecurity/__init__.py#L67)

```python
def cli():
```

Cli entry point.

## runAllPlugins

[[find in source code]](../../../simplesecurity/__init__.py#L38)

```python
def runAllPlugins(
    pluginMap: dict[str, Any],
    severity: int,
    confidence: int,
    fast: bool,
) -> list[Finding]:
```

Run each plugin. Optimise as much as we can.

#### Arguments

pluginMap (dict[str, Any]): the plugin map
- `severity` *int* - the minimum severity to report on
- `confidence` *int* - the minimum confidence to report on
- `fast` *bool* - runAllPlugins with optimisations

#### Returns

- `list[Finding]` - list of findings

#### See also

- [Finding](types.md#finding)
