"""Add plugins here

- bandit
- safety
- dodgy
- dlint

Functions return finding dictionary

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

import subprocess
import warnings
from json import loads
from shlex import split
from simplesecurity.level import Level


def _doSysExec(command: str) -> tuple[int, str]:
	"""execute a command and check for errors
	shlex.split can be used to make this safer.
	see https://docs.python.org/3/library/shlex.html#shlex.quote
	Note however, that we can still call _doSysExec with a malicious command
	but this change mitigates command chaining. Ultimately, do not accept user
	input or if you do, escape with shlex.quote(), shlex.join(shlex.split())

	Args:
		command (str): commands as a string

	Raises:
		RuntimeWarning: throw a warning should there be a non exit code
	"""
	with subprocess.Popen(split(command), shell=True, stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT, universal_newlines=True) as process:
		out = process.communicate()[0]
		exitCode = process.returncode
	return exitCode, out


def bandit() -> list[dict]:
	"""Wrapper for bandit. requires bandit on the system path

	Raises:
		RuntimeError: if bandit is not on the system path, then throw this
		error

	Returns:
		list[dict]: our findings dictionary
	"""
	if _doSysExec("bandit -h")[0] != 0:
		raise RuntimeError("bandit is not on the system path")
	findings = []
	levelMap = {"LOW": Level.LOW, "MEDIUM": Level.MED, "HIGH": Level.HIGH,
	"UNDEFINED": Level.UNKNOWN} # yapf: disable
	results = loads(_doSysExec("bandit -lirq --exclude **/test_*.py -s B322 -f json .")
	[1])["results"] # yapf: disable
	for result in results:
		findings.append({"title": f"{result['test_id']}: {result['test_name']}",
		"description": result['issue_text'],
		"file": result['filename'].replace("\\", "/"),
		"evidence": result['code'].strip(),
		"severity": levelMap[result['issue_severity']],
		"confidence": levelMap[result['issue_confidence']],
		"line": result['line_number'],
		"_other": {"more_info": result['more_info'], "line_range": result['line_range']}}) # yapf: disable
	return findings


def safety() -> list[dict]:
	"""Wrapper for safety. requires poetry and safety on the system path

	Raises:
		RuntimeError: if saftey is not on the system path, then throw this
		error

	Returns:
		list[dict]: our findings dictionary
	"""
	poetryInstalled = True
	if _doSysExec("poetry -h")[0] != 0:
		poetryInstalled = False
		warnings.warn(RuntimeWarning("poetry is not on the system path"))
	if _doSysExec("safety --help")[0] != 0:
		raise RuntimeError("safety is not on the system path")
	findings = []
	if poetryInstalled:
		results = loads(_doSysExec("poetry export -f requirements.txt | safety check --stdin --json")
		[1]) # yapf: disable
	else:
		results = loads(_doSysExec("safety check --json")[1]) # yapf: disable
	for result in results:
		findings.append({"title": f"{result[4]}: {result[0]}",
		"description": result[3],
		"file": "Project Requirements",
		"evidence": f"{result[0]} version={result[2]} affects{result[1]}",
		"severity": Level.MED,
		"confidence": Level.HIGH,
		"line": "Unknown",
		"_other": {"id": result[4], "affected": result[1]}}) # yapf: disable
	return findings


def dodgy() -> list[dict]:
	"""Wrapper for dodgy. requires dodgy on the system path

	Raises:
		RuntimeError: if dodgy is not on the system path, then throw this
		error

	Returns:
		list[dict]: our findings dictionary
	"""
	if _doSysExec("dodgy -h")[0] != 0:
		raise RuntimeError("dodgy is not on the system path")
	findings = []
	results = loads(_doSysExec("dodgy")[1])["warnings"]
	for result in results:
		findings.append({"title": result["message"],
		"description": result["message"],
		"file": result["path"].replace("\\", "/"),
		"evidence": result["code"],
		"severity": Level.MED,
		"confidence": Level.MED,
		"line": result["line"],
		"_other": {}}) # yapf: disable
	return findings


def dlint() -> list[dict]:
	"""Wrapper for dlint. requires flake8 and dlint on the system path

	Raises:
		RuntimeError: if flake8 is not on the system path, then throw this
		error

	Returns:
		list[dict]: our findings dictionary
	"""
	if _doSysExec("flake8 -h")[0] != 0:
		raise RuntimeError("flake8 is not on the system path")
	findings = []
	results = _doSysExec("flake8 --select=DUO --format='%(path)s::%(row)d" +
	"::%(col)d::%(code)s::%(text)s' .")[1].splitlines(False)# yapf: disable
	for line in results:
		result = line.split("::")
		findings.append({"title": f"{result[3]}: {result[4]}",
		"description": result[4],
		"file": result[0].replace("\\", "/"),
		"evidence": "Unknown",
		"severity": Level.MED,
		"confidence": Level.MED,
		"line": result[1],
		"_other": {"col": result[2]}}) # yapf: disable
	return findings
