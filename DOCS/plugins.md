Module simplesecurity.plugins
=============================
Add plugins here

- bandit
- safety
- dodgy
- dlint

Functions return finding dictionary

```json
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

Functions
---------

    
`bandit() ‑> list`
:   Wrapper for bandit. requires bandit on the system path
    
    Raises:
            RuntimeError: if bandit is not on the system path, then throw this
            error
    
    Returns:
            list[Finding]: our findings dictionary

    
`dlint() ‑> list`
:   Wrapper for dlint. requires flake8 and dlint on the system path
    
    Raises:
            RuntimeError: if flake8 is not on the system path, then throw this
            error
    
    Returns:
            list[Finding]: our findings dictionary

    
`dodgy() ‑> list`
:   Wrapper for dodgy. requires dodgy on the system path
    
    Raises:
            RuntimeError: if dodgy is not on the system path, then throw this
            error
    
    Returns:
            list[Finding]: our findings dictionary

    
`extractEvidence(desiredLine: int, file: str) ‑> list`
:   Grab evidence from the source file
    
    Args:
            desiredLine (int): line to highlight
            file (str): file to extract evidence from
    
    Returns:
            list[Line]: list of lines

    
`safety() ‑> list`
:   Wrapper for safety. requires poetry and safety on the system path
    
    Raises:
            RuntimeError: if saftey is not on the system path, then throw this
            error
    
    Returns:
            list[Finding]: our findings dictionary