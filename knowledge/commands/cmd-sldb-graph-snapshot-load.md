---
sldb:
  by: agent
  at: '2026-11-16T20:52:49Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-snapshot-load
system: sldb
command_path: graph snapshot load
synopsis: Read a node-link or snapshot JSON file.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph snapshot load; contract-sha256:cb273bcaf87b5a4eff8d047251a53f7eb408e1cd46a4cbb65d56ee30036d636e
---

# graph snapshot load

## Synopsis

Read a node-link or snapshot JSON file.

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
        "--input"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The node-link or snapshot JSON file."
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph snapshot load [-h] --input INPUT
