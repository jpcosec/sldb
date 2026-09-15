---
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
provenance: parser:sldb.cli.parser:build_parser#faq; contract-sha256:3142bc75631c1825e49076fe0fe8f0a9c54e3bb6c26ae705a0f7f516809242f9
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
