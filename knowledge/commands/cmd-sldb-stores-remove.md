---
sldb:
  by: agent
  at: '2026-11-16T21:11:27Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-remove
system: sldb
command_path: stores remove
synopsis: Remove a store link; refused while a model here is inherited from it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores remove; contract-sha256:d72379d29ed31229a8a6e6b433d7efb63e2916a511c1f58a759e7a05f1807093
---

# stores remove

## Synopsis

Remove a store link; refused while a model here is inherited from it.

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
        "name"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Link name"
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
      "help": "Local store path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb stores remove [-h] [--store STORE] name
