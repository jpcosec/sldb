---
id: cmd-sldb-serve
system: sldb
command_path: serve
synopsis: Serve the store over HTTP using the same methods as the CLI.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# serve

## Synopsis

Serve the store over HTTP using the same methods as the CLI.

## Purpose

The `sldb serve` command: Serve the store over HTTP using the same methods as the CLI.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'serve'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--host | optional | 
--port | optional | 
--store | optional | Store path
--pythonpath | optional | Project path
--cors | optional | Send permissive CORS headers (for browser clients)

## Usage

serve
