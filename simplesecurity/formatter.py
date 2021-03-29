"""Take our findings dictionary and give things a pretty format.

finding dictionary

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

Formats

- markdown
- json
- csv
- ansi
"""
# pyright: reportConstantRedefinition=false
from __future__ import annotations

from csv import QUOTE_ALL, writer
from io import StringIO
from json import dumps
from typing import Optional

from simplesecurity.types import Finding, Line


def formatEvidence(evidence: list[Line], newlineChar: bool = True) -> str:
	"""Format evidence to plaintext.

	Args:
		evidence (list[Line]): list of lines of code
		newlineChar (bool, optional): use newline char. Defaults to true

	Returns:
		str: string representation of this
	"""
	evidenceText = [line["content"] for line in evidence]
	if newlineChar:
		return "\n".join(evidenceText)
	return "\\n".join(evidenceText)


def markdown(findings: list[Finding], heading: Optional[str] = None, colourMode: int = 0) -> str:
	"""Format to Markdown.

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	if len(findings) == 0:
		return "No findings"

	heading = (
		heading
		if heading is not None
		else "# Findings\nFind a list of findings below ordered by severity"
	)
	strBuf = [heading]
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)

	# Summary Table
	strBuf.append("")
	strBuf.append("|Severity|Finding|\n|:--|:--|")
	for finding in findings:
		strBuf.append(f"|{finding['severity']}|{finding['title']}|")
	strBuf.append("")

	# Details
	for finding in findings:
		strBuf.extend(
			[
				f"## {finding['title']}",
				f"{finding['description']}",
				f"\n\nFile: `{finding['file']}`",
				f"### Severity\n\n{finding['severity']} (confidence: {finding['confidence']})",
				f"### Evidence\n\nLine: {finding['line']}\n",
				f"```python\n{formatEvidence(finding['evidence'])}\n```",
			]
		)
	return "\n".join(strBuf) + "\n"


def json(findings: list[Finding], heading: Optional[str] = None, colourMode: int = 0) -> str:
	"""Format to Json.

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)
	out = {
		"heading": heading
		if heading is not None
		else "Findings - Findings below are ordered by severity",
		"findings": findings,
	}
	return dumps(out, indent="\t")


def csv(findings: list[Finding], heading: Optional[str] = None, colourMode: int = 0) -> str:
	"""Format to CSV.

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)
	output = StringIO()
	csvString = writer(output, quoting=QUOTE_ALL)
	csvString.writerow(
		[
			heading
			if heading is not None
			else "Findings - Findings below are ordered by severity (you may want to delete this line)"
		]
	)
	csvString.writerow(
		["id", "title", "description", "file", "evidence", "severity", "confidence", "line"]
	)
	for finding in findings:
		csvString.writerow(
			[
				finding["id"],
				finding["title"],
				finding["description"],
				finding["file"],
				formatEvidence(finding["evidence"], False),
				finding["severity"],
				finding["confidence"],
				finding["line"],
			]
		)
	return output.getvalue()


def ansi(findings: list[Finding], heading: Optional[str] = None, colourMode: int = 0) -> str:
	"""Format to ansi.

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	# pylint: disable=invalid-name
	FMT = {
		"TXT": "",
		"BLD": "",
		"CLS": "",
		"UL": "",
		"CB": "",
		"CG": "",
		"CY": "",
		"CODE": "│",
	}
	if colourMode == 1:
		FMT = {
			"TXT": "",
			"BLD": "\033[01m",
			"CLS": "\033[00m",
			"UL": "\033[04m",
			"CB": "\033[36m",
			"CG": "\033[32m",
			"CY": "\033[33m",
			"CODE": "│\033[100m\033[93m",
		}
	elif colourMode == 2:
		FMT = {
			"TXT": "\033[97m",
			"BLD": "\033[01m",
			"CLS": "\033[00m",
			"UL": "\033[04m",
			"CB": "\033[96m",
			"CG": "\033[92m",
			"CY": "\033[93m",
			"CODE": "\033[97m│\033[107m\033[90m",
		}
	if len(findings) == 0:
		return f"{FMT['BLD']}{FMT['UL']}{FMT['CB']}No findings{FMT['CLS']}"

	# pylint: enable=invalid-name
	strBuf = (
		[heading]
		if heading is not None
		else [
			f"{FMT['BLD']}{FMT['UL']}{FMT['CB']}Findings{FMT['CLS']}\n",
			f"{FMT['TXT']}Find a list of findings below ordered by severity\n",
		]
	)
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)

	# Summary Table
	strBuf.append(f"{FMT['TXT']}┌{'─'*10}┬{'─'*50}┐")
	strBuf.append("│Severity  │Finding                                           │")
	strBuf.append(f"├{'─'*10}┼{'─'*50}┤")
	for finding in findings:
		strBuf.append(f"│{finding['severity']: <10}│{finding['title'][:50]: <50}│")
	strBuf.append(f"└{'─'*10}┴{'─'*50}┘")
	strBuf.append("")

	# Details
	for finding in findings:
		evidence = [f"{FMT['TXT']}┌{' ' + finding['file'] + ' ':─^85}┐"]
		for line in finding["evidence"]:
			evidence.append(
				(FMT["CODE"] if line["selected"] else f"{FMT['TXT']}│")
				+ f"{str(line['line'])[:3]: >3}  "
				+ f"{line['content'][:80]: <80}{FMT['CLS']}{FMT['TXT']}│"
			)
		evidence.append(f"└{'─'*85}┘")
		evidenceStr = "\n".join(evidence)
		strBuf.extend(
			[
				f"{FMT['BLD']}{FMT['UL']}{FMT['CG']}{finding['title']}{FMT['CLS']}",
				f"{FMT['TXT']}{finding['description']}",
				f"\n{FMT['UL']}{FMT['CY']}Severity: {finding['severity']} "
				+ f"(confidence: {finding['confidence']}){FMT['CLS']}\n",
				f"{FMT['UL']}{FMT['CY']}Evidence{FMT['CLS']}\n{evidenceStr}\n",
			]
		)
	return "\n".join(strBuf) + f"{FMT['CLS']}"


def sarif(findings: list[Finding], heading: Optional[str] = None, colourMode: int = 0) -> str:
	"""Format to sarif https://sarifweb.azurewebsites.net/.

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	out = {
		"version": "2.1.0",
		"$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
		"runs": [
			{
				"tool": {
					"driver": {
						"name": "SimpleSecurity",
						"informationUri": "https://github.com/FHPythonUtils/SimpleSecurity",
						"version": "2020.*",
					}
				},
				"results": [
					{
						"ruleId": finding["id"],
						"level": finding["severity"].toSarif(),
						"message": {"text": f"{finding['title']}: {finding['description']}"},
						"locations": [
							{
								"physicalLocation": {
									"artifactLocation": {"uri": finding["file"]},
									"region": {
										"startLine": finding["line"],
										"snippet": {
											"text": "".join(
												[
													line["content"]
													for line in finding["evidence"]
													if line["selected"]
												]
											)
										},
									},
									"contextRegion": {
										"startLine": finding["evidence"][0]["line"],
										"endLine": finding["evidence"][-1]["line"],
										"snippet": {
											"text": "\n".join(
												[line["content"] for line in finding["evidence"]]
											)
										},
									},
								}
							}
						],
					}
					for finding in findings
				],
			}
		],
	}
	return dumps(out, indent="\t")
