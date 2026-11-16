---
sldb:
  by: agent
  at: '2026-11-16T21:11:37Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-scaffold
system: sldb
command_path: stores scaffold
synopsis: Create the folders and seed files .sldb/store.yaml declares; without --apply,
  report what is pending.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores scaffold; contract-sha256:3bcae7ecd5f202759fa8a0def6c416a3a4ca2d2515000d93bbd2c1fb20060446
---

# stores scaffold

## Synopsis

Create the folders and seed files .sldb/store.yaml declares; without --apply, report what is pending.

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
        "--apply"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Write them (default: report only)"
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

usage: sldb stores scaffold [-h] [--store STORE] [--apply] [--format {text,json,yaml}]
