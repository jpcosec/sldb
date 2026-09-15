---
id: cmd-sldb-models-template-show
system: sldb
command_path: models template show
synopsis: Show the active or draft template.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#models template show; contract-sha256:8a3f72775c491b2c32f7f4c1e93095f93a9d6762b0ea188e4362e7b9e755765e
---

# models template show

## Synopsis

Show the active or draft template.

## Purpose

The `sldb models template show` command: Show the active or draft template.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'show'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
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
      "help": "Model name"
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
        "--draft"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Show the draft template"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

models template show
