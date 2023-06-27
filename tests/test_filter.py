from pathlib import Path

from simplesecurity import filter, level, types

THISDIR = str(Path(__file__).resolve().parent)

finding: types.Finding = {
	"id": "TEST_ID",
	"title": "TEST",
	"description": "This is a test",
	"file": "this_file_does_not_exist",
	"evidence": [{"selected": True, "line": 0, "content": "lineContent"}],
	"severity": level.Level.MED,
	"confidence": level.Level.MED,
	"line": 0,
	"_other": {},
}

simpleFindings: list[types.Finding] = [
	finding.copy(),
]


def test_lookupId_exists():
	# "DUO105": ["B102"]
	assert filter.lookupId("DUO105") == ["B102"]


def test_lookupId_notexists():
	# "DUO105": ["B102"]
	assert filter.lookupId("not_exists") == ["not_exists"]


def test_findingsEqual_true():
	findingA = finding.copy()
	findingB = finding.copy()
	assert filter.findingsEqual(findingA, findingB) == 1


def test_findingsEqual_false_file():
	findingA = finding.copy()
	findingB = finding.copy()
	findingB["file"] = "this_file_also_does_not_exist"
	assert filter.findingsEqual(findingA, findingB) == 0


def test_findingsEqual_false_line():
	findingA = finding.copy()
	findingB = finding.copy()
	findingB["line"] = 1
	assert filter.findingsEqual(findingA, findingB) == 0


def test_findingsEqual_false_id():
	findingA = finding.copy()
	findingB = finding.copy()
	findingB["id"] = "ANOTHER_TEST_ID"
	assert filter.findingsEqual(findingA, findingB) == 0


def test_deduplicate():
	assert filter.deduplicate([finding.copy(), finding.copy()]) == simpleFindings


def test_filterConfidence_2():
	findingA = finding.copy()
	findingA["confidence"] = level.Level.UNKNOWN
	findingB = finding.copy()
	findingB["confidence"] = level.Level.LOW
	findingC = finding.copy()
	findingC["confidence"] = level.Level.MED
	findingD = finding.copy()
	findingD["confidence"] = level.Level.HIGH
	findingE = finding.copy()
	findingE["confidence"] = level.Level.CRIT
	assert (
		len(
			filter.filterSeverityAndConfidence(
				[findingA, findingB, findingC, findingD, findingE], 0, 2
			)
		)
		== 3
	)


def test_filterSeverity_4():
	findingA = finding.copy()
	findingA["severity"] = level.Level.UNKNOWN
	findingB = finding.copy()
	findingB["severity"] = level.Level.LOW
	findingC = finding.copy()
	findingC["severity"] = level.Level.MED
	findingD = finding.copy()
	findingD["severity"] = level.Level.HIGH
	findingE = finding.copy()
	findingE["severity"] = level.Level.CRIT
	assert (
		len(
			filter.filterSeverityAndConfidence(
				[findingA, findingB, findingC, findingD, findingE], 4, 0
			)
		)
		== 1
	)
