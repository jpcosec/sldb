---
sldb:
  by: agent
  at: '2026-11-16T21:13:39Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-views-list
system: sldb
command_path: views list
synopsis: 'The composed views: name, title, params and section keys.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#views list; contract-sha256:2f2dc9453cf8a01b4936712daf00e8261f09dfb0313f956dd731ede72b59b944
---

# views list

## Synopsis

The composed views: name, title, params and section keys.

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
      "help": "Directory to import models from"
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

usage: sldb views list [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
