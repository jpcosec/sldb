---
id: cmd-sldb-notations-sync
system: sldb
command_path: notations sync
synopsis: Synchronize a notation or palette into the store.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations sync; contract-sha256:59f3ca9e016be2b040396ba2f6ee089fe2c93a331956da3925dd684a012bd21e
---

# notations sync

## Synopsis

Synchronize a notation or palette into the store.

## Purpose

Not documented.

## How It Works

Not documented.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "--notation"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Notation name or YAML file to sync"
    },
    {
      "names": [
        "--palette"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Palette name or YAML file to sync"
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

usage: sldb notations sync [-h] [--notation NOTATION] [--palette PALETTE] [--store STORE] [--pythonpath PYTHONPATH]
