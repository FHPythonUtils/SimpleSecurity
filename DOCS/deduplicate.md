Module simplesecurity.deduplicate
=================================
Some of our analysis tools overlap one-another so lets remove duplicates

Functions
---------

    
`deduplicate(findings: list[Finding]) ‑> list`
:   Deduplicate the list of findings
    
    Args:
            findings (list[Finding]): list of findings to deduplicate
    
    Returns:
            list[Finding]: new deduplicated list

    
`findingsEqual(findingA: Finding, findingB: Finding) ‑> int`
:   Basically and __eq__ method for findings
    
    Args:
            findingA (Finding): lhs
            findingB (Finding): rhs
    
    Returns:
            int: 0 if not equal. 1 if lookup(left) is equal to right - bin left.
            -1 if lookup(right) is equal to left - bin right

    
`lookupId(identifier: str) ‑> str`
:   Lookup an id in the id map
    
    Args:
            id (str): id to look up
    
    Returns:
            str: id that it equals