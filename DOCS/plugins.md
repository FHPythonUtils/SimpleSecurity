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
        evidence: str
        severity: Level
        confidence: Level
        line: str
        _other: {}
}
```

Functions
---------

    
`bandit() ‑> list`
:   Wrapper for bandit. requires bandit on the system path
    
    Raises:
            RuntimeError: if bandit is not on the system path, then throw this
            error
    
    Returns:
            list[dict]: our findings dictionary

    
`dlint() ‑> list`
:   Wrapper for dlint. requires flake8 and dlint on the system path
    
    Raises:
            RuntimeError: if flake8 is not on the system path, then throw this
            error
    
    Returns:
            list[dict]: our findings dictionary

    
`dodgy() ‑> list`
:   Wrapper for dodgy. requires dodgy on the system path
    
    Raises:
            RuntimeError: if dodgy is not on the system path, then throw this
            error
    
    Returns:
            list[dict]: our findings dictionary

    
`safety() ‑> list`
:   Wrapper for safety. requires poetry and safety on the system path
    
    Raises:
            RuntimeError: if saftey is not on the system path, then throw this
            error
    
    Returns:
            list[dict]: our findings dictionary