"""Add plugins here.

- bandit
- safety
- dodgy
- dlint
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
	_other: dict[str, str]
}
```
"""
from __future__ import annotations

import platform
import subprocess
from json import loads
from os import remove
from pathlib import Path
from typing import Any

from simplesecurity.excluded import EXCLUDED
from simplesecurity.level import Level
from simplesecurity.types import Finding, Line

THISDIR = str(Path(__file__).resolve().parent)


def _doSysExec(command: str, errorAsOut: bool = True) -> tuple[int, str]:
	"""Execute a command and check for errors.

	Args:
			command (str): commands as a string
			errorAsOut (bool, optional): redirect errors to stdout

	Raises:
			RuntimeWarning: throw a warning should there be a non exit code

	Returns:
			tuple[int, str]: tuple of return code (int) and stdout (str)
	"""
	with subprocess.Popen(
		command,
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT if errorAsOut else subprocess.PIPE,
		encoding="utf-8",
		errors="ignore",
	) as process:
		out = process.communicate()[0]
		exitCode = process.returncode
	return exitCode, out


def extractEvidence(desiredLine: int, file: str) -> list[Line]:
	"""Grab evidence from the source file.

	Args:
		desiredLine (int): line to highlight
		file (str): file to extract evidence from

	Returns:
		list[Line]: list of lines
	"""
	with open(file, encoding="utf-8", errors="ignore") as fileContents:
		start = max(desiredLine - 3, 0)
		content = []
		try:
			for line in range(start):
				next(fileContents)
			for line in range(start + 1, desiredLine + 3):
				lineContent = next(fileContents).rstrip().replace("\t", "    ")
				content.append(
					{"selected": line == desiredLine, "line": line, "content": lineContent}
				)
		except StopIteration:
			pass
	return content


def bandit(scanDir=".") -> list[Finding]:
	"""Generate list of findings using bandit. requires bandit on the system path.

	Params:
		scanDir(str): select a scan directory (useful for cicd etc)

	Raises:
		RuntimeError: if bandit is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("bandit -h")[0] != 0:
		raise RuntimeError("bandit is not on the system path")
	findings = []
	levelMap = {
		"LOW": Level.LOW,
		"MEDIUM": Level.MED,
		"HIGH": Level.HIGH,
		"UNDEFINED": Level.UNKNOWN,
	}
	results = loads(
		_doSysExec(
			f"bandit -lirq -x {','.join([f'./{x}' for x in EXCLUDED])} -f json {scanDir}", False
		)[1]
	)["results"]
	for result in results:
		file = result.get("filename").replace("\\", "/")
		resultId = result.get("test_id")
		line = result.get("line_number")
		findings.append(
			{
				"id": resultId,
				"title": f"{resultId}: {result.get('test_name')}",
				"description": result.get("issue_text"),
				"file": file,
				"evidence": extractEvidence(line, file),
				"severity": levelMap[result.get("issue_severity")],
				"confidence": levelMap[result.get("issue_confidence")],
				"line": line,
				"_other": {
					"more_info": result.get("more_info"),
					"line_range": result.get("line_range"),
				},
			}
		)
	return findings


def _doSafetyProcessing(results: dict[str, Any]) -> list[Finding]:
	findings = []
	for result in results["vulnerabilities"]:
		vulnerabilityId = result.get("vulnerability_id")
		packageName = result.get("package_name")
		advisory = result.get("advisory")

		moreInfo = result.get("more_info_url")
		affectedVersions = "; ".join(result.get("affected_versions"))

		content = f"{packageName}, version(s)={affectedVersions}"
		description = (
			f"Vulnerability found in package {packageName},"
			f"version(s)={affectedVersions}. {advisory}. More info available at {moreInfo}"
		)

		cvssv3Score = result.get("severity").get("cvssv3", {}).get("base_score", 0)
		severity = Level.LOW
		if cvssv3Score > 3.9:
			severity = Level.MED
		if cvssv3Score > 6.9:
			severity = Level.HIGH
		if cvssv3Score > 8.9:
			severity = Level.CRIT

		findings.append(
			{
				"id": vulnerabilityId,
				"title": f"{vulnerabilityId}: {packageName}",
				"description": description,
				"file": "Project Requirements",
				"evidence": [
					{
						"selected": True,
						"line": 0,
						"content": content,
					}
				],
				"severity": severity,
				"confidence": Level.HIGH,
				"line": "Unknown",
				"_other": {"id": vulnerabilityId, "affectedVersions": affectedVersions},
			}
		)
	return findings


def _doPureSafety() -> dict[str, Any]:
	safe = _doSysExec("safety check -r requirements.txt --json")[1]
	if safe.startswith("Warning:"):
		safe = _doSysExec("safety check --json")[1]
		if safe.startswith("Warning:"):
			raise RuntimeError("some error occurred: " + safe)
	return loads(safe)


def safety(scanDir=".") -> list[Finding]:
	"""Generate list of findings using _tool_. requires _tool_ on the system path.

	Params:
		scanDir(str): select a scan directory (useful for cicd etc)

	Raises:
		RuntimeError: if safety is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	_ = scanDir
	if _doSysExec("safety --help")[0] != 0:
		raise RuntimeError("safety is not on the system path")
	pShow = _doSysExec("poetry show")
	if not pShow[0]:
		lines = pShow[1].splitlines(False)
		data = []
		for line in lines:
			parts = line.replace("(!)", "").split()
			if len(parts) > 1:
				data.append(f"{parts[0]}=={parts[1]}")
			else:
				data.append(f"{parts[0]}")
		with open("reqs.txt", "w", encoding="utf-8", errors="ignore") as reqs:
			reqs.write("\n".join(data))
		results = loads(_doSysExec("safety check -r reqs.txt --json")[1])
		remove("reqs.txt")
	elif not _doSysExec("pipreqs --savepath reqs.txt --encoding utf-8")[0]:
		results = loads(_doSysExec("safety check -r reqs.txt --json")[1])
		remove("reqs.txt")
	else:
		# Use plain old safety (this will miss optional dependencies)
		results = _doPureSafety()
	return _doSafetyProcessing(results)


def dodgy(scanDir=".") -> list[Finding]:
	"""Generate list of findings using _tool_. requires _tool_ on the system path.

	Params:
		scanDir(str): select a scan directory (useful for cicd etc)

	Raises:
		RuntimeError: if dodgy is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("dodgy -h")[0] != 0:
		raise RuntimeError("dodgy is not on the system path")
	findings = []
	rawResults = _doSysExec(f"dodgy {scanDir} -i {' '.join(EXCLUDED)}")[1]
	results = loads(rawResults)["warnings"]
	for result in results:
		file = "./" + result.get("path").replace("\\", "/")
		message = result.get("message")
		findings.append(
			{
				"id": result.get("code"),
				"title": message,
				"description": message,
				"file": file,
				"evidence": extractEvidence(result.get("line"), file),
				"severity": Level.MED,
				"confidence": Level.MED,
				"line": result.get("line"),
				"_other": {},
			}
		)
	return findings


def dlint(scanDir=".") -> list[Finding]:
	"""Generate list of findings using _tool_. requires _tool_ on the system path.

	Params:
		scanDir(str): select a scan directory (useful for cicd etc)

	Raises:
		RuntimeError: if flake8 is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	if _doSysExec("flake8 -h")[0] != 0:
		raise RuntimeError("flake8 is not on the system path")
	findings = []
	results = _doSysExec(
		f"flake8 --select=DUO --exclude {','.join(EXCLUDED)} --format=codeclimate {scanDir}"
	)[1].splitlines(False)

	jsonResults = loads("".join(results)) if len(results) > 0 else {}
	levelMap = {
		"info": Level.LOW,
		"minor": Level.MED,
		"major": Level.MED,
		"critical": Level.CRIT,
		"blocker": Level.CRIT,
	}
	for filePath, scanResults in jsonResults.items():
		for result in scanResults:
			message = f"{result.get('check_name')}: " f"{result.get('description')}"
			positions = result.get("location", {}).get("positions", {})
			line = positions.get("begin", {}).get("line", 0)
			findings.append(
				{
					"id": result.get("check_name"),
					"title": message,
					"description": message,
					"file": filePath,
					"evidence": extractEvidence(
						line,
						filePath,
					),
					"severity": levelMap[result.get("severity")],
					"confidence": Level.MED,
					"line": line,
					"_other": {
						"start": line,
						"end": positions.get("end", {}).get("line", 0),
						"fingerprint": result.get("fingerprint"),
					},
				}
			)

	return findings


def semgrep(scanDir=".") -> list[Finding]:
	"""Generate list of findings using for semgrep. Requires semgrep on the
	system path (wsl in windows).

	Raises:
		RuntimeError: if semgrep is not on the system path, then throw this
		error

	Returns:
		list[Finding]: our findings dictionary
	"""
	findings = []
	if platform.system() == "Windows":
		raise RuntimeError("semgrep is not supported on windows")
	if _doSysExec("semgrep --help")[0] != 0:
		raise RuntimeError("semgrep is not on the system path")
	sgExclude = ["--exclude {x}" for x in EXCLUDED]
	results = loads(
		_doSysExec(
			f"semgrep -f {THISDIR}/semgrep_sec.yaml {scanDir} {' '.join(sgExclude)} "
			"-q --json --no-rewrite-rule-ids"
		)[1].strip()
	)["results"]
	levelMap = {"INFO": Level.LOW, "WARNING": Level.MED, "ERROR": Level.HIGH}
	for result in results:
		filePath = result.get("Target").replace("\\", "/")
		file = f"{scanDir}/{filePath}"
		resultId = result.get("check_id", "")
		extras = result.get("extra", {})
		line = result.get("start", {}).get("line", 0)
		findings.append(
			{
				"id": resultId,
				"title": resultId.split(".")[-1],
				"description": extras("message").strip(),
				"file": file,
				"evidence": extractEvidence(line, file),
				"severity": levelMap[extras("severity")],
				"confidence": Level.HIGH,
				"line": line,
				"_other": {
					"end": result.get("end"),
					"extra": extras,
				},
			}
		)
	return findings
