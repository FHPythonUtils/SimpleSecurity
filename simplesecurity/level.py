"""Levels for confidence and severity.

UNKNOWN = 0
LOW = 1
MED = 2
HIGH = 3
"""
from __future__ import annotations

from enum import IntEnum


class Level(IntEnum):
	"""Levels for confidence and severity."""

	UNKNOWN = 0
	LOW = 1
	MED = 2
	HIGH = 3
	CRIT = 4

	def __repr__(self) -> str:
		"""__repr__ method.

		Returns:
			str: string representation of a level
		"""
		return self.__str__()

	def __str__(self) -> str:
		"""__str__ method (tostring).

		Returns:
			str: string representation of a level
		"""
		reprMap = {
			Level.UNKNOWN: "Unknown",
			Level.LOW: "Low",
			Level.MED: "Medium",
			Level.HIGH: "High",
			Level.CRIT: "Critical",
		}
		return reprMap[self]

	def toSarif(self) -> str:
		"""Convert to sarif representation."""
		reprMap = {
			Level.UNKNOWN: "note",
			Level.LOW: "note",
			Level.MED: "warning",
			Level.HIGH: "error",
			Level.CRIT: "error",
		}
		return reprMap[self]
