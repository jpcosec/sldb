---
id: cmd-sldb-models-create
system: sldb
command_path: models create
synopsis: Generate a StructuredNLDoc model.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#models create; contract-sha256:5e5f6a4838d1f3ba3dfd8cb153f2753338153aae5c0da8c81571ce49258e0508
---

# models create

## Synopsis

Generate a StructuredNLDoc model.

## Purpose

The `sldb models create` command: Generate a StructuredNLDoc model.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'create'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "name"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Class name"
    },
    {
      "names": [
        "--template"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Template markdown path"
    },
    {
      "names": [
        "--fields"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Field spec YAML path"
    },
    {
      "names": [
        "--output"
      ],
      "required": false,
      "default": "\"-\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output Python file or -"
    },
    {
      "names": [
        "--stdout"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Print generated code"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

models create
