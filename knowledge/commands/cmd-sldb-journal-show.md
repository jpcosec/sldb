---
sldb:
  by: agent
  at: '2026-11-06T20:45:00Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-journal-show
system: sldb
command_path: journal show
synopsis: 'Retired: prints the notice and exits 0.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#journal show; contract-sha256:8b393ff4b1edd63c2b8a6eae17808cb78e9a19cf49ffeb1a9039b9c7f16e56e4
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
