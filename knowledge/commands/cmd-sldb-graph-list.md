---
id: cmd-sldb-graph-list
system: sldb
command_path: graph list
synopsis: All node ids in the store's edge index.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph list; contract-sha256:d3c480533f3a56836623595ecf935624e9bfaad94f956c1e50051bbc8c11cd3a
---

# graph list

## Synopsis

All node ids in the store's edge index.

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

usage: sldb graph list [-h] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
