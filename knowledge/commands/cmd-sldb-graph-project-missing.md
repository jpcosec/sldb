---
sldb:
  by: agent
  at: '2026-11-16T20:52:16Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-graph-project-missing
system: sldb
command_path: graph project missing
synopsis: Declared targets that resolve to no node, with where each is declared.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph project missing; contract-sha256:9fddee2db98430518678bbd550310927e021a26c6d709d477fcbe2ed58bafee7
---

# graph project missing

## Synopsis

Declared targets that resolve to no node, with where each is declared.

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

usage: sldb graph project missing [-h] [--store STORE] [--format {text,json,yaml}]
