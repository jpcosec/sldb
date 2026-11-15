---
id: cmd-sldb-graph-project-nodes
system: sldb
command_path: graph project nodes
synopsis: Every document and file node, sorted by id.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph project nodes; contract-sha256:5d2803945d4a27600d1f969a03f686ec6d25eccfdac49d3126de8da2edb1b137
---

# graph project nodes

## Synopsis

Every document and file node, sorted by id.

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
        "--kind"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only nodes of this kind"
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
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph project nodes [-h] [--kind KIND] [--store STORE] [--format {text,json,yaml}]
