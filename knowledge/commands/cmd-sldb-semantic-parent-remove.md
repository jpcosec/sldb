---
sldb:
  by: agent
  at: '2026-11-16T21:08:47Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-semantic-parent-remove
system: sldb
command_path: semantic parent remove
synopsis: Undeclare it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic parent remove; contract-sha256:ee7696b9a6e0aa0cdc70488d8266add918fed1d1d08777f0124c4614f813f60c
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
        "--version"
      ],
      "required": false,
      "default": "SUPPRESS",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "sldb.cli.parsers.core._VersionAction",
      "const": "null",
      "help": "print the version and the git revision, then exit"
    },
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
