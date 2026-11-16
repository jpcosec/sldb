---
sldb:
  by: agent
  at: '2026-11-16T21:01:42Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-predicates-sync
system: sldb
command_path: predicates sync
synopsis: Make the store match a versioned predicates file (create/update; --prune
  removes the rest).
tags: []
provenance: parser:sldb.cli.parser:build_parser#predicates sync; contract-sha256:f695dda2876ff235517df94c5bdeefb4a9fdcbe85bb25275e0cea7ec0d05c3da
---

# predicates sync

## Synopsis

Make the store match a versioned predicates file (create/update; --prune removes the rest).

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
        "--file"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "YAML file: name -> {axis, description}; - for stdin"
    },
    {
      "names": [
        "--prune"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Remove store predicates absent from the file"
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

usage: sldb predicates sync [-h] --file FILE [--prune] [--store STORE]
