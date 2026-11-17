---
id: cmd-sldb-stores-rebuild-index
system: sldb
command_path: stores rebuild-index
synopsis: Regenerate the derived store indexes from the shards (after a merge).
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores rebuild-index; contract-sha256:8db29674ab56e843ee738e3d6013b2c3bfe454fb6f9925b6352306b4fc23c838
---

# stores rebuild-index

## Synopsis

Regenerate the derived store indexes from the shards (after a merge).

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
        "--version"
      ],
      "required": false,
      "default": "SUPPRESS",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "sldb.cli.parsers.core._VersionAction",
      "const": "null",
      "help": "print the version and the git revision, then exit"
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

usage: sldb stores rebuild-index [-h] [--store STORE]
