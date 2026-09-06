---
id: cmd-sldb-sections-fields
system: sldb
command_path: sections fields
synopsis: Show fields owned by a section.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# sections fields

## Synopsis

Show fields owned by a section.

## Purpose

The `sldb sections fields` command: Show fields owned by a section.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'fields'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

target | required | docs/<Doc> or docs/<Doc>/<section_path>
--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | 

## Usage

sections fields
