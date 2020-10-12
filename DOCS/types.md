Module simplesecurity.types
===========================
Types used by simplesecurity

Classes
-------

`Finding(*args, **kwargs)`
:   Finding type
    
    {
            title: str
            description: str
            file: str
            evidence: list[Line]
            severity: Level
            confidence: Level
            line: int
            _other: {}
    }

    ### Ancestors (in MRO)

    * builtins.dict

    ### Class variables

    `confidence: simplesecurity.level.Level`
    :

    `description: str`
    :

    `evidence: list`
    :

    `file: str`
    :

    `line: int`
    :

    `severity: simplesecurity.level.Level`
    :

    `title: str`
    :

`Line(*args, **kwargs)`
:   Line type
    
    {
            line: int
            content: str
            selected: bool
    }

    ### Ancestors (in MRO)

    * builtins.dict

    ### Class variables

    `content: str`
    :

    `line: int`
    :

    `selected: bool`
    :