---
id: cmd-sldb-notations-list
system: sldb
command_path: notations list
synopsis: List notations or projection views in the store or builtins.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations list; contract-sha256:4d188184699c968ab11e21b745d7d89048410c3150917af57bedc079ac1cb26a
---

# notations list

## Synopsis

List notations or projection views in the store or builtins.

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
        "--views"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "List projection views instead of notations"
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

usage: sldb notations list [-h] [--views] [--store STORE] [--pythonpath PYTHONPATH]
