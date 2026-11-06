---
sldb:
  by: agent
  at: '2026-11-06T20:45:09Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-semantic-parent-remove
system: sldb
command_path: semantic parent remove
synopsis: Undeclare it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic parent remove; contract-sha256:2e311605e5bedff645d76feb29340dd4fe6c4c98ccff6541592d3307100409b2
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
      "help": "Who is writing (accepted for compatibility; the journal was retired on 2026-11-04)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb semantic parent remove [-h] [--store STORE] [--actor ACTOR] tag parent
