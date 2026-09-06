---
id: cmd-sldb-inbox
system: sldb
command_path: inbox
synopsis: Log unclear points or suggestions into the repo desk.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# inbox

## Synopsis

Log unclear points or suggestions into the repo desk.

## Purpose

The `sldb inbox` command: Log unclear points or suggestions into the repo desk.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'inbox'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

message | optional | Inbox note body
--kind | optional | Type of desk note to write
--title | optional | Short title for the note
--desk-root | optional | Desk root directory override
--store | optional | Store path used to resolve the target project root
--pythonpath | optional | Project path used when auto-tracking inbox notes
--author | optional | Source label for the inbox note
--list | optional | List desk inbox notes
--show | optional | Show one inbox note
--limit | optional | Limit listed notes
--format | optional | 

## Usage

inbox
