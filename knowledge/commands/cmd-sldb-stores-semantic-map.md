---
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
provenance: parser:sldb.cli.parser:build_parser#stores semantic-map; contract-sha256:6adb6e5b0bc4868e2029e8ed4aa25f627a52c2ad567eb5e8772068c18c5972ab
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
