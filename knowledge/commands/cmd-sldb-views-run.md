---
id: cmd-sldb-views-run
system: sldb
command_path: views run
synopsis: 'Evaluate a composed view: {view, params, revision, sections}.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#views run; contract-sha256:af6cb3a20e7f2dcfc1df5c5faa740d1f444fb162538f2fd34bf0c096406598f1
---

# views run

## Synopsis

Evaluate a composed view: {view, params, revision, sections}.

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
        "name"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The view's name (ViewDoc:<name>)"
    },
    {
      "names": [
        "--param"
      ],
      "required": false,
      "default": "{}",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "sldb.cli.parsers.views.ParamAction",
      "const": "null",
      "help": "A param value (repeatable); every value is a string"
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

usage: sldb views run [-h] [--param KEY=VALUE] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] name
