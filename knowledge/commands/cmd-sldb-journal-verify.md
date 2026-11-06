---
sldb:
  by: agent
  at: '2026-11-06T20:45:00Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-journal-verify
system: sldb
command_path: journal verify
synopsis: 'Retired: prints the notice and exits 0.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#journal verify; contract-sha256:61be786ec36e0159069712ecb2df976ceb62625d7f3de6f37b0b5035ac1a71b2
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
