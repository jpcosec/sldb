---
id: cmd-sldb-stores-scaffold
system: sldb
command_path: stores scaffold
synopsis: Create the folders and seed files .sldb/store.yaml declares; without --apply,
  report what is pending.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores scaffold; contract-sha256:9fd19bc23d9d49d84dbac157e87d206f8bc5b41bf6489cbdcced808446bfb53a
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
