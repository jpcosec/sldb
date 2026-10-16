---
id: cmd-sldb-journal-show
system: sldb
command_path: journal show
synopsis: Show journal entries, newest first.
tags: []
provenance: parser:sldb.cli.parser:build_parser#journal show; contract-sha256:ed40f3478dd771e649fc8929df6349d62a8f452b07cf359c6242f3d5c0d09347
---

# journal show

## Synopsis

Show journal entries, newest first.

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
