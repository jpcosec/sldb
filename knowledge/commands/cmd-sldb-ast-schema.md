---
sldb:
  by: agent
  at: '2026-11-16T20:44:27Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-ast-schema
system: sldb
command_path: ast schema
synopsis: Show node and edge schema.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#ast schema; contract-sha256:b7942350944b9b7a382d47201bd9f2000c52ad32f91ec62e8531401b2ee04c6b
---

# ast schema

## Synopsis

Show node and edge schema.

## Purpose

The `sldb ast schema` command: Show node and edge schema.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'schema'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "--format"
      ],
      "required": false,
      "default": "\"json\"",
      "choices": [
        "\"json\"",
        "\"yaml\"",
        "\"text\""
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

ast schema
