---
id: cmd-sldb-graph-order
system: sldb
command_path: graph order
synopsis: The nodes in dependency order.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph order; contract-sha256:956ad8f3d5e7c3df8c723953f0d536233ca26249c4a1f476e848cb924c385cee
---

# graph order

## Synopsis

The nodes in dependency order.

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
        "--layers"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Group the order into levels"
    },
    {
      "names": [
        "--relation"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Relation to walk, repeatable (default: the authored ones)"
    },
    {
      "names": [
        "--all-relations"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Walk every relation, derived spine included"
    },
    {
      "names": [
        "--type"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Keep only nodes of this class, repeatable"
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

usage: sldb graph order [-h] [--layers] [--relation RELATION] [--all-relations] [--type NODE_TYPE] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
