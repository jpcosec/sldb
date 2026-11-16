---
sldb:
  by: agent
  at: '2026-11-16T21:12:38Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-tags-check
system: sldb
command_path: tags check
synopsis: The findings of builtin:tag_namespace:* over every local document, as `rules
  check` reports them; exit 1 on an error.
tags: []
provenance: parser:sldb.cli.parser:build_parser#tags check; contract-sha256:93881414955f0e4afbbf3f35c99473005b0879ce8447a34d46519111df418783
---

# tags check

## Synopsis

The findings of builtin:tag_namespace:* over every local document, as `rules check` reports them; exit 1 on an error.

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

usage: sldb tags check [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
