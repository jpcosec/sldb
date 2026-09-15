---
id: cmd-sldb-docs-list
system: sldb
command_path: docs list
synopsis: List tracked documents.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#docs list; contract-sha256:49fa1cc6ce0e6c19eab4f1c2d3d43a0885c4a0432c4e64ad83bb7e32c32b816d
---

# docs list

## Synopsis

List tracked documents.

## Purpose

The `sldb docs list` command: List tracked documents.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'list'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
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
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\"",
        "\"yaml\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

docs list
