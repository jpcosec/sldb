---
id: cmd-sldb-models-list
system: sldb
command_path: models list
synopsis: List registered models.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models list

## Synopsis

List registered models.

## Purpose

The `sldb models list` command: List registered models.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'list'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--store | optional | Store path
--format | optional | 

## Usage

models list
