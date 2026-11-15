---
id: cmd-sldb-tags-namespaces
system: sldb
command_path: tags namespaces
synopsis: 'The declared namespaces: name, hierarchical, folder_axis, anchored_by.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#tags namespaces; contract-sha256:87179afb0f236ac4f384ea3d7f501c4e6f9004e9c47c4545ca17567f89a5524e
---

# tags namespaces

## Synopsis

The declared namespaces: name, hierarchical, folder_axis, anchored_by.

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

usage: sldb tags namespaces [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
