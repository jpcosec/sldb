---
sldb:
  by: agent
  at: '2026-11-16T21:02:10Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#render; contract-sha256:90766ef79e1d59b6b053022cb5cc72c7f39f6d0eae46edec0b3fea5ae73a2040
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
