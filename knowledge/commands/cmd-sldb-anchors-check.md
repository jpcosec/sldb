---
sldb:
  by: agent
  at: '2026-11-16T20:44:02Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-anchors-check
system: sldb
command_path: anchors check
synopsis: Every anchor of the store against the code now; reads only, unless --record.
tags: []
provenance: parser:sldb.cli.parser:build_parser#anchors check; contract-sha256:731a8a4e1d5bb11cc66e09ffb4ef3d16a070f2650bdb7b5f57379c7dacb16c3f
---

# anchors check

## Synopsis

Every anchor of the store against the code now; reads only, unless --record.

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
        "--record"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Write the reconnections into the anchors (new ref, a history entry); the only write"
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
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb anchors check [-h] [--record] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}]
