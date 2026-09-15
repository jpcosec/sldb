---
id: cmd-sldb-predicates-remove
system: sldb
command_path: predicates remove
synopsis: Remove a predicate definition.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#predicates remove; contract-sha256:9befc14dbf8ac94f9b74c7bf5e8d89c01b6ce6720605daf355db80dfc660d240
---

# predicates remove

## Synopsis

Remove a predicate definition.

## Purpose

The `sldb predicates remove` command: Remove a predicate definition.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'remove'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
      "help": "Predicate name"
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

predicates remove
