---
sldb:
  by: agent
  at: '2026-11-16T20:45:30Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-docs-exists
system: sldb
command_path: docs exists
synopsis: Check that a doc reference resolves, here or in a linked store, without
  importing it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#docs exists; contract-sha256:85781d6338c117a3135b05d1cd9e0273bad620e4c18efc538e1fe11eadeac214
---

# docs exists

## Synopsis

Check that a doc reference resolves, here or in a linked store, without importing it.

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
        "ref"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name, Model/DocName or tracked path; 'alias:ref' for a directly linked store"
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
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb docs exists [-h] [--store STORE] [--format {text,json}] ref
