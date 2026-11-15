---
id: cmd-sldb-edges-rewrite
system: sldb
command_path: edges rewrite
synopsis: Rewrite (--to) or remove (--remove) every reference to a document or project
  node, all or nothing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges rewrite; contract-sha256:aece50113f5d5c4752c5e38fe5cc93a2207c8b7323ea16a1c48ba1e38465bca1
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
