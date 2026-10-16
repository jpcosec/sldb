---
id: cmd-sldb-models-remove
system: sldb
command_path: models remove
synopsis: Unregister a model; refused while it tracks documents unless --with-documents.
tags: []
provenance: parser:sldb.cli.parser:build_parser#models remove; contract-sha256:e8f4c6402be8397969f891adbafd1d00a4c5d32803db2f93e7367661185b23b5
---

# models remove

## Synopsis

Unregister a model; refused while it tracks documents unless --with-documents.

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
        "--with-documents"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Also untrack its documents (files stay); the class need not import"
    },
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
