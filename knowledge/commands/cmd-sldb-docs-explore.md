---
id: cmd-sldb-docs-explore
system: sldb
command_path: docs explore
synopsis: Search tracked docs, repo docs, and docstrings.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# docs explore

## Synopsis

Search tracked docs, repo docs, and docstrings.

## Purpose

The `sldb docs explore` command: Search tracked docs, repo docs, and docstrings.

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

docs explore
