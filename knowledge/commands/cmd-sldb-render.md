---
id: cmd-sldb-render
system: sldb
command_path: render
synopsis: Render Markdown from data.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#render; contract-sha256:e04642ea74565f1edd927135c01b15befc97e4c91cb83b4a44e861720e075743
---

# render

## Synopsis

Render Markdown from data.

## Purpose

The `sldb render` command: Render Markdown from data.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'render'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
      "help": "Model ref: module:Class"
    },
    {
      "names": [
        "input"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Data file"
    },
    {
      "names": [
        "output"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output .md"
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
        "--ref-root"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Directory a composed field's refs resolve against (default: the working directory)."
    }
  ],
  "exclusive_groups": []
}
```

## Usage

render
