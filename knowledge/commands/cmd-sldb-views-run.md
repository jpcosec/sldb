---
sldb:
  by: agent
  at: '2026-11-16T21:13:48Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-views-run
system: sldb
command_path: views run
synopsis: 'Evaluate a composed view: {view, params, revision, sections}.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#views run; contract-sha256:d6a60d5437bd9ccc5733559372bee289a14594558455825417bb3a76ef842392
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
