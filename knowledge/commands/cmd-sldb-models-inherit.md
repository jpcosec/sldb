---
sldb:
  by: agent
  at: '2026-11-16T20:57:19Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-models-inherit
system: sldb
command_path: models inherit
synopsis: Inherit a model from the linked store that owns it (converts a local copy).
tags: []
provenance: parser:sldb.cli.parser:build_parser#models inherit; contract-sha256:34302028f3a983aeb7e866ef2b6d0eb67f9d983e67c974e6765eddabfee106c5
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
        "--version"
      ],
      "required": false,
      "default": "SUPPRESS",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "sldb.cli.parsers.core._VersionAction",
      "const": "null",
      "help": "print the version and the git revision, then exit"
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
