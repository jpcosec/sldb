---
sldb:
  by: agent
  at: '2026-11-16T20:56:28Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-models-check
system: sldb
command_path: models check
synopsis: Report each model as registered or missing; exit 1 if any is missing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#models check; contract-sha256:8f780a26e08eeee8a8843d138367c7bbb1f898d4800ea66ade94b8401fd7f383
---

# models check

## Synopsis

Report each model as registered or missing; exit 1 if any is missing.

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
        "models"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": "+",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Model names or refs (module:Class or module.Class)"
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

usage: sldb models check [-h] [--store STORE] [--format {text,json,yaml}] models [models ...]
