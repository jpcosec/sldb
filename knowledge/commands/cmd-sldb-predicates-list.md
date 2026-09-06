---
id: cmd-sldb-predicates-list
system: sldb
command_path: predicates list
synopsis: List predicate definitions.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# predicates list

## Synopsis

List predicate definitions.

## Purpose

The `sldb predicates list` command: List predicate definitions.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'list'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--store | optional | Store path
--format | optional | 

## Usage

predicates list
