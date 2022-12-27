"""
Combine multiple popular python security tools and generate reports or output
into different formats

Plugins (these require the plugin executable in the system path. e.g. bandit
requires bandit to be in the system path...)

- bandit
- safety
- dodgy
- dlint
- semgrep

Formats

- ansi (for terminal)
- json
- markdown
- csv
- sarif
"""
from __future__ import annotations

import argparse
from sys import exit as sysexit
from sys import stdout
from typing import Any
import os

from github import Github
from simplesecurity import filter as secfilter
from simplesecurity import formatter, plugins
from simplesecurity.types import Finding

stdout.reconfigure(encoding="utf-8")  # type:ignore
FORMAT_HELP = "Output format. One of ansi, json, markdown, csv. default=ansi"
PLUGIN_HELP = (
    "Plugin to use. One of bandit, safety, dodgy, dlint, semgrep, trivy or all, default=all"
)
SCAN_PATH = "Define Path that should be scannend, default path is root of CLI tool"


def comment_in_pr(github_access_token, github_repository, github_pr_number, findings):
    """Annotate a PR with a comment."""
    github_session = Github(github_access_token)
    repo = github_session.get_repo(github_repository)
    pull_request = repo.get_pull(int(github_pr_number))
    commits = pull_request.get_commits()

    for find in findings:
        pull_request.create_comment(
            body=f"Title: {find['title']}; \nDescription: {find['description']}",
            commit_id=commits.reversed[0],
            path=find["file"],
            position=find["line"],
        )


def runAllPlugins(
    scan_path: str, pluginMap: dict[str, Any], severity: int, confidence: int, fast: bool
) -> list[Finding]:
    """Run each plugin. Optimise as much as we can.

    Args:
            pluginMap (dict[str, Any]): the plugin map
            severity (int): the minimum severity to report on
            confidence (int): the minimum confidence to report on
            fast (bool): runAllPlugins with optimisations

    Returns:
            list[Finding]: list of findings
    """
    findings: list[Finding] = []
    for plugin in pluginMap:
        # Do optimisations
        if (
            pluginMap[plugin]["max_severity"] >= severity
            and pluginMap[plugin]["max_confidence"] >= confidence
            and (not fast or pluginMap[plugin]["fast"])
        ):
            try:
                findings.extend(pluginMap[plugin]["func"](scan_dir=scan_path))
            except RuntimeError as error:
                print(error)
    return findings


def cli():
    """Cli entry point."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--scan_path",
        "-s",
        default=None,
        action="store",
        help=SCAN_PATH,
    )
    parser.add_argument(
        "--format",
        "-f",
        help=FORMAT_HELP,
    )
    parser.add_argument(
        "--plugin",
        "-p",
        help=PLUGIN_HELP,
    )
    parser.add_argument(
        "--file",
        "-o",
        help="Filename to write to (omit for stdout)",
    )
    # Let's use a low severity and medium confidence by default
    parser.add_argument(
        "--level",
        "-l",
        help="Minimum level/ severity to show",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--confidence",
        "-c",
        help="Minimum confidence to show",
        type=int,
        default=2,
    )
    parser.add_argument(
        "--no-colour",
        "-z",
        help="No ANSI colours",
        action="store_true",
    )
    parser.add_argument(
        "--high-contrast",
        "-Z",
        help="High contrast colours",
        action="store_true",
    )
    parser.add_argument(
        "--fast",
        "--skip",
        action="store_true",
        help="Skip long running jobs. Will omit plugins with long run time (applies to -p all only)",
    )
    parser.add_argument(
        "--zero",
        "-0",
        action="store_true",
        help="Return non zero exit code if any security vulnerabilities are found",
    )
    parser.add_argument(
        "--send_to_git",
        action="store_true",
        default=False,
        help="Explicit Flag for I you want to annotate your PR, doesnt require value. Make sure that you use the other Git Flags too. These include --github_access_token, --github_repository and --github_pr_number",
    )
    parser.add_argument(
        "--github_access_token",
        action="store",
        default=None,
        help="Provide the GitHub Access Token if you want to annotate the PR (For CI applications)",
    )
    parser.add_argument(
        "--github_repository",
        action="store",
        default=None,
        help="Provide the Repo if you want to annotate the PR (For CI applications)",
    )
    parser.add_argument(
        "--github_pr_number",
        action="store",
        default=None,
        help="Provide the PR Number if you want to annotate the PR (For CI applications)",
    )

    args = parser.parse_args()
    # File
    filename = (
        stdout
        if args.file is None
        else open(args.file, "w", encoding="utf-8")  # pylint: disable=consider-using-with
    )
    # Colour Mode
    colourMode = 1
    if args.no_colour:
        colourMode = 0
    if args.high_contrast:
        colourMode = 2
    # Format
    formatMap = {
        "json": formatter.json,
        "markdown": formatter.markdown,
        "csv": formatter.csv,
        "ansi": formatter.ansi,
        "sarif": formatter.sarif,
    }
    if args.format is None:
        formatt = formatter.ansi
    elif args.format in formatMap:
        formatt = formatMap[args.format]
    else:
        print(FORMAT_HELP)
        sysexit(1)

    # Plugin
    pluginMap: dict[str, Any] = {
        "bandit": {
            "func": plugins.bandit,
            "max_severity": 3,
            "max_confidence": 3,
            "fast": True,
        },
        "safety": {
            "func": plugins.safety,
            "max_severity": 2,
            "max_confidence": 3,
            "fast": True,
        },
        "dodgy": {
            "func": plugins.dodgy,
            "max_severity": 2,
            "max_confidence": 2,
            "fast": True,
        },
        "dlint": {
            "func": plugins.dlint,
            "max_severity": 2,
            "max_confidence": 2,
            "fast": True,
        },
        "semgrep": {
            "func": plugins.semgrep,
            "max_severity": 3,
            "max_confidence": 3,
            "fast": False,
        },
        "trivy": {
            "func": plugins.trivy,
            "max_severity": 3,
            "max_confidence": 3,
            "fast": False,
        },
    }

    assert type(args.scan_path) == str, "Please define scanning path"
    assert (
        os.path.exists(args.scan_path) or os.path.exists(os.path.join(os.getcwd(), args.scan_path))
    ) == True, "Scanning path not found.."
    # TODO, we might need to validate whether it make sense to parse a absolute path as scan_path by default for robustness.

    if args.plugin is None or args.plugin == "all" or args.plugin in pluginMap:
        findings = []
        if args.plugin is None or args.plugin == "all":
            findings = runAllPlugins(
                scan_path=args.scan_path,
                pluginMap=pluginMap,
                severity=args.level,
                confidence=args.confidence,
                fast=args.fast,
            )
        elif (
            pluginMap[args.plugin]["max_severity"] >= args.level
            and pluginMap[args.plugin]["max_confidence"] >= args.confidence
        ):
            findings = pluginMap[args.plugin]["func"](scan_dir=args.scan_path)
        print(
            formatt(
                secfilter.filterSeverityAndConfidence(
                    secfilter.deduplicate(findings), args.level, args.confidence
                ),
                colourMode=colourMode,
            ),
            file=filename,
        )

        if args.send_to_git:
            assert (
                args.github_access_token != None
            ), "Error, please provide github_access_token provided"
            assert (
                args.github_repository != None
            ), "Error, please provide github_repository provided"
            assert args.github_pr_number != None, "Error, please provide github_pr_number provided"

            comment_in_pr(
                github_access_token=args.github_access_token,
                github_repository=args.github_repository,
                github_pr_number=args.github_pr_number,
            )
    else:
        print(PLUGIN_HELP)
        sysexit(2)
    if len(findings) > 0 and args.zero:
        sysexit(1)
    sysexit(0)
