---
sldb:
  by: agent
  at: '2026-11-16T20:54:08Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-journal-show
system: sldb
command_path: journal show
synopsis: 'Retired: prints the notice and exits 0.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#journal show; contract-sha256:eabdf0dfe4ab399a7488ed047fb3deb7eda39fabb3e867da321425d0d60ab95f
---

# journal show

## Synopsis

Retired: prints the notice and exits 0.

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
        "--limit"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Max entries to show"
    },
    {
      "names": [
        "--since"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "ISO UTC timestamp; only entries at or after it"
    },
    {
      "names": [
        "--address"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only entries for this 'Model:doc' address"
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\"",
        "\"yaml\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb journal show [-h] [--store STORE] [--limit LIMIT] [--since SINCE] [--address ADDRESS] [--format {text,json,yaml}]
