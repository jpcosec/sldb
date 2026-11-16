---
sldb:
  by: agent
  at: '2026-11-16T20:54:17Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-journal-verify
system: sldb
command_path: journal verify
synopsis: 'Retired: prints the notice and exits 0.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#journal verify; contract-sha256:0a6c3d16b91e705fe83c953caddb0995870e8d74704524cc9c5d679a986c9958
---

# journal verify

## Synopsis

Retired: prints the notice and exits 0.

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

usage: sldb journal verify [-h] [--store STORE] [--format {text,json,yaml}]
