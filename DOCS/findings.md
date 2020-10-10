Module simplesecurity.findings
==============================
finding dictionary

```json
{
        title: str
        description: str
        file: str
        evidence: str
        severity: Level
        confidence: Level
        line: str
        _other: {}
}
```

Classes
-------

`Finding(*args, **kwargs)`
:   Finding type

    ### Ancestors (in MRO)

    * builtins.dict

    ### Class variables

    `confidence: simplesecurity.level.Level`
    :

    `description: str`
    :

    `evidence: str`
    :

    `file: str`
    :

    `line: str`
    :

    `severity: simplesecurity.level.Level`
    :

    `title: str`
    :