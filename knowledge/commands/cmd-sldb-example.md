---
sldb:
  by: agent
  at: '2026-11-16T20:48:06Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-example
system: sldb
command_path: example
synopsis: Unpack the bundled SLDB reference example.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#example; contract-sha256:28e34d9fa377fb466bb21992bf82ce49af035e191c27a4b92009adb917236f79
---

# example

## Synopsis

Unpack the bundled SLDB reference example.

## Purpose

The `sldb example` command: ==SUPPRESS==

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'example'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

example
