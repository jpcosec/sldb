---
id: cmd-sldb-stores-check
system: sldb
command_path: stores check
synopsis: 'Integrity check: reports each finding and its category.'
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#stores check; contract-sha256:4b7b0dfbbfcc5baf149e9f8a167dabe8d5abc97ba00421a2e34b5220d1fe72b6
---

# stores check

## Synopsis

Integrity check: reports each finding and its category.

## Purpose

The `sldb stores check` command: Integrity check.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'check'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
    },
    {
      "names": [
        "--quiet"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Only the PASS/FAIL line, without per-document findings"
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

stores check
