---
id: cmd-sldb-docs-recover
system: sldb
command_path: docs recover
synopsis: Resolve [[links]] and report their targets.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs recover

## Synopsis

Resolve [[links]] and report their targets.

## Purpose

The `sldb docs recover` command: Resolve [[links]] and report their targets.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'recover'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

doc | required | Doc name or path
--store | optional | Store path
--format | optional | 
--depth | optional | 
--links-only | optional | 
--include-transclusions | optional | 

## Usage

docs recover
