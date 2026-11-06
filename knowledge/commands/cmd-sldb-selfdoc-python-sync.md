---
sldb:
  by: agent
  at: '2026-11-06T20:45:07Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-selfdoc-python-sync
system: sldb
command_path: selfdoc python-sync
synopsis: Track static Python symbols as reference documents.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc python-sync; contract-sha256:65902c2d3bd7857833f0ece9b7647c86c80733fd8935d523e2b48b758a1f8edb
---

# selfdoc python-sync

## Synopsis

Track static Python symbols as reference documents.

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
    },
    {
      "names": [
        "--system"
      ],
      "required": false,
      "default": "\"sldb\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Stable lowercase tool identifier"
    },
    {
      "names": [
        "--output"
      ],
      "required": false,
      "default": "\"knowledge\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Documentation directory relative to the store root"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb selfdoc python-sync [-h] [--source-root SOURCE_ROOT] [--package PACKAGE] [--store STORE] [--system SYSTEM] [--output OUTPUT]
