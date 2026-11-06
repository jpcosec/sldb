---
sldb:
  by: agent
  at: '2026-11-06T20:45:08Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-semantic-equivalent-add
system: sldb
command_path: semantic equivalent add
synopsis: Declare LOCAL equivalent to GLOBAL.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic equivalent add; contract-sha256:5218d13bd4268f6677a54ab3a18e79567e8f4091a086c7b97a0c55828d2af4c1
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
      "help": "Who is writing (accepted for compatibility; the journal was retired on 2026-11-04)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb semantic equivalent add [-h] [--store STORE] [--actor ACTOR] local global
