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

from simplesecurity import filter as secfilter
from simplesecurity import formatter, plugins
from simplesecurity.types import Finding

stdout.reconfigure(encoding="utf-8")  # type:ignore
FORMAT_HELP = "Output format. One of ansi, json, markdown, csv. default=ansi"
PLUGIN_HELP = "Plugin to use. One of bandit, safety, dodgy, dlint, semgrep, all, default=all"


def runAllPlugins(
	pluginMap: dict[str, Any], severity: int, confidence: int, fast: bool
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
				findings.extend(pluginMap[plugin]["func"]())
			except RuntimeError as error:
				print(error)
	return findings


def cli():
	"""Cli entry point."""
	parser = argparse.ArgumentParser(
		description=__doc__, formatter_class=argparse.RawTextHelpFormatter
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
	args = parser.parse_args()
	# File
	filename = stdout if args.file is None else open(args.file, "w", encoding="utf-8")
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
	}

	if args.plugin is None or args.plugin == "all" or args.plugin in pluginMap:
		findings = []
		if args.plugin is None or args.plugin == "all":
			findings = runAllPlugins(pluginMap, args.level, args.confidence, args.fast)
		elif (
			pluginMap[args.plugin]["max_severity"] >= args.level
			and pluginMap[args.plugin]["max_confidence"] >= args.confidence
		):
			findings = pluginMap[args.plugin]["func"]()
		print(
			formatt(
				secfilter.filterSeverityAndConfidence(
					secfilter.deduplicate(findings), args.level, args.confidence
				),
				colourMode=colourMode,
			),
			file=filename,
		)
	else:
		print(PLUGIN_HELP)
		sysexit(2)
	if len(findings) > 0 and args.zero:
		sysexit(1)
	sysexit(0)
