---
sldb:
  by: agent
  at: '2026-11-16T21:00:09Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-notations-view
system: sldb
command_path: notations view
synopsis: Resolve a SpecDoc or projection view.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations view; contract-sha256:255efdc0d421256aced68d833d2b8a3540fb6185babc809e65a64a6018e63c18
---

# notations view

## Synopsis

Resolve a SpecDoc or projection view.

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
        "spec"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "SpecDoc reference (e.g. SpecDoc:arch or arch) or ViewDoc reference"
    },
    {
      "names": [
        "--projection"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Evaluate as projection view instead of SpecDoc"
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

usage: sldb notations view [-h] [--projection] [--store STORE] [--pythonpath PYTHONPATH] spec
