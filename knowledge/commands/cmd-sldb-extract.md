---
sldb:
  by: agent
  at: '2026-11-16T20:48:43Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-extract
system: sldb
command_path: extract
synopsis: Extract data from Markdown.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#extract; contract-sha256:a8b25c282a96dad4240383b7a334cd3f73d29f6993791c8d82b11669b5168d66
---

# extract

## Synopsis

Extract data from Markdown.

## Purpose

The `sldb extract` command: Extract data from Markdown.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'extract'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "model"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Model ref: module:Class"
    },
    {
      "names": [
        "input"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Markdown file"
    },
    {
      "names": [
        "output"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output JSON/YAML"
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "null",
      "choices": [
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
        "--pythonpath"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Project path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

extract
