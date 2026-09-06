---
id: cmd-sldb-predicates-validate
system: sldb
command_path: predicates validate
synopsis: Validate predicate definitions.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# predicates validate

## Synopsis

Validate predicate definitions.

## Purpose

The `sldb predicates validate` command: Validate predicate definitions.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'validate'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

name | optional | Optional predicate name
--store | optional | Store path
--format | optional | 

## Usage

predicates validate
