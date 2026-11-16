---
sldb:
  by: agent
  at: '2026-11-16T21:10:35Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#stores init; contract-sha256:fe548b6aa93e907d8125d0a681f46e45bdc5e95b1c78cf6e6d37b7e70686ecf3
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
