---
id: cmd-sldb-notations-resolve
system: sldb
command_path: notations resolve
synopsis: Resolve documents under a notation without a SpecDoc.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations resolve; contract-sha256:d138c7b4a178328670b276d551a59052eef47b16da985e68d6ee8f5cb5d9757c
---

# notations resolve

## Synopsis

Resolve documents under a notation without a SpecDoc.

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
        "--notation"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "NotationDoc reference (e.g. NotationDoc:uml-class or uml-class)"
    },
    {
      "names": [
        "--docs"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": "+",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Document references to style (Model:name)"
    },
    {
      "names": [
        "--relations"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": "*",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Optional RelationDoc references to style"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb notations resolve [-h] --notation NOTATION --docs DOCS [DOCS ...] [--relations [RELATIONS ...]] [--store STORE] [--pythonpath PYTHONPATH]
