---
sldb:
  by: agent
  at: '2026-11-16T20:47:40Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-edges-rewrite
system: sldb
command_path: edges rewrite
synopsis: Rewrite (--to) or remove (--remove) every reference to a document or project
  node, all or nothing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges rewrite; contract-sha256:40bb48bc7a408d195698c0fb413225d8bd12f07053e694a4b2e8ef0e4d641c4e
---

# edges rewrite

## Synopsis

Rewrite (--to) or remove (--remove) every reference to a document or project node, all or nothing.

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
        "target"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "As in `edges referrers`"
    },
    {
      "names": [
        "--to"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The replacement: resolved like TARGET (each value keeps its form), else written as given"
    },
    {
      "names": [
        "--remove"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Remove the references: a scalar field becomes null, a list loses the element, a mention is reported as skipped"
    },
    {
      "names": [
        "--dry-run"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Report what would change, validated in memory, without writing"
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
  "exclusive_groups": [
    {
      "required": true,
      "arguments": [
        "to",
        "remove"
      ]
    }
  ]
}
```

## Usage

usage: sldb edges rewrite [-h] (--to NEW | --remove) [--dry-run] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] target
