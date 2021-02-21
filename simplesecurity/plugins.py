"""Add plugins here

- bandit
- safety
- dodgy
- dlint
- pygraudit
- semgrep

Functions return finding dictionary

```json
{
	title: str
	description: str
	file: str
	evidence: list[Line]
	severity: Level
	confidence: Level
	line: int
	_other: {}
}
```
"""
from __future__ import annotations
from typing import Any
from os import remove
import platform
import subprocess
import warnings
from pathlib import Path
from json import loads
from simplesecurity.level import Level
from simplesecurity.types import Finding, Line

THISDIR = str(Path(__file__).resolve().parent)

def _doSysExec(command: str, errorAsOut: bool=True) -> tuple[int, str]:
	"""execute a command and check for errors

	Args:
		command (str): commands as a string
		errorAsOut (bool, optional): redirect errors to stdout

	Raises:
		RuntimeWarning: throw a warning should there be a non exit code
	"""
	with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT if errorAsOut else subprocess.PIPE,
	encoding="utf-8", errors="ignore") as process:
		out = process.communicate()[0]
		exitCode = process.returncode
	return exitCode, out


def extractEvidence(desiredLine: int, file: str) -> list[Line]:
	"""Grab evidence from the source file

	Args:
		desiredLine (int): line to highlight
		file (str): file to extract evidence from

	Returns:
		list[Line]: list of lines
	"""
	with open(file, "r", encoding="utf-8", errors="ignore") as fileContents:
		start, stop = max(desiredLine - 3, 0), min(desiredLine + 2,
		sum(1 for _i in open(file, 'rb')))
		for line in range(start):
			next(fileContents)
		content = []
		for line in range(start + 1, stop + 1):
			content.append({"selected": line==desiredLine,"line": line,
			"content": next(fileContents).rstrip().replace("\t", "    ")}) # yapf: disable
	return content


def bandit() -> list[Finding]:
	"""Wrapper for bandit. requires bandit on the system path

	Raises:
		RuntimeError: if bandit is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("bandit -h")[0] != 0:
		raise RuntimeError("bandit is not on the system path")
	findings = []
	levelMap = {"LOW": Level.LOW, "MEDIUM": Level.MED, "HIGH": Level.HIGH,
	"UNDEFINED": Level.UNKNOWN} # yapf: disable
	results = loads(
	_doSysExec("bandit -lirq --exclude **/test_*.py --exclude **/test.py -f json .", False)
	[1])["results"] # yapf: disable
	for result in results:
		file =result['filename'].replace("\\", "/")
		findings.append({"id": result['test_id'],
		"title": f"{result['test_id']}: {result['test_name']}",
		"description": result['issue_text'],
		"file": file,
		"evidence": extractEvidence(result["line_number"], file),
		"severity": levelMap[result['issue_severity']],
		"confidence": levelMap[result['issue_confidence']],
		"line": result['line_number'],
		"_other": {"more_info": result['more_info'], "line_range": result['line_range']}}) # yapf: disable
	return findings

def _doSafetyProcessing(results: dict[str, Any]) -> list[Finding]:
	findings = []
	for result in results:
		findings.append({"id": result[4],
		"title": f"{result[4]}: {result[0]}",
		"description": result[3],
		"file": "Project Requirements",
		"evidence": [{"selected": True, "line": 0,
		"content": f"{result[0]} version={result[2]} affects{result[1]}"}],
		"severity": Level.MED,
		"confidence": Level.HIGH,
		"line": "Unknown",
		"_other": {"id": result[4], "affected": result[1]}}) # yapf: disable
	return findings

def safety() -> list[Finding]:
	"""Wrapper for safety. requires poetry and safety on the system path

	Raises:
		RuntimeError: if saftey is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	poetryInstalled = True
	if _doSysExec("poetry -h")[0] != 0:
		poetryInstalled = False
		warnings.warn(RuntimeWarning("poetry is not on the system path"))
	if _doSysExec("safety --help")[0] != 0:
		raise RuntimeError("safety is not on the system path")
	if poetryInstalled:
		# Use poetry show to get dependents of dependencies
		lines = _doSysExec("poetry show")[1].splitlines(False)
		data = []
		for line in lines:
			parts = line.split()
			if len(parts) > 1:
				if "(!)" in parts[1] and len(parts) > 2:
					data.append(f"{parts[0]}=={parts[2]}")
				else:
					data.append(f"{parts[0]}=={parts[1]}")
			else:
				data.append(f"{parts[0]}")
		with open("reqs.txt", "w", encoding="utf-8", errors="ignore") as reqs:
			reqs.write("\n".join(data))
		results = loads(_doSysExec("safety check -r reqs.txt --json")[1])
		remove("reqs.txt")
	else:
		# Use plain old safety (this will miss optional dependencies)
		results = loads(_doSysExec("safety check --json")[1]) # yapf: disable
	return _doSafetyProcessing(results)


def safetyFast() -> list[Finding]:
	"""Wrapper for safety. requires safety on the system path

	Raises:
		RuntimeError: if saftey is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("safety --help")[0] != 0:
		raise RuntimeError("safety is not on the system path")
	# Use plain old safety (this will miss optional dependencies)
	results = loads(_doSysExec("safety check --json")[1]) # yapf: disable
	return _doSafetyProcessing(results)



def dodgy() -> list[Finding]:
	"""Wrapper for dodgy. requires dodgy on the system path

	Raises:
		RuntimeError: if dodgy is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("dodgy -h")[0] != 0:
		raise RuntimeError("dodgy is not on the system path")
	findings = []
	results = loads(_doSysExec("dodgy")[1])["warnings"]
	for result in results:
		file = "./" + result["path"].replace("\\", "/")
		findings.append({"id": result['code'],
		"title": result["message"],
		"description": result["message"],
		"file": file,
		"evidence": extractEvidence(result["line"], file),
		"severity": Level.MED,
		"confidence": Level.MED,
		"line": result["line"],
		"_other": {}}) # yapf: disable
	return findings


def dlint() -> list[Finding]:
	"""Wrapper for dlint. requires flake8 and dlint on the system path

	Raises:
		RuntimeError: if flake8 is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("flake8 -h")[0] != 0:
		raise RuntimeError("flake8 is not on the system path")
	findings = []
	results = _doSysExec("flake8 --select=DUO --format='%(path)s::%(row)d" +
	"::%(col)d::%(code)s::%(text)s' .")[1].splitlines(False)# yapf: disable
	for line in results:
		if line[0] == "'":
			line = line[1:-1]
		result = line.split("::")
		file = result[0].replace("\\", "/")
		findings.append({"id": result[3],
		"title": f"{result[3]}: {result[4]}",
		"description": result[4],
		"file": file,
		"evidence": extractEvidence(int(result[1]), file),
		"severity": Level.MED,
		"confidence": Level.MED,
		"line": int(result[1]),
		"_other": {"col": result[2]}}) # yapf: disable
	return findings


def pygraudit() -> list[Finding]:
	"""Wrapper for pygraudit. requires pygraudit on the system path

	Raises:
		RuntimeError: if pygraudit is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("pygraudit -h")[0] != 0:
		raise RuntimeError("pygraudit is not on the system path")
	findings = []
	results = loads(_doSysExec("pygraudit -B -f json .")[1])["findings"]
	for result in results:
		findings.append({"id": result['id'],
		"title": f"{result['id']}: {result['title']}",
		"description": result['title'],
		"file": result['file'],
		"evidence": result["evidence"],
		# The python database isn't the best tbh but the end user may want very
		# verbose output
		"severity": Level.LOW,
		"confidence": Level.LOW,
		"line": result['line'],
		"_other": {"col": result['col']}}) # yapf: disable
	return findings

def semgrep() -> list[Finding]:
	"""Wrapper for semgrep. requires semgrep on the system path (wsl in windows)

	Raises:
		RuntimeError: if semgrep is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	findings = []
	prepend = "wsl " if platform.system() == "Windows" else ""
	if _doSysExec(prepend + "semgrep -h")[0] != 0:
		if platform.system() == "Windows":
			raise RuntimeError("semgrep is not installed in wsl")
		raise RuntimeError("semgrep is not on the system path")
	directory = THISDIR.replace("\\", "/").replace("C:", "/mnt/c")
	results = loads(_doSysExec(prepend + "semgrep -f " + directory +
	"/semgrep_sec.yaml -q --json --no-rewrite-rule-ids")[1])["results"] # yapf: disable
	levelMap = {"INFO": Level.LOW, "WARNING": Level.MED, "ERROR": Level.HIGH}
	for result in results:
		file = "./" + result["path"].replace("\\", "/")
		findings.append({"id": result['check_id'],
		"title": result['check_id'].split(".")[-1],
		"description": result["extra"]["message"].strip(),
		"file": file,
		"evidence": extractEvidence(result["start"]["line"], file),
		"severity": levelMap[result["extra"]["severity"]],
		"confidence": Level.HIGH,
		"line": result["start"]["line"],
		"_other": {"col": result["start"]["col"], "start": result["start"],
		"end": result["end"], "extra": result["extra"]}}) # yapf: disable
	return findings
