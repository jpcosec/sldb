---
sldb:
  by: agent
  at: '2026-11-16T20:51:31Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-list
system: sldb
command_path: graph list
synopsis: All node ids in the store's edge index.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph list; contract-sha256:d99b3a12edb34f30a25ebaf877293cd8e6e6b6d2f0268ccd3cffd48a9b0c0b98
---

# graph list

## Synopsis

All node ids in the store's edge index.

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
        "--local"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Leave the linked stores out"
    },
    {
      "names": [
        "--exclude-tag"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Leave out documents carrying this tag (repeatable)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph list [-h] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
