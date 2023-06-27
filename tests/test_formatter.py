import json
from pathlib import Path

from jsonschema import validate
from simplesecurity import formatter, level, types

THISDIR = str(Path(__file__).resolve().parent)

sarifSchema = json.loads(Path(f"{THISDIR}/data/sarif-schema-2.1.0.json").read_text("utf-8"))
simpleFindings: list[types.Finding] = [{
	"id": "TEST_ID",
	"title": "TEST",
	"description": "This is a test",
	"file": "this_file_does_not_exist",
	"evidence": [{"selected": True, "line": 0, "content": "lineContent"}],
	"severity": level.Level.MED,
	"confidence": level.Level.MED,
	"line": 0,
	"_other": {},

}]

advancedFindings: list[types.Finding] = [{
	"id": "TEST_ID",
	"title": "TEST",
	"description": "This is a test",
	"file": "this_file_does_not_exist",
	"evidence": [{"selected": True, "line": 0, "content": "lineContent"}],
	"severity": level.Level.MED,
	"confidence": level.Level.MED,
	"line": 0,
	"_other": {},
}, {
	"id": "TEST_ID2",
	"title": "TEST2",
	"description": "This is a test2",
	"file": "this_file_does_not_exist2",
	"evidence": [
		{"selected": False, "line": 3, "content": "3"},
		{"selected": True, "line": 5, "content": "5"},
		{"selected": True, "line": 9, "content": "9"},
		{"selected": True, "line": 99, "content": "999999999999999999999999999999999"},
		  ],
	"severity": level.Level.LOW,
	"confidence": level.Level.HIGH,
	"line": 700,
	"_other": {},
}

]

def test_simpleMarkdown():
	fmt = formatter.markdown(simpleFindings)
	# Path(f"{THISDIR}/data/simple.md").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.md").read_text("utf-8")

def test_simpleAnsi():
	fmt = formatter.ansi(simpleFindings)
	# Path(f"{THISDIR}/data/simple.ansi").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.ansi").read_text("utf-8")

def test_simpleJson():
	fmt = formatter.json(simpleFindings)
	# Path(f"{THISDIR}/data/simple.json").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.json").read_text("utf-8")


def test_simpleCsv():
	fmt = formatter.csv(simpleFindings)
	# Path(f"{THISDIR}/data/simple.csv").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.csv").read_text("utf-8")

def test_simpleSarif():
	fmt = formatter.sarif(simpleFindings)
	Path(f"{THISDIR}/data/simple.sarif").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/simple.sarif").read_text("utf-8")
	assert validate(json.loads(fmt), sarifSchema) is None


def test_advancedMarkdown():
	fmt = formatter.markdown(advancedFindings)
	# Path(f"{THISDIR}/data/advanced.md").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.md").read_text("utf-8")

def test_advancedAnsi():
	fmt = formatter.ansi(advancedFindings)
	# Path(f"{THISDIR}/data/advanced.ansi").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.ansi").read_text("utf-8")

def test_advancedJson():
	fmt = formatter.json(advancedFindings)
	# Path(f"{THISDIR}/data/advanced.json").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.json").read_text("utf-8")


def test_advancedCsv():
	fmt = formatter.csv(advancedFindings)
	# Path(f"{THISDIR}/data/advanced.csv").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.csv").read_text("utf-8")

def test_advancedSarif():
	fmt = formatter.sarif(advancedFindings)
	Path(f"{THISDIR}/data/advanced.sarif").write_text(fmt, "utf-8")
	assert fmt == Path(f"{THISDIR}/data/advanced.sarif").read_text("utf-8")
	assert validate(json.loads(fmt), sarifSchema) is None
