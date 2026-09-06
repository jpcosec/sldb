---
id: cmd-sldb-render
system: sldb
command_path: render
synopsis: Render Markdown from data.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# render

## Synopsis

Render Markdown from data.

## Purpose

The `sldb render` command: Render Markdown from data.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'render'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model ref: module:Class
input | required | Data file
output | required | Output .md
--pythonpath | optional | Project path

## Usage

render
