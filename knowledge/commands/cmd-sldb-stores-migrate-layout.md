---
id: cmd-sldb-stores-migrate-layout
system: sldb
command_path: stores migrate-layout
synopsis: Move the cache from .sldb/runtime/ to .sldb_cache/ (sibling of .sldb/),
  drop the journal and fix the root .gitignore.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores migrate-layout; contract-sha256:97c78383a7e3368fceea9ee2172682e7e31a8e48233450bfda7259e13fd55df3
---

# stores migrate-layout

## Synopsis

Move the cache from .sldb/runtime/ to .sldb_cache/ (sibling of .sldb/), drop the journal and fix the root .gitignore.

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
        "--force"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Replace an existing, non-empty .sldb_cache/"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb stores migrate-layout [-h] [--store STORE] [--force]
