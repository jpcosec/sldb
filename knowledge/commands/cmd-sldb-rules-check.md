---
sldb:
  by: agent
  at: '2026-11-16T21:04:23Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-rules-check
system: sldb
command_path: rules check
synopsis: Report each failing rule as a finding; exit 1 only on an error.
tags: []
provenance: parser:sldb.cli.parser:build_parser#rules check; contract-sha256:54e7d7c8835851e9a64f68e37a14d320464477672c8b10aa65281414694bb487
---

# rules check

## Synopsis

Report each failing rule as a finding; exit 1 only on an error.

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
        "--subject"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only this document (Model:name, store:Model:name or path), every rule of any moment"
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

usage: sldb rules check [-h] [--subject SUBJECT] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
