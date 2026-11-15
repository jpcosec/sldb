---
id: cmd-sldb-graph-project-edges
system: sldb
command_path: graph project edges
synopsis: Declared edges leaving (--from) or reaching (--to) a node, with their provenance.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph project edges; contract-sha256:6629d39c63720c06b948f63c217719f48782454a48cdc1f486fa77d69ebe1084
---

# graph project edges

## Synopsis

Declared edges leaving (--from) or reaching (--to) a node, with their provenance.

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
        "--from"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Edges leaving this node id"
    },
    {
      "names": [
        "--to"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Edges reaching this node id"
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
  "exclusive_groups": [
    {
      "required": true,
      "arguments": [
        "from_id",
        "to_id"
      ]
    }
  ]
}
```

## Usage

usage: sldb graph project edges [-h] (--from ID | --to ID) [--store STORE] [--format {text,json,yaml}]
