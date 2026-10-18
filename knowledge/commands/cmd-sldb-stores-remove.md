---
id: cmd-sldb-stores-remove
system: sldb
command_path: stores remove
synopsis: Remove a store link; refused while a model here is inherited from it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores remove; contract-sha256:ad5b96a5223306c68a3695e9727f955292403c2f5964bb760491af2a2279c1ef
---

# stores remove

## Synopsis

Remove a store link; refused while a model here is inherited from it.

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
        "name"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Link name"
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
      "help": "Local store path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb stores remove [-h] [--store STORE] name
