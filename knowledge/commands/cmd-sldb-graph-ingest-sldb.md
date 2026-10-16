---
id: cmd-sldb-graph-ingest-sldb
system: sldb
command_path: graph ingest-sldb
synopsis: Convert an sldb semantic export into node-link JSON.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph ingest-sldb; contract-sha256:522269e66ac777403d15f9e816700875ec483d8f7bbe93d96b807739ff292d6f
---

# graph ingest-sldb

## Synopsis

Convert an sldb semantic export into node-link JSON.

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
        "--input"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The sldb_kgdb_semantic_export JSON file."
    },
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph ingest-sldb [-h] --input INPUT --output OUTPUT
