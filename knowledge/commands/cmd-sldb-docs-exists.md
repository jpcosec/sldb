---
id: cmd-sldb-docs-exists
system: sldb
command_path: docs exists
synopsis: Check that a doc reference resolves, here or in a linked store, without
  importing it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#docs exists; contract-sha256:5fd8a9128bfc5bfb17c85cf5f2d4690d29f1cbad7f47e592501b68e8e53319c2
---

# docs exists

## Synopsis

Check that a doc reference resolves, here or in a linked store, without importing it.

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
        "ref"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name, Model/DocName or tracked path; 'alias:ref' for a directly linked store"
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
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\""
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

usage: sldb docs exists [-h] [--store STORE] [--format {text,json}] ref
