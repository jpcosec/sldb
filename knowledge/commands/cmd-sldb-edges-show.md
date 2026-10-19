---
id: cmd-sldb-edges-show
system: sldb
command_path: edges show
synopsis: Edges from (or --to) a document or node.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges show; contract-sha256:bf9df8956855b86d0b8fa9ef4d84987dfde67d14dc6c2e13d8867a9383c6afe1
---

# edges show

## Synopsis

Edges from (or --to) a document or node.

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
        "node"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Export id `Model:name`, or a node id `sldb://<kind>/...`"
    },
    {
      "names": [
        "--to"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Edges pointing at the node instead of leaving it"
    },
    {
      "names": [
        "--relation"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only edges of this relation type"
    },
    {
      "names": [
        "--holds-for"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Only edges whose condition holds on this document's fields (name, path or Model/name)"
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
      "help": "Project path (to read the --holds-for document)"
    },
    {
      "names": [
        "--evidence"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Add metadata.evidence: the target's hash, the source's contract, and the engine or actor"
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
        "--local"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Leave the linked stores out"
    },
    {
      "names": [
        "--exclude-tag"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Leave out documents carrying this tag (repeatable)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb edges show [-h] [--to] [--relation RELATION] [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG] node
