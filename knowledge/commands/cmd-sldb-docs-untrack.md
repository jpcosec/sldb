---
sldb:
  by: agent
  at: '2026-11-16T20:46:44Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-docs-untrack
system: sldb
command_path: docs untrack
synopsis: Remove a tracked doc from the store, keeping its file.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#docs untrack; contract-sha256:65230938ad36cf3f8becaa63f3fd196d2bae9cf33b7e8d6c936c9cce5d4c8cde
---

# docs untrack

## Synopsis

Remove a tracked doc from the store, keeping its file.

## Purpose

The `sldb docs untrack` command: Remove a tracked doc from the store.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'untrack'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "doc"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name or tracked path"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

docs untrack
