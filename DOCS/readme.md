Module simplesecurity
=====================
Combine multiple popular python security tools and generate reports or output
into different formats

Plugins (these require the plugin executable in the system path. e.g. bandit
requires bandit to be in the system path...)

- bandit
- safety
- dodgy
- dlint

Formats

- ansi (for terminal)
- json
- md
- csv

Sub-modules
-----------
* simplesecurity.formatter
* simplesecurity.level
* simplesecurity.plugins

Functions
---------

    
`cli()`
:   cli entry point