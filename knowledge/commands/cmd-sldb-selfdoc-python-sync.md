---
id: cmd-sldb-selfdoc-python-sync
system: sldb
command_path: selfdoc python-sync
synopsis: Track static Python symbols as reference documents.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc python-sync; contract-sha256:7250e6678a1d21d3a192b52d4dffc385ef3e86e40b19d0673ebf3d61ba1a43b6
---

# selfdoc python-sync

## Synopsis

Track static Python symbols as reference documents.

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

usage: sldb selfdoc python-sync [-h] [--source-root SOURCE_ROOT] [--package PACKAGE] [--store STORE] [--system SYSTEM] [--output OUTPUT]
