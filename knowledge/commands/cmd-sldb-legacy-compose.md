---
sldb:
  by: agent
  at: '2026-11-16T20:54:34Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-legacy-compose
system: sldb
command_path: legacy compose
synopsis: Compose transclusions.
tags: []
provenance: parser:sldb.cli.parser:build_parser#legacy compose; contract-sha256:e74e5adcfee18d6a8017b0d40d4e952e630585a55d71e22a07016b57199c411e
---

# legacy compose

## Synopsis

Compose transclusions.

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
        "doc"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name or path"
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
        "-o",
        "--output"
      ],
      "required": false,
      "default": "\"-\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "\"markdown\"",
      "choices": [
        "\"markdown\"",
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

usage: sldb legacy compose [-h] [--store STORE] [-o OUTPUT]
                           [--format {markdown,json,yaml}]
                           doc
