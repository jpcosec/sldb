---
id: cmd-sldb-predicates-show
system: sldb
command_path: predicates show
synopsis: Show one predicate definition.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# predicates show

## Synopsis

Show one predicate definition.

## Purpose

The `sldb predicates show` command: Show one predicate definition.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

name | required | Predicate name
--store | optional | Store path
--format | optional | 

## Usage

predicates show
