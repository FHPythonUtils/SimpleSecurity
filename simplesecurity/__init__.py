"""Combine multiple popular python security tools and generate reports or output
into different formats

Plugins (these require the plugin executable in the system path. e.g. bandit
requires bandit to be in the system path...)

- bandit
- safety
- dodgy
- dlint

Formats

- ansi (for terminal)
- json
- markdown
- csv
"""
import argparse
from sys import exit as sysexit, stdout

import simplesecurity.formatter as formatter
import simplesecurity.plugins as plugins

FORMAT_HELP = "Output format. One of ansi, json, markdown, csv. default=ansi"
PLUGIN_HELP = "Plugin to use. One of bandit, safety, dodgy, dlint, all, default=all"


def cli():
	""" cli entry point """
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--format", "-f", help=FORMAT_HELP)
	parser.add_argument("--plugin", "-p", help=PLUGIN_HELP)
	parser.add_argument("--file", "-o",
	help="Filename to write to (omit for stdout)")
	args = parser.parse_args()
	# File
	filename = stdout if args.file is None else open(args.file, "w", encoding="utf-8")

	# Format
	formatMap = {
	"json": formatter.json, "markdown": formatter.markdown, "csv": formatter.csv,
	"ansi": formatter.ansi}
	if args.format is None:
		formatt = formatter.ansi
	elif args.format in formatMap:
		formatt = formatMap[args.format]
	else:
		print(FORMAT_HELP)
		sysexit(1)

	# Plugin
	pluginMap = {
	"bandit": plugins.bandit, "safety": plugins.safety, "dodgy": plugins.dodgy,
	"dlint": plugins.dlint}
	if args.plugin is None or args.plugin == "all":
		print(
		formatt(plugins.bandit() + plugins.safety() + plugins.dodgy() +
		plugins.dlint()), file=filename)
	elif args.plugin in pluginMap:
		print(formatt(pluginMap[args.plugin]()), file=filename)
	else:
		print(PLUGIN_HELP)
		sysexit(1)
