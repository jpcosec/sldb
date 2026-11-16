---
sldb:
  by: agent
  at: '2026-11-16T20:57:55Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-models-remove
system: sldb
command_path: models remove
synopsis: Unregister a model; refused while it tracks documents unless --with-documents.
tags: []
provenance: parser:sldb.cli.parser:build_parser#models remove; contract-sha256:75d8c836b3232e6a1815de3f2802cc35fee94f744d9b8d043b9fb02301a5c30e
---

# models remove

## Synopsis

Unregister a model; refused while it tracks documents unless --with-documents.

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
        "--with-documents"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Also untrack its documents (files stay); the class need not import"
    },
    {
      "names": [
        "model"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Model name"
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

usage: sldb models remove [-h] [--store STORE] [--pythonpath PYTHONPATH] model
