---
id: cmd-sldb-predicates-export
system: sldb
command_path: predicates export
synopsis: Write the store predicates to a YAML file (input of `predicates sync`).
tags: []
provenance: parser:sldb.cli.parser:build_parser#predicates export; contract-sha256:3e929f9422ad218772f1303a295e7dc44188d37006bba8c23132c50d9a88d345
---

# predicates export

## Synopsis

Write the store predicates to a YAML file (input of `predicates sync`).

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
        "--file"
      ],
      "required": false,
      "default": "\"-\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output file, - for stdout"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb predicates export [-h] [--file FILE] [--store STORE]
