---
sldb:
  by: agent
  at: '2026-11-16T20:51:23Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-ingest-sldb
system: sldb
command_path: graph ingest-sldb
synopsis: Convert an sldb semantic export into node-link JSON.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph ingest-sldb; contract-sha256:ca8ff870e442912ef50601e7360662edc36182bc4925018b11e19663d67f39b4
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
        "--version"
      ],
      "required": false,
      "default": "SUPPRESS",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "sldb.cli.parsers.core._VersionAction",
      "const": "null",
      "help": "print the version and the git revision, then exit"
    },
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
