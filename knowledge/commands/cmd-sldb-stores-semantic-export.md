---
sldb:
  by: agent
  at: '2026-11-16T21:11:49Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#stores semantic-export; contract-sha256:31ed7d2348b38461ae6b66bb0f32cc8493380654dd2f28d9dd36d87181899431
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
