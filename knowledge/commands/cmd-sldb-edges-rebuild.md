---
sldb:
  by: agent
  at: '2026-11-16T20:47:24Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-edges-rebuild
system: sldb
command_path: edges rebuild
synopsis: Bring the edge index current; only what moved is rewritten.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges rebuild; contract-sha256:2e4aa010d6932660b185fe2a06ec21a10ccabddf2c8d600c945ae02e75689b46
---

# edges rebuild

## Synopsis

Bring the edge index current; only what moved is rewritten.

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
        "--pythonpath"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Project path"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb edges rebuild [-h] [--store STORE] [--pythonpath PYTHONPATH]
