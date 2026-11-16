---
sldb:
  by: agent
  at: '2026-11-16T20:59:47Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-notations-resolve
system: sldb
command_path: notations resolve
synopsis: Resolve documents under a notation without a SpecDoc.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations resolve; contract-sha256:dc213fd4a50326e82513e1361912e6b37b3af114779fb535d525357047afbb5b
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
