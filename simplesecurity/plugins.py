"""Plugins are modules that kick-off a particular scanner and return the
results as a findings object. The structure of the findings object is shown
below:

.. highlight:: python
.. code-block:: python

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

"""
from __future__ import annotations

import platform
import subprocess
from json import loads
from pathlib import Path
from typing import Any, Dict, List, Type

from simplesecurity.level import Level
from simplesecurity.types import Finding, Line

THISDIR = str(Path(__file__).resolve().parent)

EXCLUDED = [
    "./.env",
    "./tests",
    "./.venv",
    "./env/",
    "./venv/",
    "./ENV/",
    "./env.bak/",
    "./venv.bak/",
]


def _doSysExec(command: str, errorAsOut: bool = True) -> tuple[int, str]:
    """Helper function for executing commandline commands.

    :raises:  RuntimeWarning: throw a warning should there be a non exit code
    :param: commands as a string
    :param: optional, redirect errors to stdout
    :return: tuple of return code (int) and stdout (str)

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


def stringMatchesinFile(file: str, pattern: str) -> list:
    """Search for the given string in file and return lines containing that
    string, along with line numbers.

    :param str file: string that outlines the exact line or keyword that should be scanned.
    :param str pattern: string that provides the keyword for the search
    :return list: returns a list of matches

    """
    line_number = 0
    list_of_results = []
    with open(file, "r") as read_obj:
        for line in read_obj:
            line_number += 1
            if pattern in line:
                list_of_results.append(line_number)
    return list_of_results


def extractEvidence(LineNrOrWord: int | str, file: str) -> dict:
    """Grab evidence from the source file.

    :param LineNrOrWord: This can be an integer or string that outlines the exact line or keyword that should be scanned.
    :param file: A string that point to the file that should be interrogated for annotation
    :return: This function returns a dictionary that contains the line_nrs of where the matches were found, and content, that shows the bodies of text where the matches were found in.

    """
    results = {}
    if type(LineNrOrWord) == str:
        line_nrs = stringMatchesinFile(file=file, pattern=LineNrOrWord)
    elif type(LineNrOrWord) == int:
        line_nrs = [LineNrOrWord]

    content = []
    for line_nr in line_nrs:
        with open(file, encoding="utf-8", errors="ignore") as fileContents:
            start = max(line_nr - 3, 0)
            for line in range(start):
                next(fileContents)
            # content = []
            for line in range(start + 1, line_nr + 3):
                try:
                    lineContent = (
                        next(fileContents).rstrip().replace("\t", "    ")
                    )
                except StopIteration:
                    break
                content.append(
                    {
                        "selected": line == line_nr,
                        "line": line,
                        "content": lineContent,
                    }
                )

    if len(content) > 20:
        matches = f"Found many more matches: {len(line_nrs)}, cut-off printout to 20 items \n consult line_nrs for full trace"
        content = content[0:20]
        content.append({"selected": True, "line": 99999, "content": matches})
    return {"line_nrs": line_nrs, "content": content}


def bandit(scan_dir: str) -> list[dict]:
    """bandit plugin for generating list of findings using for bandit. Requires
    bandit on the system path.

    :raises: RuntimeError: if bandit is not on the system path, then throw this error
    :param scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: returns structured list of findings, if there are any

    """
    if _doSysExec("bandit -h")[0] != 0:
        raise RuntimeError("bandit is not on the system path")
    findings: Finding = []
    levelMap = {
        "LOW": Level.LOW,
        "MEDIUM": Level.MED,
        "HIGH": Level.HIGH,
        "UNDEFINED": Level.UNKNOWN,
    }
    results = loads(
        _doSysExec(
            f"bandit -lirq -x {','.join(EXCLUDED)} -f json {scan_dir}", False
        )[1]
    )["results"]
    for result in results:
        file = result["filename"].replace("\\", "/")
        findings.append(
            {
                "id": result["test_id"],
                "title": f"{result['test_id']}: {result['test_name']}",
                "description": result["issue_text"],
                "file": file,
                "evidence": extractEvidence(result["line_number"], file)[
                    "content"
                ],
                "severity": levelMap[result["issue_severity"]],
                "confidence": levelMap[result["issue_confidence"]],
                "line": result["line_number"],
                "_other": {
                    "more_info": result["more_info"],
                    "line_range": result["line_range"],
                },
            }
        )
    return findings


def safety(scan_dir: str) -> list[Finding]:
    """safety plugin for generating list of findings using for safety. Requires
    safety on the system path.

    :raises: RuntimeError: if safety is not on the system path, then throw this error
    :param scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: returns structured list of findings, if there are any

    """
    if _doSysExec("safety --help")[0] != 0:
        raise RuntimeError("safety is not on the system path")
    try:
        results = loads(
            _doSysExec(
                f"poetry export --without-hashes -f requirements.txt | safety check --json --stdin"
            )[1]
        )
    except Exception as e:
        self.logger.warning(f"Unable to run safety, returned {e}")

    findings: [Finding] = []
    for result in results["affected_packages"]:
        package_name = result

        # Retrieve all relevant vulnerabilities
        relevant_vulnerabilities = str()
        for vulnerability in results["vulnerabilities"]:
            if vulnerability["package_name"] == package_name:
                relevant_vulnerabilities += str(vulnerability)

        findings.append(
            {
                "id": f"Safety: {package_name}",
                "title": f"Safety: {package_name}",
                "description": str(results["affected_packages"][package_name])
                + relevant_vulnerabilities,
                "file": "pyproject.toml",
                "evidence": extractEvidence(package_name, "pyproject.toml")[
                    "content"
                ],
                "severity": Level.MED,
                "confidence": Level.MED,
                "line": extractEvidence(package_name, "pyproject.toml")[
                    "line_nrs"
                ][0],
                "_other": {},
            }
        )

    return findings


def dodgy(scan_dir: str) -> list[Finding]:
    """dodgy plugin for generating list of findings using for dodgy. Requires
    dodgy on the system path.

    :raises: RuntimeError: if dodgy is not on the system path, then throw this error
    :param scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: returns structured list of findings, if there are any

    """
    if _doSysExec("dodgy -h")[0] != 0:
        raise RuntimeError("dodgy is not on the system path")
    findings: [Finding] = []
    results = loads(
        _doSysExec(f"dodgy {scan_dir} -i {' '.join(EXCLUDED)}")[1]
    )["warnings"]
    for result in results:
        file = "./" + result["path"].replace("\\", "/")
        findings.append(
            {
                "id": result["code"],
                "title": result["message"],
                "description": result["message"],
                "file": file,
                "evidence": extractEvidence(result["line"], file)["content"],
                "severity": Level.MED,
                "confidence": Level.MED,
                "line": result["line"],
                "_other": {},
            }
        )
    return findings


def flake8(scan_dir: str) -> list[dict]:
    """flake8 plugin for generating list of findings using for dlint. Requires
    flake8 and dlint on the system path.

    :raises: RuntimeError: if flake8 is not on the system path, then throw this error
    :param scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: returns structured list of findings, if there are any

    """

    """Generate list of findings using dlint. Requires flake8 and dlint on the system path.

    Raises:
            RuntimeError: if flake8 is not on the system path, then throw this
            error

    Returns:
            list[Finding]: our findings dictionary
    """
    if _doSysExec("flake8 -h")[0] != 0:
        raise RuntimeError("flake8 is not on the system path")
    findings: [Finding] = []

    # Using codeclimate format instead of json as it supports serverity indicators
    results = _doSysExec(
        f"flake8 --exclude {','.join(EXCLUDED)} --format=codeclimate {scan_dir}"
    )[1].splitlines(False)
    json_results = loads(results[0])
    levelMap = {
        "info": Level.LOW,
        "minor": Level.MED,
        "major": Level.MED,
        "critical": Level.HIGH,
        "blocker": Level.HIGH,
    }
    for path_of_file, scan_results in json_results.items():
        for scan_result in scan_results:
            findings.append(
                {
                    "id": scan_result["check_name"],
                    "title": f"{scan_result['check_name']}: {scan_result['description']}",
                    "description": f"{scan_result['check_name']}: {scan_result['description']}",
                    "file": path_of_file,
                    "evidence": extractEvidence(
                        scan_result["location"]["positions"]["begin"]["line"],
                        path_of_file,
                    )["content"],
                    "severity": levelMap[scan_result["severity"]],
                    "confidence": Level.MED,
                    "line": scan_result["location"]["positions"]["begin"][
                        "line"
                    ],
                    "_other": {
                        "col": scan_result["location"]["positions"]["begin"][
                            "column"
                        ],
                        "start": scan_result["location"]["positions"]["begin"][
                            "line"
                        ],
                        "end": scan_result["location"]["positions"]["end"][
                            "line"
                        ],
                        "fingerprint": scan_result["fingerprint"],
                    },
                }
            )
    return findings


def semgrep(scan_dir: str) -> list[dict]:
    """Semgrep plugin for generating list of findings using for semgrep.
    Requires Semgrep on the system path (wsl in windows).

    :raises: RuntimeError: if black cant be found
    :param str scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: returns structured list of findings, if there are any

    """
    findings: [Finding] = []
    if platform.system() == "Windows":
        raise RuntimeError("semgrep is not supported on windows")
    if _doSysExec("semgrep --help")[0] != 0:
        raise RuntimeError("semgrep is not on the system path")
    sgExclude = ["--exclude {x}" for x in EXCLUDED]
    results = loads(
        _doSysExec(
            f"semgrep -f {THISDIR}/semgrep_sec.yaml {scan_dir} {' '.join(sgExclude)} "
            "-q --json --no-rewrite-rule-ids"
        )[1].strip()
    )["results"]
    levelMap = {"INFO": Level.LOW, "WARNING": Level.MED, "ERROR": Level.HIGH}
    for result in results:
        file = scan_dir + "/" + result["Target"].replace("\\", "/")
        findings.append(
            {
                "id": result["check_id"],
                "title": result["check_id"].split(".")[-1],
                "description": result["extra"]["message"].strip(),
                "file": file,
                "evidence": extractEvidence(result["start"]["line"], file)[
                    "content"
                ],
                "severity": levelMap[result["extra"]["severity"]],
                "confidence": Level.HIGH,
                "line": result["start"]["line"],
                "_other": {
                    "col": result["start"]["col"],
                    "start": result["start"],
                    "end": result["end"],
                    "extra": result["extra"],
                },
            }
        )
    return findings


def trivy(scan_dir: str) -> list[dict]:
    """Trivy plugin for generating list of findings using for trivy. Requires
    trivy on the system path (wsl in windows).

    :raises: RuntimeError: if trivy cant be found
    :param str scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: returns structured list of findings, if there are any

    """
    findings: [Finding] = []
    if platform.system() == "Windows":
        raise RuntimeError("trivy is not supported on windows")
    if _doSysExec("trivy --help")[0] != 0:
        raise RuntimeError("trivy is not on the system path")
    # sgExclude = ["--exclude {x}" for x in EXCLUDED]
    payload = loads(
        _doSysExec(f"trivy fs {scan_dir} " " --format json -q")[1].strip()
    )

    levelMap = {
        "UNKNOWN": Level.UNKNOWN,
        "LOW": Level.LOW,
        "MEDIUM": Level.MED,
        "HIGH": Level.HIGH,
        "CRITICAL": Level.HIGH,
    }

    if "Results" in payload.keys():
        results = payload["Results"]
        for result in results:
            file = scan_dir + "/" + result["Target"].replace("\\", "/")
            # Title key is not always present in JSON, e.g. with secret scanning.
            if "Vulnerabilities" in result.keys():
                for vulnerability in result["Vulnerabilities"]:
                    # Title key is not always present in JSON
                    if "Title" in vulnerability.keys():
                        title = vulnerability["Title"]
                    else:
                        title = ""

                    if "PkgName" in vulnerability.keys():
                        evidence = extractEvidence(
                            vulnerability["PkgName"], file
                        )
                    else:
                        evidence = extractEvidence(0, file)
                    # Description contains a lot of additional new lines that are replaced with single new line.
                    simplified_description = vulnerability[
                        "Description"
                    ].replace("\n\n", "\n")
                    findings.append(
                        {
                            "id": vulnerability["VulnerabilityID"],
                            "title": f"{vulnerability['VulnerabilityID']} : {title}",
                            "description": f"{simplified_description} {vulnerability['PrimaryURL']}",
                            "file": file,
                            "evidence": evidence["content"],
                            "severity": levelMap[vulnerability["Severity"]],
                            "confidence": Level.HIGH,
                            "line": 0,
                        }
                    )
            elif result["Class"] == "secret":  # When dealing with secrets
                for secret in result["Secrets"]:
                    findings.append(
                        {
                            "id": secret["RuleID"],
                            "title": f"{secret['RuleID']} : {secret['Title']}",
                            "description": f"secrets issue",
                            "file": file,
                            "evidence": extractEvidence(
                                secret["StartLine"], file
                            )["content"],
                            "severity": levelMap[secret["Severity"]],
                            "confidence": Level.HIGH,
                            "line": secret["StartLine"],
                        }
                    )
            else:
                print("Unhandled type of class: ")
                print(result)
    else:  # Handling no results.
        findings = []
    return findings


def black(scan_dir: str) -> list[dict]:
    """Black plugin for reformatting the code. This plugin doesnt return
    scanning results but just reformat code.

    :raises: RuntimeError: if black cant be found
    :param str scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return list[Findings]: empty list as it does not return results.

    """
    if platform.system() == "Windows":
        raise RuntimeError("black is not supported on windows")
    if _doSysExec("black --help")[0] != 0:
        raise RuntimeError("black is not on the system path")
    results = _doSysExec(f"black {scan_dir}")
    print("##################  Reformatting  #########################")
    print(f"Black results: {results[1]}")
    return []


def mypy(scan_dir: str) -> list[dict]:
    """mypy plugin for generating list of findings using for semgrep. Requires
    mypy on the system path (wsl in windows). The structure of the output is:

    -- path:linenr:columnr:type:message --
    where the linenr and columnr can be optional.

    :raises: RuntimeError: if mypy cant be found
    :param scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: returns structured list of findings, if there are any

    """
    findings: [Finding] = []
    if platform.system() == "Windows":
        raise RuntimeError("mypy is not supported on windows")
    if _doSysExec("mypy --help")[0] != 0:
        raise RuntimeError("semgrep is not on the system path")

    sgExclude = ["--exclude {x}" for x in EXCLUDED]
    results = (
        _doSysExec(f"mypy {scan_dir}  {' '.join(sgExclude)}")[1]
        .strip()
        .split("\n")
    )
    levelMap = {"note": Level.LOW, "error": Level.HIGH}
    counter = 0

    for item in results[:-1]:
        correction = 0
        chunks = item.split(":")
        if chunks[1].isdigit():
            correction += 1
            linenr = int(chunks[1])
        else:
            linenr = 0
        if chunks[2].isdigit():
            correction += 1
            columnnr = int(chunks[2])
        else:
            columnnr = 0

        findings.append(
            {
                "id": f"mypy issue {counter}",
                "title": f"mypy: {chunks[correction + 1].strip()}",
                "description": " ".join(chunks[(correction + 1) :]),
                "file": chunks[0],
                "evidence": extractEvidence(linenr, chunks[0])["content"],
                "severity": levelMap[chunks[(correction + 1)].strip()],
                "confidence": levelMap[chunks[(correction + 1)].strip()],
                "line": linenr,
                "_other": {
                    "col": columnnr,
                },
            }
        )
        counter += 1
    return findings


def isort(scan_dir: str) -> list[dict]:
    """isort plugin for reformatting imports. This plugin doesn't return
    scanning results but just reformat code.

    :raises: RuntimeError: if isort cant be found
    :param scan_dir: The scanning path is a string that point to the directory that should be scanned. This argument is required.
    :return: empty list as it does not return results.
    """
    if platform.system() == "Windows":
        raise RuntimeError("isort is not supported on windows")
    if _doSysExec("isort --help")[0] != 0:
        raise RuntimeError("isort is not on the system path")
    results = _doSysExec(f"isort {scan_dir}")
    print("##################  Reformatting  #########################")
    print(f"Black results: {results[1]}")
    return []
