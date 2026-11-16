---
sldb:
  by: agent
  at: '2026-11-16T20:45:23Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-docs-delete
system: sldb
command_path: docs delete
synopsis: Untrack a doc AND delete its Markdown file.
tags: []
provenance: parser:sldb.cli.parser:build_parser#docs delete; contract-sha256:990c8943e91b2cbe7e5dcc1840bc9b0fb7359b23b5eb0299ae44b7dcf15021c1
---

# docs delete

## Synopsis

Untrack a doc AND delete its Markdown file.

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
        "doc"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name or tracked path"
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
    },
    {
      "names": [
        "--yes"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Do not ask for confirmation"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb docs delete [-h] [--store STORE] [--pythonpath PYTHONPATH] [--yes] doc
