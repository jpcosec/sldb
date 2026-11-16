---
sldb:
  by: agent
  at: '2026-11-16T20:59:34Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-notations-list
system: sldb
command_path: notations list
synopsis: List notations or projection views in the store or builtins.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations list; contract-sha256:e9ff5a3254adfe4e149b8204ba101fc0815b750b3a5a7eb24399b581a9ce18e6
---

# notations list

## Synopsis

List notations or projection views in the store or builtins.

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
        "--views"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "List projection views instead of notations"
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
        "--pythonpath"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Project path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb notations list [-h] [--views] [--store STORE] [--pythonpath PYTHONPATH]
