---
id: cmd-sldb-models-remove
system: sldb
command_path: models remove
synopsis: Unregister a model that tracks no documents.
tags: []
provenance: parser:sldb.cli.parser:build_parser#models remove; contract-sha256:a3b2a11fcbda5e3b2328f8a1ed007fbf84f38680b1b8afce8a7e70c9b4901b58
---

# models remove

## Synopsis

Unregister a model that tracks no documents.

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
      "help": "Model name"
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

usage: sldb models remove [-h] [--store STORE] [--pythonpath PYTHONPATH] model
