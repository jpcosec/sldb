---
sldb:
  by: agent
  at: '2026-11-06T20:45:01Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#models create; contract-sha256:0b1a44bdfaf9e5bbafd908a92caaad76aac11cc600e9dd002e3372cb2a438631
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
    },
    {
      "names": [
        "--containment"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Containment mapping as JSON/YAML"
    },
    {
      "names": [
        "--references"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "References list as JSON/YAML"
    },
    {
      "names": [
        "--compositions"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Compositions mapping as JSON/YAML"
    },
    {
      "names": [
        "--semantics"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Semantics mapping as JSON/YAML"
    },
    {
      "names": [
        "--authority"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Authority string"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

models create
