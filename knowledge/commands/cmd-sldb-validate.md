---
id: cmd-sldb-validate
system: sldb
command_path: validate
synopsis: Validate idempotency.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# validate

## Synopsis

Validate idempotency.

## Purpose

The `sldb validate` command: Validate idempotency.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'validate'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model ref: module:Class
--input | optional | Markdown file
--data | optional | Data file
--format | optional | 
--pythonpath | optional | Project path

## Usage

validate
