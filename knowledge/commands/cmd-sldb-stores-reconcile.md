---
id: cmd-sldb-stores-reconcile
system: sldb
command_path: stores reconcile
synopsis: Explicitly reconcile a catalog against a subtree.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores reconcile; contract-sha256:fa5677737edd6da97f7720ab902239b5b8696e0a37d21e25444e1fe28127bfb1
---

# stores reconcile

## Synopsis

Explicitly reconcile a catalog against a subtree.

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
        "--path"
      ],
      "required": false,
      "default": "\".\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Subtree to discover"
    },
    {
      "names": [
        "--catalog"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Catalog store path; defaults to ~/.sldb"
    },
    {
      "names": [
        "--apply"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Replace catalog entries with discovered stores"
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

usage: sldb stores reconcile [-h] [--path PATH] [--catalog CATALOG] [--apply] [--format {text,json,yaml}]
