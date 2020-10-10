"""
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

"""

from __future__ import annotations
import typing
from simplesecurity.level import Level

class Finding(typing.TypedDict):
	"""Finding type
	"""
	title: str
	description: str
	file: str
	evidence: str
	severity: Level
	confidence: Level
	line: str
	_other: dict[str, str]
