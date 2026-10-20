---
id: cmd-sldb-anchors-record
system: sldb
command_path: anchors record
synopsis: 'What the symbol looks like now: the block an anchor keeps (code:<path>::<name>).'
tags: []
provenance: parser:sldb.cli.parser:build_parser#anchors record; contract-sha256:24b5fff36da0f8aa9b4121f7d4ad8261ac5e0f6c62f680c515ea75cfa710479f
---

# anchors record

## Synopsis

What the symbol looks like now: the block an anchor keeps (code:<path>::<name>).

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
        "ref"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "code:<path>::<qualified_name>; an empty name is the module"
    },
    {
      "names": [
        "--write"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Create (or re-record) a CodeAnchorDoc at this path, tracked in the store"
    },
    {
      "names": [
        "--claim"
      ],
      "required": false,
      "default": "\"\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "With --write: what is being said because of this symbol"
    },
    {
      "names": [
        "--name"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "With --write: document name (default: the file stem)"
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
      "default": "\"yaml\"",
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

usage: sldb anchors record [-h] [--write PATH] [--claim CLAIM] [--name NAME] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] ref
