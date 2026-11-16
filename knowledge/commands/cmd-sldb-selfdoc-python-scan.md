---
sldb:
  by: agent
  at: '2026-11-16T21:07:14Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-selfdoc-python-scan
system: sldb
command_path: selfdoc python-scan
synopsis: Inspect static Python symbols without importing code.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc python-scan; contract-sha256:d2fc0a0d02be2311015523ef5d1a8c10a84bc5f49f127bc8e85629419b9aced6
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
