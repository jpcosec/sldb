---
id: cmd-sldb-stores-add
system: sldb
command_path: stores add
synopsis: Link federated store.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#stores add; contract-sha256:a5a60d8166665974dd1fe4c554f241f9dd5bc69fdfcb5432488ef1a459c4d423
---

# stores add

## Synopsis

Link federated store.

## Purpose

The `sldb stores add` command: Link federated store.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'add'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "path"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Store path"
    },
    {
      "names": [
        "--name"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Store name"
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
      "help": "Local store path"
    },
    {
      "names": [
        "--replace"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Point a link already recorded under that name here"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

stores add
