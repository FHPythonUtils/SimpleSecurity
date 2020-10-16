"""Some of our analysis tools overlap one-another so lets remove duplicates
"""
from __future__ import annotations

from simplesecurity.types import Finding

ID_MAP = {
	"DUO105": ["B102"], # use of exec
	"DUO109": ["B506"], # use of yaml.load
	"DUO116": ["B602", "subprocess-shell-true"], # use of shell=True in subprocess
	"B602": ["subprocess-shell-true"],
	"DUO103": ["B402"], # use of pickle
	"DUO120": ["B302"], # use of marshal
	"DUO121": ["B306"], # use of mktemp
	"DUO104": ["B307"], # use of eval
	"DUO102": ["B311"], # use of random
	"DUO108": ["B322"], # use of input, py<3
	"DUO133": ["B413"], # use of pycrypto
} # yapf: disable


def lookupId(identifier: str) -> str:
	"""Lookup an id in the id map

	Args:
		id (str): id to look up

	Returns:
		str: id that it equals
	"""
	if identifier not in ID_MAP:
		return "not found"
	return ID_MAP[identifier]


def findingsEqual(findingA: Finding, findingB: Finding) -> int:
	"""Basically and __eq__ method for findings

	Args:
		findingA (Finding): lhs
		findingB (Finding): rhs

	Returns:
		int: 0 if not equal. 1 if lookup(left) is equal to right - bin left.
		-1 if lookup(right) is equal to left - bin right
	"""
	if (findingA["file"].replace("./", "") == findingB["file"].replace(
	"./", "") and findingA["line"] == findingB["line"]):
		if findingB["id"] in lookupId(findingA["id"]):
			return 1
		if findingA["id"] in lookupId(findingB["id"]):
			return -1
	return 0


def deduplicate(findings: list[Finding]) -> list[Finding]:
	"""Deduplicate the list of findings

	Args:
		findings (list[Finding]): list of findings to deduplicate

	Returns:
		list[Finding]: new deduplicated list
	"""
	findings = findings.copy()
	for indexA, findingA in enumerate(findings):
		for _indexB, findingB in enumerate(findings[indexA+1:]):
			equal = findingsEqual(findingA, findingB)
			if equal == 1: # lookup(left) is equal to right - bin left.
				findings.remove(findingA)
			elif equal == -1: # lookup(right) is equal to left - bin right.
				findings.remove(findingB)
	return findings


def filterSeverityAndConfidence(findings: list[Finding], severity: int,
confidence: int) -> list[Finding]:
	"""filters the list of findings

	Args:
		findings (list[Finding]): list of findings to
		severity (int): min severity
		confidence (int): min confidence

	Returns:
		list[Finding]: new deduplicated list
	"""
	if severity == 0 and confidence == 0:
		return findings
	findings = findings.copy()
	for finding in findings:
		if finding["severity"] < severity or finding["confidence"] < confidence:
			findings.remove(finding)
	return findings
