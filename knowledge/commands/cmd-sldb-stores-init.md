---
id: cmd-sldb-stores-init
system: sldb
command_path: stores init
synopsis: Init .sldb store.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#stores init; contract-sha256:ae366f29de24a73e9855d287e9ae4095b38eb0d2ee4a4ffbc183261f0b8ac81c
---

# stores init

## Synopsis

Init .sldb store.

## Purpose

The `sldb stores init` command: Init .sldb store.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'init'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "--path"
      ],
      "required": false,
      "default": "\".\"",
      "choices": null,
      "nargs": null,
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

stores init
