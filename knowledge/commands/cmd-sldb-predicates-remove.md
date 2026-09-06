---
id: cmd-sldb-predicates-remove
system: sldb
command_path: predicates remove
synopsis: Remove a predicate definition.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# predicates remove

## Synopsis

Remove a predicate definition.

## Purpose

The `sldb predicates remove` command: Remove a predicate definition.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'remove'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

name | required | Predicate name
--store | optional | Store path

## Usage

predicates remove
