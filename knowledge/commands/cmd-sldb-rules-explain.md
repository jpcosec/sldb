---
sldb:
  by: agent
  at: '2026-11-16T21:04:42Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-rules-explain
system: sldb
command_path: rules explain
synopsis: The eval finding of one rule on one document; exit 0 true, 1 false, 2 incomplete,
  3 not applicable.
tags: []
provenance: parser:sldb.cli.parser:build_parser#rules explain; contract-sha256:d85ab27aafb8ab7592421e061dfcf208443925e27dbda8bc04a8693c7a57c016
---

# rules explain

## Synopsis

The eval finding of one rule on one document; exit 0 true, 1 false, 2 incomplete, 3 not applicable.

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
        "rule"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "RuleDoc:<name>, <name> or the rule's path"
    },
    {
      "names": [
        "subject"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Model:name, store:Model:name or the document's path"
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
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb rules explain [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] rule subject
