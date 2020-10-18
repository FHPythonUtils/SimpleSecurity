"""Levels for confidence and severity
UNKNOWN = 0
LOW = 1
MED = 2
HIGH = 3
"""
from enum import IntEnum


class Level(IntEnum):
	"""Levels for confidence and severity
	UNKNOWN = 0
	LOW = 1
	MED = 2
	HIGH = 3
	"""
	UNKNOWN = 0
	LOW = 1
	MED = 2
	HIGH = 3

	def __repr__(self) -> str:
		reprMap = {Level.UNKNOWN: "Unknown", Level.LOW: "Low", Level.MED: "Medium", Level.HIGH: "High"}
		return reprMap[self]

	def __str__(self) -> str:
		reprMap = {Level.UNKNOWN: "Unknown", Level.LOW: "Low", Level.MED: "Medium", Level.HIGH: "High"}
		return reprMap[self]

	def toSarif(self) -> str:
		""" Convert to sarif representation """
		reprMap = {Level.UNKNOWN: "note", Level.LOW: "warning", Level.MED: "warning", Level.HIGH: "error"}
		return reprMap[self]
