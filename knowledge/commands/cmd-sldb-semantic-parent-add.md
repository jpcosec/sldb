---
id: cmd-sldb-semantic-parent-add
system: sldb
command_path: semantic parent add
synopsis: Declare TAG a kind of PARENT.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic parent add; contract-sha256:8da991ab4ab581975dbaf6ae5601a640c83913ac3706a49ffdd52b20758f489b
---

# semantic parent add

## Synopsis

Declare TAG a kind of PARENT.

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

usage: sldb semantic parent add [-h] [--store STORE] [--actor ACTOR] tag parent
