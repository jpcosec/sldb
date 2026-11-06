---
id: cmd-sldb-rules-check
system: sldb
command_path: rules check
synopsis: Report each failing rule as a finding; exit 1 only on an error.
tags: []
provenance: parser:sldb.cli.parser:build_parser#rules check; contract-sha256:f6456a6e92186480572e9c1faa3fd885db9e2de433e56824554b3a227c7f031c
---

# rules check

## Synopsis

Report each failing rule as a finding; exit 1 only on an error.

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
        "--subject"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only this document (Model:name, store:Model:name or path), every rule of any moment"
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
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb rules check [-h] [--subject SUBJECT] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
