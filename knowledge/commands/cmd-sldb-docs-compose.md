---
id: cmd-sldb-docs-compose
system: sldb
command_path: docs compose
synopsis: Expand ![[transclusions]] into composed Markdown.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#docs compose; contract-sha256:58356de5b808e28368e8565dc5e39d1c463ba6ef3fba1a0184d592ced47e5511
---

# docs compose

## Synopsis

Expand ![[transclusions]] into composed Markdown.

## Purpose

The `sldb docs compose` command: Expand ![[transclusions]] into composed Markdown.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'compose'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
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
      "help": "Output path or - for stdout"
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

docs compose
