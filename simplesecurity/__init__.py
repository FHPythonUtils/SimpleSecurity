from __future__ import annotations

import argparse
import logging
import os
from sys import exit as sysexit
from sys import stdout
from typing import Any

from simplesecurity import filter as secfilter
from simplesecurity import formatter, plugins
from simplesecurity.github import GithubAnnotationsAndComments
from simplesecurity.types import Finding

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-6s %(levelname)-6s %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger()

stdout.reconfigure(encoding="utf-8")  # type:ignore
FORMAT_HELP = "Output format. One of ansi, json, markdown, csv. default=ansi"
PLUGIN_HELP = (
    "Plugin to use. One of bandit, safety, dodgy, dlint, semgrep, "
    "trivy or all, default=all"
)
SCAN_PATH = (
    "Define Path that should be scannend, default path is root of CLI tool"
)


def runAllPlugins(
    scan_path: str,
    pluginMap: dict[str, Any],
    severity: int,
    confidence: int,
    fast: bool,
) -> list[Finding]:
    """This helper function triggers als scans if no specific scan is
    requested. It triggers the scans chronologically.

    :param scan_path: The scanning path is a string that point to the directory
     that should be scanned. This argument is required.
    :param pluginMap: A map of all the plugins, or scans, that are iterated
    over when scanning everything.
    :param severity: Level of Severity helps you filter through the results and
    is denoted as a integer.
    :param confidence: Level of Confidence helps you filter through the results
     and is denoted as a integer.
    :param fast: A Boolean indicator to enable fast scanning when available.
    :return: A list findings that the list of scans have returned.

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
        help="Skip long running jobs. Will omit plugins with long run time "
        "(applies to -p all only)",
    )
    parser.add_argument(
        "--zero",
        "-0",
        action="store_true",
        help="Return non zero exit code if any security vulnerabilities are "
        "found",
    )
    parser.add_argument(
        "--send_to_git",
        action="store_true",
        default=False,
        help="Explicit Flag for I you want to annotate your PR, doesnt require"
        " value. Make sure that you use the other Git Flags too. These "
        "include --github_access_token, --github_repository and "
        "--github_pr_number",
    )
    parser.add_argument(
        "--github_access_token",
        action="store",
        default=None,
        help="Provide the GitHub Access Token if you want to annotate the PR "
        "(For CI applications)",
    )
    parser.add_argument(
        "--github_repo_url",
        action="store",
        default=None,
        help="Provide the Repo URL if you want to annotate the PR (For CI "
        "applications)",
    )
    parser.add_argument(
        "--github_workflow_run_id",
        action="store",
        default=None,
        help="Provide the github workflow id if you want to annotate the PR "
        "(For CI applications)",
    )

    args = parser.parse_args()
    # File
    filename = (
        stdout
        if args.file is None
        else open(
            args.file, "w", encoding="utf-8"
        )  # pylint: disable=consider-using-with
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
        # Needs to run after black
        "flake8": {
            "func": plugins.flake8,
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

    assert args.scan_path is not None, "Please define scanning path"
    assert (
        os.path.exists(args.scan_path)
        or os.path.exists(os.path.join(os.getcwd(), args.scan_path))
    ) is True, "Scanning path not found.."

    scanning_path = os.path.abspath(str(args.scan_path))

    if args.plugin is None or args.plugin == "all" or args.plugin in pluginMap:
        if args.plugin is None or args.plugin == "all":
            findings = runAllPlugins(
                scan_path=scanning_path,
                pluginMap=pluginMap,
                severity=args.level,
                confidence=args.confidence,
                fast=args.fast,
            )
        else:
            findings = pluginMap[args.plugin]["func"](scan_dir=scanning_path)
        print(
            formatt(
                secfilter.filterSeverityAndConfidence(
                    secfilter.deduplicate(findings),
                    args.level,
                    args.confidence,
                ),
                colourMode=colourMode,
            ),
            file=filename,
        )
        if args.send_to_git:
            assert (
                args.github_access_token is not None
            ), "Error, please provide github_access_token provided"
            assert (
                args.github_repo_url is not None
            ), "Error, please provide github_repo_url provided"
            assert (
                args.github_workflow_run_id is not None
            ), "Error, please provide github_workflow_run_id provided"

            try:
                GithubAnnotationsAndComments(
                    github_access_token=args.github_access_token,
                    github_repo_url=args.github_repo_url,
                    github_workflow_run_id=args.github_workflow_run_id,
                    findings=findings,
                    logger=logger,
                ).annotate_and_comment_in_pr()

            except Exception as e:
                print(e)
    else:
        print(PLUGIN_HELP)
        sysexit(2)
    if len(findings) > 0 and args.zero:
        sysexit(1)
    sysexit(0)
