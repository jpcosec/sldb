---
id: cmd-sldb-stores-build
system: sldb
command_path: stores build
synopsis: Rebuild the store from .sldb/store.yaml, the tracked Markdown and the models.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores build; contract-sha256:af5937277739ee0a7796fba59fe02ee32cd8ce07f4050f361c8a455386787765
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
