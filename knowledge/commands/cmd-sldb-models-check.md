---
id: cmd-sldb-models-check
system: sldb
command_path: models check
synopsis: Report each model as registered or missing; exit 1 if any is missing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#models check; contract-sha256:3b8b383c84650f22625e1beab8c3c1f62a1ad22430df08657220ac15a773a9c3
---

# models check

## Synopsis

Report each model as registered or missing; exit 1 if any is missing.

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
        "models"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": "+",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Model names or refs (module:Class or module.Class)"
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

usage: sldb models check [-h] [--store STORE] [--format {text,json,yaml}] models [models ...]
