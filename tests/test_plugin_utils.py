import sys
from pathlib import Path

from simplesecurity import level, plugins

THISDIR = str(Path(__file__).resolve().parent)

evidence = f"{THISDIR}/data/evidence.txt"
evidenceBig = f"{THISDIR}/data/evidence_big.txt"


def test_doSysExec_ls():
	ls = "ls"
	if "win" in sys.platform.lower():
		ls = "dir"
	assert plugins._doSysExec(f"{ls} {THISDIR}")[0] == 0


def test_doSysExec_commandnotexists():
	assert plugins._doSysExec("commandnotexists")[0] != 0


def test_extractEvidence_1line():
	compare = [
		{"content": "Lorem", "line": 1, "selected": True},
		{"content": "ipsum", "line": 2, "selected": False},
		{"content": "dolor", "line": 3, "selected": False},
	]
	assert plugins.extractEvidence(1, evidence) == compare


def test_extractEvidence_5line():
	compare = [
		{"content": "Lorem", "line": 1, "selected": False},
		{"content": "ipsum", "line": 2, "selected": False},
		{"content": "dolor", "line": 3, "selected": True},
		{"content": "sit", "line": 4, "selected": False},
		{"content": "amet,", "line": 5, "selected": False},
	]
	assert plugins.extractEvidence(3, evidence) == compare


def test_extractEvidence_line_notinfile_lower():
	compare = [
		{"content": "Lorem", "line": 1, "selected": False},
		{"content": "ipsum", "line": 2, "selected": False},
	]
	assert plugins.extractEvidence(0, evidence) == compare


def test_extractEvidence_line_notinfile_upper():
	compare = [
		{"content": "Nulla", "line": 18, "selected": False},
		{"content": "ut", "line": 19, "selected": False},
		{"content": "lectus.", "line": 20, "selected": True},
	]
	assert plugins.extractEvidence(20, evidence) == compare


def test__doSafetyProcessing():
	safety = {
		"vulnerabilities": [
			{
				"vulnerability_id": "44742",
				"package_name": "django",
				"ignored": False,
				"ignored_reason": None,
				"ignored_expires": None,
				"vulnerable_spec": ">=4.0a1,<4.0.2",
				"all_vulnerable_specs": [">=4.0a1,<4.0.2"],
				"analyzed_version": "4.0.1",
				"analyzed_requirement": {
					"raw": "django==4.0.1",
					"extras": [],
					"marker": None,
					"name": "django",
					"specifier": "==4.0.1",
					"url": None,
					"found": None,
				},
				"advisory": "The {% debug %} template tag in Django",
				"is_transitive": False,
				"published_date": "2022-Feb-03",
				"fixed_versions": ["2.2.27", "3.2.12", "4.0.2"],
				"closest_versions_without_known_vulnerabilities": [],
				"resources": ["https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-22818"],
				"CVE": "CVE-2022-22818",
				"severity": {
					"source": "CVE-2022-22818",
					"cvssv2": {
						"base_score": 4.3,
						"impact_score": 2.9,
						"vector_string": "AV:N/AC:M/Au:N/C:N/I:P/A:N",
					},
					"cvssv3": {
						"base_score": 6.1,
						"impact_score": 2.7,
						"base_severity": "MEDIUM",
						"vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
					},
				},
				"affected_versions": [
					"4.0.1",
				],
				"more_info_url": "https://pyup.io/vulnerabilities/CVE-2022-22818/44742/",
			},
		],
	}
	findings = [
		{
			"id": "44742",
			"title": "44742: django",
			"description": (
				"Vulnerability found in package django,"
				"version(s)=4.0.1. The {% debug %} template tag in Django. More info available at https://pyup.io/vulnerabilities/CVE-2022-22818/44742/"
			),
			"file": "Project Requirements",
			"evidence": [
				{
					"selected": True,
					"line": 0,
					"content": "django, version(s)=4.0.1",
				}
			],
			"severity": level.Level.MED,
			"confidence": level.Level.HIGH,
			"line": "Unknown",
			"_other": {"id": "44742", "affectedVersions": "4.0.1"},
		}
	]
	assert plugins._doSafetyProcessing(safety) == findings
