---
id: cmd-sldb-predicates-add
system: sldb
command_path: predicates add
synopsis: Register a predicate definition.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#predicates add; contract-sha256:4c58c0121ac9193c1128e8bc9a88f5fe83f7559cded1ea8d05a5a24b508c4c2d
---

# predicates add

## Synopsis

Register a predicate definition.

## Purpose

The `sldb predicates add` command: Register a predicate definition.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'add'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "name"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Predicate name used in [name:: [[target]]]."
    },
    {
      "names": [
        "--axis"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Semantic axis, for example HOW."
    },
    {
      "names": [
        "--description"
      ],
      "required": false,
      "default": "\"\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Predicate description."
    },
    {
      "names": [
        "--store"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Store path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

predicates add
