---
id: cmd-sldb-graph-snapshot-save
system: sldb
command_path: graph snapshot save
synopsis: Export the store's edge index as node-link JSON.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph snapshot save; contract-sha256:f5bc2ed33dc1827460fed9550ec14077cae05b528e1f4c73d2ead5754df9ebd3
---

# graph snapshot save

## Synopsis

Export the store's edge index as node-link JSON.

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
        "--output"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Where to write the node-link JSON."
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
        "--local"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Leave the linked stores out"
    },
    {
      "names": [
        "--exclude-tag"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Leave out documents carrying this tag (repeatable)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph snapshot save [-h] --output OUTPUT [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
