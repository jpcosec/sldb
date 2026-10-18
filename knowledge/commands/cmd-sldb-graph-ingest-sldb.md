---
id: cmd-sldb-graph-ingest-sldb
system: sldb
command_path: graph ingest-sldb
synopsis: Convert an sldb semantic export into node-link JSON.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph ingest-sldb; contract-sha256:55542eae4a3756a0507e3c4ecae9c4da716f1f16c7241e050dab81418cc51019
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
      "help": "The sldb_semantic_export JSON file."
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
