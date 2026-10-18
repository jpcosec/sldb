---
id: cmd-sldb-edges-unresolved
system: sldb
command_path: edges unresolved
synopsis: Declared references that name no document.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges unresolved; contract-sha256:fbb404fd4c01c275eec83ba386dad621eff87bef281b3753c9fa8b0be76a1f67
---

# edges unresolved

## Synopsis

Declared references that name no document.

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
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
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
        "--local"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Leave the linked stores out"
    },
    {
      "names": [
        "--exclude-tag"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Leave out documents carrying this tag (repeatable)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb edges unresolved [-h] [--format {text,json}] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
