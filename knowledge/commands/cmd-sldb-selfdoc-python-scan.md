---
id: cmd-sldb-selfdoc-python-scan
system: sldb
command_path: selfdoc python-scan
synopsis: Inspect static Python symbols without importing code.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc python-scan; contract-sha256:2f59ad593179060ca043fe3bdc30fdf2e07fc166d70b5181dd30f586f78738b0
---

# selfdoc python-scan

## Synopsis

Inspect static Python symbols without importing code.

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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb selfdoc python-scan [-h] [--source-root SOURCE_ROOT] [--package PACKAGE] [--store STORE]
