---
sldb:
  by: agent
  at: '2026-11-16T20:53:42Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#init; contract-sha256:9697092f003eaf68726658fa0a048c0430f11c9aa212e514bb15d6da968ded88
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
