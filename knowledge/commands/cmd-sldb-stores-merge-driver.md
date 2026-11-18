---
sldb:
  by: agent
  at: '2026-11-18T04:51:30Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-merge-driver
system: sldb
command_path: stores merge-driver
synopsis: Git merge driver for .sldb/ files; --install registers it in this clone.
tags: []
provenance: parser:sldb.cli.parser:build_parser#stores merge-driver; contract-sha256:6e11246f3f48d8a8dbab79101487559f5c3648e25285716facbb1a0741ce8570
---

# stores merge-driver

## Synopsis

Git merge driver for .sldb/ files; --install registers it in this clone.

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
        "files"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": "*",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Base, current (result), other and merged path, as git passes them"
    },
    {
      "names": [
        "--install"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Write .gitattributes lines and set merge.sldb.driver in .git/config (idempotent)"
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
      "help": "Store path (for --install)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb stores merge-driver [-h] [--install] [--store STORE] [%O %A %B %P ...]
