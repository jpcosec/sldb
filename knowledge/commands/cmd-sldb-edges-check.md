---
id: cmd-sldb-edges-check
system: sldb
command_path: edges check
synopsis: Validate every edge against its relation type.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges check; contract-sha256:accd4fb23f7e818b576dce063d9e9328740a74ae77c1583b2d0cf75aa64617e0
---

# edges check

## Synopsis

Validate every edge against its relation type.

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

usage: sldb edges check [-h] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
