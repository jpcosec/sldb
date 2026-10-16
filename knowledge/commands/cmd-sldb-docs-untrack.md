---
id: cmd-sldb-docs-untrack
system: sldb
command_path: docs untrack
synopsis: Remove a tracked doc from the store, keeping its file.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#docs untrack; contract-sha256:3e476408df09ed3c9430516902c4746737a6c637cff3209e05c7c6287a299dba
---

# docs untrack

## Synopsis

Remove a tracked doc from the store, keeping its file.

## Purpose

The `sldb docs untrack` command: Remove a tracked doc from the store.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'untrack'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "doc"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name or tracked path"
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
    },
    {
      "names": [
        "--pythonpath"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Project path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

docs untrack
