---
id: cmd-sldb-notations-view
system: sldb
command_path: notations view
synopsis: Resolve a SpecDoc or projection view.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations view; contract-sha256:51325b6cea4931240f149acc821153a69a70a20e57b1bc1873356ec349aac59b
---

# notations view

## Synopsis

Resolve a SpecDoc or projection view.

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
        "spec"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "SpecDoc reference (e.g. SpecDoc:arch or arch) or ViewDoc reference"
    },
    {
      "names": [
        "--projection"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Evaluate as projection view instead of SpecDoc"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb notations view [-h] [--projection] [--store STORE] [--pythonpath PYTHONPATH] spec
