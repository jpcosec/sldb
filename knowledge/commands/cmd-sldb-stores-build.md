---
sldb:
  by: agent
  at: '2026-11-16T21:10:04Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-build
system: sldb
command_path: stores build
synopsis: Rebuild the store from .sldb/store.yaml, the tracked Markdown and the models.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores build; contract-sha256:17ec9bef6dade13079f77c29ce3befe2425d7e0167fc16b1a3f933e3545fa93e
---

# stores build

## Synopsis

Rebuild the store from .sldb/store.yaml, the tracked Markdown and the models.

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
        "--check"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Rebuild a scratch copy of the sources and compare, writing nothing here"
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
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb stores build [-h] [--store STORE] [--check] [--format {text,json,yaml}]
