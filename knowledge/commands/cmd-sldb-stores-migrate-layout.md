---
sldb:
  by: agent
  at: '2026-11-16T21:11:07Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-migrate-layout
system: sldb
command_path: stores migrate-layout
synopsis: Move the cache from .sldb/runtime/ to .sldb_cache/ (sibling of .sldb/),
  drop the journal and fix the root .gitignore.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores migrate-layout; contract-sha256:f5ad792ae4b6d6449497e36a7dd7d1be28e011c9ab65258ebcddc09ef2b088c6
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
