---
id: cmd-sldb-explore
system: sldb
command_path: explore
synopsis: Search markdown docs and Python docstrings.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# explore

## Synopsis

Search markdown docs and Python docstrings.

## Purpose

The `sldb explore` command: Search markdown docs and Python docstrings.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'explore'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

term | required | Search term or regex
--source | optional | 
--regex | optional | 
--docs-root | optional | Docs directory to scan
--code-root | optional | Python source directory to scan
--max-results | optional | 
--format | optional | 

## Usage

explore
