---
sldb:
  by: agent
  at: '2026-11-16T20:49:04Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-faq
system: sldb
command_path: faq
synopsis: Browse the first-use FAQ by question.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#faq; contract-sha256:d4e29ba122449ae36773c7bec1db755c2fd32af56c40fb6736f50e1edfba0d46
---

# faq

## Synopsis

Browse the first-use FAQ by question.

## Purpose

The `sldb faq` command: Browse the first-use FAQ by question.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'faq'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "question"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": "?",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Question index, slug, or text fragment."
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
    },
    {
      "names": [
        "--faq-path"
      ],
      "required": false,
      "default": "\"docs/faq.md\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "FAQ markdown path"
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
      "help": "Store used to anchor a relative FAQ path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

faq
