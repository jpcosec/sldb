---
sldb:
  by: agent
  at: '2026-11-16T21:10:26Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-declare
system: sldb
command_path: stores declare
synopsis: Print the store.yaml declaration the current index implies.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores declare; contract-sha256:f35105333555e2c11391b1325afe080691e1405f25912a9bcf7cc07fe3ae1430
---

# stores declare

## Synopsis

Print the store.yaml declaration the current index implies.

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
        "--write"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Write it to .sldb/store.yaml"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb stores declare [-h] [--store STORE] [--write]
