---
id: cmd-sldb-predicates-add
system: sldb
command_path: predicates add
synopsis: Register a predicate definition.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# predicates add

## Synopsis

Register a predicate definition.

## Purpose

The `sldb predicates add` command: Register a predicate definition.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'add'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

name | required | Predicate name used in [name:: [[target]]].
--axis | required | Semantic axis, for example HOW.
--description | optional | Predicate description.
--store | optional | Store path

## Usage

predicates add
