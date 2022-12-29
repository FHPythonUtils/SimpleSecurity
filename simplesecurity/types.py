"""Types used by simplesecurity.
"""
from __future__ import annotations

import typing

from simplesecurity.level import Level

# pylint: disable=too-few-public-methods


class Finding(typing.TypedDict):
    """Finding type"""

    id: str
    title: str
    description: str
    file: str
    evidence: list[Line]
    severity: Level
    confidence: Level
    line: int
    _other: dict[str, str]


class Line(typing.TypedDict):
    """Line type"""

    line: int
    content: str
    selected: bool
