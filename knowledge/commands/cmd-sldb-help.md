---
id: cmd-sldb-help
system: sldb
command_path: help
synopsis: Curated CLI help.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# help

## Synopsis

Curated CLI help.

## Purpose

The `sldb help` command: Curated CLI help.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'help'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

topic | optional | stores, models, predicates, docs, fields, sections, ast, find, faq, inbox, explore, legacy

## Usage

help
