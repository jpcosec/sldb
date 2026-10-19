---
id: cmd-sldb-stores-declare
system: sldb
command_path: stores declare
synopsis: Print the store.yaml declaration the current index implies.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores declare; contract-sha256:f1dd54df014027317bf4b776c06fabbf4dc9c8f179951d863fb38951c68ca202
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
