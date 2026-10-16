---
id: cmd-sldb-journal-verify
system: sldb
command_path: journal verify
synopsis: Verify the journal hash chain.
tags: []
provenance: parser:sldb.cli.parser:build_parser#journal verify; contract-sha256:e39cd00e3342b9c6568059a4b70b07e9034be9bfccd5f17ef3cc077a13056f39
---

# journal verify

## Synopsis

Verify the journal hash chain.

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

usage: sldb journal verify [-h] [--store STORE] [--format {text,json,yaml}]
