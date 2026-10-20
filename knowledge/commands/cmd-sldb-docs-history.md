---
id: cmd-sldb-docs-history
system: sldb
command_path: docs history
synopsis: 'The document''s committed versions from git: who signed each one and which
  fields moved.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#docs history; contract-sha256:40049783962f3f24df9116b8138d209af7f61d2fb4ae9a39ef7c6f24971c2a53
---

# docs history

## Synopsis

The document's committed versions from git: who signed each one and which fields moved.

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
        "doc"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name or Model/DocName or tracked path"
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
      "help": "Only versions committed at or after this ISO date"
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

usage: sldb docs history [-h] [--since SINCE] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] doc
