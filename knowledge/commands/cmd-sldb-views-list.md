---
id: cmd-sldb-views-list
system: sldb
command_path: views list
synopsis: 'The composed views: name, title, params and section keys.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#views list; contract-sha256:181eeb617005806c8be9e25b751bb3d8265066073678f570c5c07cfc2862855f
---

# views list

## Synopsis

The composed views: name, title, params and section keys.

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
        "--pythonpath"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Directory to import models from"
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
      "help": "Output format (default text)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb views list [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
