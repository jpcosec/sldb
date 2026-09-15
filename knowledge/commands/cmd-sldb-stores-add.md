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
provenance: parser:sldb.cli.parser:build_parser#stores add; contract-sha256:420e56e3c941638193aae484468577ca5eee1c6a17a48719fb71478655770543
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

stores add
