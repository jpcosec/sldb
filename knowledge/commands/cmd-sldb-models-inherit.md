---
id: cmd-sldb-models-inherit
system: sldb
command_path: models inherit
synopsis: Inherit a model from the linked store that owns it (converts a local copy).
tags: []
provenance: parser:sldb.cli.parser:build_parser#models inherit; contract-sha256:e4fd776c4e78871f8dce5af72426b0a709efa57bae39997cbf435bfc2eec5d3b
---

# models inherit

## Synopsis

Inherit a model from the linked store that owns it (converts a local copy).

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
        "model"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "alias:ModelName, the alias linked with `stores add`"
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

usage: sldb models inherit [-h] [--store STORE] [--pythonpath PYTHONPATH] model
