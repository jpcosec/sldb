---
id: cmd-sldb-anchors-check
system: sldb
command_path: anchors check
synopsis: Every anchor of the store against the code now; reads only, unless --record.
tags: []
provenance: parser:sldb.cli.parser:build_parser#anchors check; contract-sha256:ca2930871bf398d38ad19e20e1dd0a002fd4ca15d6fcc3af60b86473a5513f49
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
