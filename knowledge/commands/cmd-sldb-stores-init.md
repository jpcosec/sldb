---
id: cmd-sldb-stores-init
system: sldb
command_path: stores init
synopsis: Init .sldb store.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# stores init

## Synopsis

Init .sldb store.

## Purpose

The `sldb stores init` command: Init .sldb store.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'init'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

--path | optional | 
--force | optional | 

## Usage

stores init
