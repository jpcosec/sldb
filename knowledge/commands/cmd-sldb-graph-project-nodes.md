---
sldb:
  by: agent
  at: '2026-11-16T20:52:25Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-project-nodes
system: sldb
command_path: graph project nodes
synopsis: Every document and file node, sorted by id.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph project nodes; contract-sha256:73247644b775324da0928be69df74ec7cc819275adf6b41d33502d3b3c330838
---

# graph project nodes

## Synopsis

Every document and file node, sorted by id.

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
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only nodes of this kind"
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
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph project nodes [-h] [--kind KIND] [--store STORE] [--format {text,json,yaml}]
