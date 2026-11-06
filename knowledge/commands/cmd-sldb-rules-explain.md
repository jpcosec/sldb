---
id: cmd-sldb-rules-explain
system: sldb
command_path: rules explain
synopsis: The eval finding of one rule on one document; exit 0 true, 1 false, 2 incomplete,
  3 not applicable.
tags: []
provenance: parser:sldb.cli.parser:build_parser#rules explain; contract-sha256:b1b42b245dd52a7df45e965c36881d0e836a269209fd70320463fda55f31996d
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
