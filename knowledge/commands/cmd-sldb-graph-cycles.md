---
sldb:
  by: agent
  at: '2026-11-16T20:51:06Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-cycles
system: sldb
command_path: graph cycles
synopsis: Cycles in a relation that should be a DAG.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph cycles; contract-sha256:55e8be358c2cb023a5d9b59d9df46ee0a089fe1b15aba7fa66fdfdf2aabe818c
---

# graph cycles

## Synopsis

Cycles in a relation that should be a DAG.

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
        "--limit"
      ],
      "required": false,
      "default": "10",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "How many cycles to print (default 10)"
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

usage: sldb graph cycles [-h] [--limit LIMIT] [--relation RELATION] [--all-relations] [--type NODE_TYPE] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
