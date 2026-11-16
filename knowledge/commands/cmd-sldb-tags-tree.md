---
sldb:
  by: agent
  at: '2026-11-16T21:12:57Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-tags-tree
system: sldb
command_path: tags tree
synopsis: 'One namespace''s tags as a tree: roots (nested by prefix), orphans and
  unplaced.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#tags tree; contract-sha256:56ae8fbd3a31625d683e2317ee5466a401b30737803a4f5b859ecd8d3a7cdf5a
---

# tags tree

## Synopsis

One namespace's tags as a tree: roots (nested by prefix), orphans and unplaced.

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
        "namespace"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "A declared namespace, e.g. area"
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

usage: sldb tags tree [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] namespace
