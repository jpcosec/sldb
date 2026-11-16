---
sldb:
  by: agent
  at: '2026-11-16T20:45:07Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#docs compose; contract-sha256:7014891075e243296b572c7a82fd5aca047ebad62ee06e2c873d0dfb45848ee6
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
