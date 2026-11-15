---
id: cmd-sldb-tags-check
system: sldb
command_path: tags check
synopsis: The findings of builtin:tag_namespace:* over every local document, as `rules
  check` reports them; exit 1 on an error.
tags: []
provenance: parser:sldb.cli.parser:build_parser#tags check; contract-sha256:8f62642282e6add6fdc43cb369eeaf10a229ee93e3fadc5714c38716d84cf1f9
---

# tags check

## Synopsis

The findings of builtin:tag_namespace:* over every local document, as `rules check` reports them; exit 1 on an error.

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

usage: sldb tags check [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
