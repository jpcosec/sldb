---
sldb:
  by: agent
  at: '2026-11-16T21:00:52Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-predicates-export
system: sldb
command_path: predicates export
synopsis: Write the store predicates to a YAML file (input of `predicates sync`).
tags: []
provenance: parser:sldb.cli.parser:build_parser#predicates export; contract-sha256:85986eda715810423c53432b0469f140f34058a8dd910c4f242bddf703c012c0
---

# predicates export

## Synopsis

Write the store predicates to a YAML file (input of `predicates sync`).

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
        "--file"
      ],
      "required": false,
      "default": "\"-\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output file, - for stdout"
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

usage: sldb predicates export [-h] [--file FILE] [--store STORE]
