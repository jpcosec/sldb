---
sldb:
  by: agent
  at: '2026-11-16T21:12:02Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-stores-semantic-map
system: sldb
command_path: stores semantic-map
synopsis: Map equivalent semantic concepts.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#stores semantic-map; contract-sha256:e960da3fb04272b980c6bce43391f71ac12f5616d4fa40321d29513069c8cb3d
---

# stores semantic-map

## Synopsis

Map equivalent semantic concepts.

## Purpose

The `sldb stores semantic-map` command: Map equivalent semantic concepts.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'semantic-map'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "concept_a"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "First concept"
    },
    {
      "names": [
        "concept_b"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Second concept"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

stores semantic-map
