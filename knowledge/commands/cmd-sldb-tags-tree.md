---
id: cmd-sldb-tags-tree
system: sldb
command_path: tags tree
synopsis: 'One namespace''s tags as a tree: roots (nested by prefix), orphans and
  unplaced.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#tags tree; contract-sha256:c083d074f6a389db14066a86d26f00ac78965af9584cf4fee0c65e4139d1919a
---

# tags tree

## Synopsis

One namespace's tags as a tree: roots (nested by prefix), orphans and unplaced.

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
        "namespace"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "A declared namespace, e.g. area"
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
      "help": "Directory to import models from"
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
      "help": "Output format (default text)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb tags tree [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] namespace
