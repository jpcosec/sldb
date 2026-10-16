---
id: cmd-sldb-edges-show
system: sldb
command_path: edges show
synopsis: Edges from (or --to) a document or node.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges show; contract-sha256:e1a325e7caecfa7e860d831c51a3259e680507cf9558ed090df942a25c0dda54
---

# edges show

## Synopsis

Edges from (or --to) a document or node.

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
        "node"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Export id `Model:name`, or a node id `sldb://<kind>/...`"
    },
    {
      "names": [
        "--to"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Edges pointing at the node instead of leaving it"
    },
    {
      "names": [
        "--relation"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only edges of this relation type"
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

usage: sldb edges show [-h] [--to] [--relation RELATION] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG] node
