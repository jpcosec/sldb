---
sldb:
  by: agent
  at: '2026-11-16T21:10:56Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-migrate-hashes
system: sldb
command_path: stores migrate-hashes
synopsis: Rename hash_a..hash_d to store/model/source/content.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores migrate-hashes; contract-sha256:c560a97cff7917240e71b3c79273f6f392582347e4238c36884b9c2d455a8d88
---

# stores migrate-hashes

## Synopsis

Rename hash_a..hash_d to store/model/source/content.

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

usage: sldb stores migrate-hashes [-h] [--store STORE]
