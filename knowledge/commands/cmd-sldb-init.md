---
id: cmd-sldb-init
system: sldb
command_path: init
synopsis: Create a repository-local SLDB skill file.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#init; contract-sha256:74e0986dc3590370dc5c67a46bcef8cbe79f47792cb014b23d185c592e281d6f
---

# init

## Synopsis

Create a repository-local SLDB skill file.

## Purpose

The `sldb init` command: ==SUPPRESS==

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'init'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "path"
      ],
      "required": false,
      "default": "\".\"",
      "choices": null,
      "nargs": "?",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    },
    {
      "names": [
        "--force"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

init
