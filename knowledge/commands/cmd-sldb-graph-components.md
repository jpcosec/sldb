---
id: cmd-sldb-graph-components
system: sldb
command_path: graph components
synopsis: What hangs together, and what hangs alone.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph components; contract-sha256:8f4591854dffeee319c0e6a3abf2a52f23f882cc1518c5791f11aa22f91f5595
---

# graph components

## Synopsis

What hangs together, and what hangs alone.

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
        "--islands"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Only the groups outside the largest one"
    },
    {
      "names": [
        "--isolated"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Only the nodes with no edge at all"
    },
    {
      "names": [
        "--relation"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Relation to walk, repeatable (default: the authored ones)"
    },
    {
      "names": [
        "--all-relations"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Walk every relation, derived spine included"
    },
    {
      "names": [
        "--type"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Keep only nodes of this class, repeatable"
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
        "--local"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Leave the linked stores out"
    },
    {
      "names": [
        "--exclude-tag"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Leave out documents carrying this tag (repeatable)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph components [-h] [--islands] [--isolated] [--relation RELATION] [--all-relations] [--type NODE_TYPE] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
