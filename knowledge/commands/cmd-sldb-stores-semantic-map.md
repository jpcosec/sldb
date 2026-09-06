---
id: cmd-sldb-stores-semantic-map
system: sldb
command_path: stores semantic-map
synopsis: Map equivalent semantic concepts.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# stores semantic-map

## Synopsis

Map equivalent semantic concepts.

## Purpose

The `sldb stores semantic-map` command: Map equivalent semantic concepts.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'semantic-map'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

concept_a | required | First concept
concept_b | required | Second concept
--store | optional | Store path

## Usage

stores semantic-map
