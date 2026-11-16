---
sldb:
  by: agent
  at: '2026-11-16T21:11:18Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-reconcile
system: sldb
command_path: stores reconcile
synopsis: Explicitly reconcile a catalog against a subtree.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores reconcile; contract-sha256:e77979c68b26526a2b8f4cd1aaebc0946f6acd54f6c43c8d646321f00f4f6b57
---

# stores reconcile

## Synopsis

Explicitly reconcile a catalog against a subtree.

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
        "--path"
      ],
      "required": false,
      "default": "\".\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Subtree to discover"
    },
    {
      "names": [
        "--catalog"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Catalog store path; defaults to ~/.sldb"
    },
    {
      "names": [
        "--apply"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Replace catalog entries with discovered stores"
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\"",
        "\"yaml\""
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

usage: sldb stores reconcile [-h] [--path PATH] [--catalog CATALOG] [--apply] [--format {text,json,yaml}]
