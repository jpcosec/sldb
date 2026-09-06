---
id: cmd-sldb-models-fields-add
system: sldb
command_path: models fields add
synopsis: Add a field to the model draft.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# models fields add

## Synopsis

Add a field to the model draft.

## Purpose

The `sldb models fields add` command: Add a field to the model draft.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'add'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

model | required | Model name
field | required | Field name
--type | required | Python type annotation
--description | required | Field description
--default | optional | Inline YAML/JSON default value
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

models fields add
