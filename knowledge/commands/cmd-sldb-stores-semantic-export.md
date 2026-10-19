---
id: cmd-sldb-stores-semantic-export
system: sldb
command_path: stores semantic-export
synopsis: Export semantic payloads.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#stores semantic-export; contract-sha256:e2151bfd4c7dfb041ee9b3f144d2b25e8c003472c98bcd2f3bcd77923f17d317
---

# stores semantic-export

## Synopsis

Export semantic payloads.

## Purpose

The `sldb stores semantic-export` command: Export semantic payloads.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'semantic-export'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "\"sldb\"",
      "choices": [
        "\"sldb\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Payload contract: sldb_kgdb_semantic_export v1"
    },
    {
      "names": [
        "--encoding"
      ],
      "required": false,
      "default": "\"json\"",
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
        "--output",
        "-o"
      ],
      "required": false,
      "default": "\"-\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output path or -"
    },
    {
      "names": [
        "--rebuild"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Refresh semantic and section indexes"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

stores semantic-export
