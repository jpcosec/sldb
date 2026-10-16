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
provenance: parser:sldb.cli.parser:build_parser#docs compose; contract-sha256:0a2f934e0913cf383209ade835624281091a95292c721cb36b0e15df8c7a33e8
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
    },
    {
      "names": [
        "--render-links"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Turn [[x]] into Markdown links relative to the output file"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

docs compose
