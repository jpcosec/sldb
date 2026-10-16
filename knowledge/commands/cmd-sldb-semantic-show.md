---
id: cmd-sldb-semantic-show
system: sldb
command_path: semantic show
synopsis: A tag's parents, children, and everything above and below it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic show; contract-sha256:3f21a2ab7ba88d1723b5646e1cc9d128c5e15dfc158897ace5d325351def2595
---

# semantic show

## Synopsis

A tag's parents, children, and everything above and below it.

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
        "tag"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The tag"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb semantic show [-h] [--store STORE] tag
