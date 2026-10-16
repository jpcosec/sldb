---
id: cmd-sldb-semantic-parent-remove
system: sldb
command_path: semantic parent remove
synopsis: Undeclare it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic parent remove; contract-sha256:3b46fa4618f800b0dd4638a1bb5a806bd81193490c7e4d58d9c78cbbdfbbed50
---

# semantic parent remove

## Synopsis

Undeclare it.

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
      "help": "The tag, e.g. layer.topology"
    },
    {
      "names": [
        "parent"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "What it is a kind of, e.g. type.knowledge"
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

usage: sldb semantic parent remove [-h] [--store STORE] [--actor ACTOR] tag parent
