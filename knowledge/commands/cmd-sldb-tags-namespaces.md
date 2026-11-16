---
sldb:
  by: agent
  at: '2026-11-16T21:12:48Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-tags-namespaces
system: sldb
command_path: tags namespaces
synopsis: 'The declared namespaces: name, hierarchical, folder_axis, anchored_by.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#tags namespaces; contract-sha256:cc60723ec2bed0b0895bf605fc5acf154fe48d30a65bf5019c2df039b76805e1
---

# tags namespaces

## Synopsis

The declared namespaces: name, hierarchical, folder_axis, anchored_by.

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

usage: sldb tags namespaces [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
