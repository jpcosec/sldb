---
id: cmd-sldb-selfdoc-python-check
system: sldb
command_path: selfdoc python-check
synopsis: Report static Python documentation drift without writing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc python-check; contract-sha256:7d5a66705e28347f28d20d36a44029c42891ff14c18a083cd37040a91a3db8ed
---

# selfdoc python-check

## Synopsis

Report static Python documentation drift without writing.

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
        "--source-root"
      ],
      "required": false,
      "default": "\"src\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Python root relative to selected store"
    },
    {
      "names": [
        "--package"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Optional package prefix for stable IDs"
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
      "help": "Store used to anchor source root"
    },
    {
      "names": [
        "--architecture-spec"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Explicit spec2viz YAML relative to store root"
    },
    {
      "names": [
        "--graph-output"
      ],
      "required": false,
      "default": "\".sldb/runtime/graphs/python-source.graph.json\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Source graph (node-link JSON) relative to the store root"
    },
    {
      "names": [
        "--system"
      ],
      "required": false,
      "default": "\"sldb\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Stable lowercase tool identifier"
    },
    {
      "names": [
        "--output"
      ],
      "required": false,
      "default": "\"knowledge\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Documentation directory relative to the store root"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb selfdoc python-check [-h] [--source-root SOURCE_ROOT] [--package PACKAGE] [--store STORE] [--system SYSTEM] [--output OUTPUT]
