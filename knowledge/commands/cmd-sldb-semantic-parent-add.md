---
sldb:
  by: agent
  at: '2026-11-06T20:45:08Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-semantic-parent-add
system: sldb
command_path: semantic parent add
synopsis: Declare TAG a kind of PARENT.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic parent add; contract-sha256:5ecc0fa518fea0295a510d0c3c5672e0f283dec474865f2062d846e84d2565eb
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
      "help": "Who is writing (accepted for compatibility; the journal was retired on 2026-11-04)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb semantic parent add [-h] [--store STORE] [--actor ACTOR] tag parent
