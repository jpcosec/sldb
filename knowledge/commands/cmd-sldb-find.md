---
id: cmd-sldb-find
system: sldb
command_path: find
synopsis: Unified semantic + physical retrieval.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# find

## Synopsis

Unified semantic + physical retrieval.

## Purpose

The `sldb find` command: Unified semantic + physical retrieval.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'find'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

term | required | Resource term, semantic tag, or physical token
--in | optional | Use `physical` for names, paths, section titles, and field addresses
--global | optional | 
--regex | optional | 
--fuzzy | optional | 
--rebuild | optional | 
--type | optional | 
--select | optional | Comma-separated projection fields
--where | optional | Filter expression
--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | 

## Usage

find
