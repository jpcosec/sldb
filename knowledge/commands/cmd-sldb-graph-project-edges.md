---
sldb:
  by: agent
  at: '2026-11-16T20:52:06Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-project-edges
system: sldb
command_path: graph project edges
synopsis: Declared edges leaving (--from) or reaching (--to) a node, with their provenance.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph project edges; contract-sha256:f3524501a0e722402fb0aa107dc34161549a38487ea9e38fd874a7ed1d028662
---

# graph project edges

## Synopsis

Declared edges leaving (--from) or reaching (--to) a node, with their provenance.

## Purpose

Not documented.

## How It Works

Not documented.

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
        "--from"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Edges leaving this node id"
    },
    {
      "names": [
        "--to"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Edges reaching this node id"
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
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\"",
        "\"yaml\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output format (default text)"
    }
  ],
  "exclusive_groups": [
    {
      "required": true,
      "arguments": [
        "from_id",
        "to_id"
      ]
    }
  ]
}
```

## Usage

usage: sldb graph project edges [-h] (--from ID | --to ID) [--store STORE] [--format {text,json,yaml}]
