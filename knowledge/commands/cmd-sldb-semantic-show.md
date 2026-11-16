---
sldb:
  by: agent
  at: '2026-11-16T21:08:59Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-semantic-show
system: sldb
command_path: semantic show
synopsis: A tag's parents, children, and everything above and below it.
tags: []
provenance: parser:sldb.cli.parser:build_parser#semantic show; contract-sha256:74844fa1b131058fdfc5f9abbe1c5538e0e2f0699f570485044b932e836d42de
---

# semantic show

## Synopsis

A tag's parents, children, and everything above and below it.

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
        "tag"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The tag"
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

usage: sldb semantic show [-h] [--store STORE] tag
