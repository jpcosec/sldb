---
id: cmd-sldb-selfdoc-python-check
system: sldb
command_path: selfdoc python-check
synopsis: Report static Python documentation drift without writing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc python-check; contract-sha256:e2839beb38b6830576bc61058a920a625f16043c7dd1ee37bd382e2dbca4f5b0
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
        "--kgdb-output"
      ],
      "required": false,
      "default": "\".kgdb/python-source.graph.json\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "KGDB graph relative to the store root"
    },
    {
      "names": [
        "--kgdb-command"
      ],
      "required": false,
      "default": "\"kgdb\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "KGDB executable used by python-sync"
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
