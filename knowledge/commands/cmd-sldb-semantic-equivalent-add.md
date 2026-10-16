---
id: cmd-sldb-semantic-equivalent-add
system: sldb
command_path: semantic equivalent add
synopsis: Declare LOCAL equivalent to GLOBAL.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic equivalent add; contract-sha256:eefec08e52ab01398b28f5c3c8b4823769519c63ede22222290f400f02d616d4
---

# semantic equivalent add

## Synopsis

Declare LOCAL equivalent to GLOBAL.

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
        "local"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The tag in this store"
    },
    {
      "names": [
        "global_tag"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The tag it means across linked stores"
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
        "--actor"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Who is writing, for the journal"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb semantic equivalent add [-h] [--store STORE] [--actor ACTOR] local global
