---
sldb:
  by: agent
  at: '2026-11-16T20:50:49Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-central
system: sldb
command_path: graph central
synopsis: Which nodes the rest of the store leans on.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph central; contract-sha256:c912cc6f9183f40e10bc539f5aed14206bf2632fc710c297d7735821973933cc
---

# graph central

## Synopsis

Which nodes the rest of the store leans on.

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
        "--kind"
      ],
      "required": false,
      "default": "\"pagerank\"",
      "choices": [
        "\"pagerank\"",
        "\"betweenness\"",
        "\"degree\"",
        "\"in_degree\"",
        "\"out_degree\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "How to measure (default pagerank)"
    },
    {
      "names": [
        "--limit"
      ],
      "required": false,
      "default": "20",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "How many nodes to print (default 20)"
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

usage: sldb graph central [-h] [--kind {pagerank,betweenness,degree,in_degree,out_degree}] [--limit LIMIT] [--relation RELATION] [--all-relations] [--type NODE_TYPE] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
