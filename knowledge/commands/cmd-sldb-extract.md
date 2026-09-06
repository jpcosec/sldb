---
id: cmd-sldb-extract
system: sldb
command_path: extract
synopsis: Extract data from Markdown.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# extract

## Synopsis

Extract data from Markdown.

## Purpose

The `sldb extract` command: Extract data from Markdown.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'extract'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model ref: module:Class
input | required | Markdown file
output | required | Output JSON/YAML
--format | optional | 
--pythonpath | optional | Project path

## Usage

extract
