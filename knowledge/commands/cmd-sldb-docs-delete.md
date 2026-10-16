---
id: cmd-sldb-docs-delete
system: sldb
command_path: docs delete
synopsis: Untrack a doc AND delete its Markdown file.
tags: []
provenance: parser:sldb.cli.parser:build_parser#docs delete; contract-sha256:3d6796a92c3e104a905c3f72eaefe8e064b1f2c2553f170b7933440b668ffffa
---

# docs delete

## Synopsis

Untrack a doc AND delete its Markdown file.

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
      "help": "Doc name or tracked path"
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
        "--yes"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Do not ask for confirmation"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb docs delete [-h] [--store STORE] [--pythonpath PYTHONPATH] [--yes] doc
