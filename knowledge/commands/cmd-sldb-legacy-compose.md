---
id: cmd-sldb-legacy-compose
system: sldb
command_path: legacy compose
synopsis: Compose transclusions.
tags: []
provenance: parser:sldb.cli.parser:build_parser#legacy compose; contract-sha256:0695742089fd09f86ef7123b8d55cca214b58b510981263e3528d2acc31f8e80
---

# legacy compose

## Synopsis

Compose transclusions.

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
        "doc"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name or path"
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
        "-o",
        "--output"
      ],
      "required": false,
      "default": "\"-\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "\"markdown\"",
      "choices": [
        "\"markdown\"",
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

usage: sldb legacy compose [-h] [--store STORE] [-o OUTPUT]
                           [--format {markdown,json,yaml}]
                           doc
