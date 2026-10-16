---
id: cmd-sldb-edges-init
system: sldb
command_path: edges init
synopsis: Register RelationTypeDoc/RelationDoc and track the builtin relation types.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges init; contract-sha256:446d219c7dedb1841f3ef75a24e7a614ba0d2845634e8680f806e2a8672fa6f5
---

# edges init

## Synopsis

Register RelationTypeDoc/RelationDoc and track the builtin relation types.

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
      "help": "Project path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb edges init [-h] [--store STORE] [--pythonpath PYTHONPATH]
