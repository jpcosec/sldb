---
id: cmd-sldb-graph-get
system: sldb
command_path: graph get
synopsis: One node from the store's edge index.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph get; contract-sha256:8a7daa5deb0e5615f0243a4727b6dc7e84ea4f6e0115b82feba080537eed251e
---

# graph get

## Synopsis

One node from the store's edge index.

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
      "help": "Node id `sldb://<kind>/...` or export id `Model:name`."
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

usage: sldb graph get [-h] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG] node
