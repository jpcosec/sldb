---
id: cmd-sldb-docs-show
system: sldb
command_path: docs show
synopsis: Show document AST and payload.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#docs show; contract-sha256:4cb248fa827d7603f6faddde979b93c945c5a1d8889f738cb4990efc62b6a550
---

# docs show

## Synopsis

Show document AST and payload.

## Purpose

The `sldb docs show` command: Show document AST and payload.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
      "help": "Doc name or Model/DocName or tracked path; 'alias:ref' for a directly linked store"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

docs show
