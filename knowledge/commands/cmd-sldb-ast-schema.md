---
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
provenance: parser:sldb.cli.parser:build_parser#ast schema; contract-sha256:f36bb2571f3b2ad66865dfd3fb5e2d1b34dd4f3f5cb009623984737a41cd1054
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
