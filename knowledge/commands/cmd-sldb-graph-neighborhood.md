---
sldb:
  by: agent
  at: '2026-11-16T20:51:39Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-neighborhood
system: sldb
command_path: graph neighborhood
synopsis: Nodes within a depth of a starting node.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph neighborhood; contract-sha256:cb2cd8993839a3951adc02b70d865b7ec415a76fd1f37e62c55469fad7012c99
---

# graph neighborhood

## Synopsis

Nodes within a depth of a starting node.

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
        "node"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Starting node id."
    },
    {
      "names": [
        "--depth"
      ],
      "required": false,
      "default": "1",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Hops to traverse (default 1)."
    },
    {
      "names": [
        "--direction"
      ],
      "required": false,
      "default": "\"both\"",
      "choices": [
        "\"incoming\"",
        "\"outgoing\"",
        "\"both\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Direction to traverse."
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

usage: sldb graph neighborhood [-h] [--depth DEPTH] [--direction {incoming,outgoing,both}] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG] node
