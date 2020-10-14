Module simplesecurity
=====================
Combine multiple popular python security tools and generate reports or output
into different formats

Sub-modules
-----------
* simplesecurity.filter
* simplesecurity.formatter
* simplesecurity.level
* simplesecurity.plugins
* simplesecurity.types

Functions
---------

    
`cli()`
:   cli entry point

    
`runAllPlugins(pluginMap: dict[str, Any], severity: int, confidence: int) ‑> list`
:   Run each plugin
    
    Args:
            pluginMap (dict[str, Any]): the plugin map
            severity (int): the minimum severity to report on
            confidence (int): the minimum confidence to report on
    
    Returns:
            list[Finding]: list of findings