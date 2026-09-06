---
id: cmd-sldb-docs-compose
system: sldb
command_path: docs compose
synopsis: Expand ![[transclusions]] into composed Markdown.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs compose

## Synopsis

Expand ![[transclusions]] into composed Markdown.

## Purpose

The `sldb docs compose` command: Expand ![[transclusions]] into composed Markdown.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'compose'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

doc | required | Doc name or path
--store | optional | Store path
-o | optional | Output path or - for stdout
--format | optional | 

## Usage

docs compose
