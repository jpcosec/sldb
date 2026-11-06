---
sldb:
  by: agent
  at: '2026-11-06T20:45:07Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-selfdoc-python-scan
system: sldb
command_path: selfdoc python-scan
synopsis: Inspect static Python symbols without importing code.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc python-scan; contract-sha256:4cc4ed1ec9c41d75270d8b3765a6295895346f5e3f1f7d2754f1f6bf39f31066
---

# selfdoc python-scan

## Synopsis

Inspect static Python symbols without importing code.

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
        "--source-root"
      ],
      "required": false,
      "default": "\"src\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Python root relative to selected store"
    },
    {
      "names": [
        "--package"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Optional package prefix for stable IDs"
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
      "help": "Store used to anchor source root"
    },
    {
      "names": [
        "--architecture-spec"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Explicit spec2viz YAML relative to store root"
    },
    {
      "names": [
        "--graph-output"
      ],
      "required": false,
      "default": "\".sldb_cache/graphs/python-source.graph.json\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Source graph (node-link JSON) relative to the project root"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb selfdoc python-scan [-h] [--source-root SOURCE_ROOT] [--package PACKAGE] [--store STORE]
