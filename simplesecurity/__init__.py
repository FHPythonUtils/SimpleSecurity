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
from typing import Any, Callable, TextIO

from simplesecurity import filter as secfilter
from simplesecurity import formatter, plugins

stdout.reconfigure(encoding="utf-8")  # type:ignore
FORMAT_HELP = "Output format. One of ansi, json, markdown, csv. default=ansi"
PLUGIN_HELP = "Plugin to use. One of bandit, safety, dodgy, dlint, semgrep, all, default=all"


def _processFile(file: str | None) -> TextIO:
	return (
		stdout
		if file is None
		else open(file, "w", encoding="utf-8")  # pylint: disable=consider-using-with
	)


def _processColour(noColour: bool, highContrast: bool) -> int:
	colourMode = 1
	if noColour:
		colourMode = 0
	if highContrast:
		colourMode = 2
	return colourMode


def _processFormat(formatin: str | None) -> Callable:
	formatMap = {
		"json": formatter.json,
		"markdown": formatter.markdown,
		"csv": formatter.csv,
		"ansi": formatter.ansi,
		"sarif": formatter.sarif,
	}
	if formatin is None:
		formatt = formatter.ansi
	elif formatin in formatMap:
		formatt = formatMap[formatin]
	else:
		print(FORMAT_HELP)
		sysexit(1)
	return formatt


def _processPlugin(args) -> list[Callable]:
	pluginMap = {
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
			"max_severity": 3,
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

	plugin = args.plugin

	filtered = {
		k: v["func"]
		for k, v in pluginMap.items()
		if (
			v["max_severity"] >= args.level
			and v["max_confidence"] >= args.confidence
			and (not args.fast or v["fast"])
		)
	}

	if plugin in (None, "all"):
		return [v for _, v in filtered.items()]
	if plugin in filtered:
		return [filtered[plugin]]

	print(PLUGIN_HELP)
	sysexit(2)


def cli():
	"""Cli entry point."""
	parser = argparse.ArgumentParser(
		description=__doc__, formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument(
		"--scan-dir",
		"-s",
		help="Pass a path to the scan directory (optional)",
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
	# Let's use a low level and medium confidence by default
	parser.add_argument(
		"--level",
		"-l",
		help="Minimum severity/ level to show",
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

	scanDir = args.scan_dir or "."
	filename = _processFile(args.file)
	colourMode = _processColour(args.no_colour, args.high_contrast)
	formatt = _processFormat(args.format)

	filteredPlugins = _processPlugin(args)

	findings = []
	for plugin in filteredPlugins:
		finding = []
		try:
			finding = plugin(scanDir=scanDir)
		except BaseException as e:
			print(f"! SimpleSecurity encountered an error: {e}")
		findings.extend(finding)

	filteredFindings = secfilter.filterSeverityAndConfidence(
		secfilter.deduplicate(findings), args.level, args.confidence
	)

	print(
		formatt(
			filteredFindings,
			colourMode=colourMode,
		),
		file=filename,
	)

	if len(filteredFindings) > 0 and args.zero:
		sysexit(1)
	sysexit(0)
