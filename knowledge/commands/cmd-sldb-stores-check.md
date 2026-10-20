---
sldb:
  by: agent
  at: '2026-10-20T17:12:38Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#stores check; contract-sha256:425d7a107e2d19a4fbc62a33367ad90c94818f0dab5cfd731ddfa55a7efadb9a
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
        "--apply"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Run what the store's policy answers to each finding: `reindex` and `hook: <command>`"
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
