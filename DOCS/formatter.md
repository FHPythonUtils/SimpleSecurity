Module simplesecurity.formatter
===============================
Take our findings dictionary and give things a pretty format

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

Formats

- markdown
- json
- csv
- ansi

Functions
---------

    
`ansi(findings: list, heading: Optional[str] = None) ‑> str`
:   Format to ansi
    
    Args:
            findings (list[dict[str, str]]): Findings to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout

    
`csv(findings: list, heading: Optional[str] = None) ‑> str`
:   Format to CSV
    
    Args:
            findings (list[dict[str, str]]): Findings to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout

    
`json(findings: list, heading: Optional[str] = None) ‑> str`
:   Format to Json
    
    Args:
            findings (list[dict[str, str]]): Findings to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout

    
`markdown(findings: list, heading: Optional[str] = None) ‑> str`
:   Format to Markdown
    
    Args:
            findings (list[dict[str, str]]): Findings to format
            heading (str, optional): Optional heading to include. Defaults to None.
    
    Returns:
            str: String to write to a file of stdout