---
sldb:
  by: agent
  at: '2026-11-21T08:27:48Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-rules-explain
system: sldb
command_path: rules explain
synopsis: The eval finding of one rule on one document; exit 0 true, 1 false, 3 not
  applicable.
tags: []
provenance: parser:sldb.cli.parser:build_parser#rules explain; contract-sha256:22f4cdd996301640a6f074bb650dfbc61251d68d71f53c7dbbc9e45926b42b03
---

# rules explain

## Synopsis

The eval finding of one rule on one document; exit 0 true, 1 false, 3 not applicable.

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
