---
sldb:
  by: agent
  at: '2026-11-15T22:21:46Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-notations-sync
system: sldb
command_path: notations sync
synopsis: Synchronize a notation, a palette, diagram specs or a vistas.yml catalog
  into the store.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations sync; contract-sha256:a1bb8a357a4ecee6c8f383e82a2892d7ec1e7615a22ed7873ee7fb1eaf3f5beb
---

# notations sync

## Synopsis

Synchronize a notation, a palette, diagram specs or a vistas.yml catalog into the store.

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
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Notation name or YAML file to sync; with --spec, the notation the specs are drawn with (`none` for none)"
    },
    {
      "names": [
        "--palette"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Palette name or YAML file to sync"
    },
    {
      "names": [
        "--spec"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Diagram spec YAML to reconcile (SpecDoc, SpecNodeDoc, RelationDoc); repeatable"
    },
    {
      "names": [
        "--catalog"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "vistas.yml whose specs are synced with their notation and catalog metadata"
    },
    {
      "names": [
        "--check"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "With --catalog: only validate it (paths, specs, notations); write nothing"
    },
    {
      "names": [
        "--prune"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "With --catalog: delete the catalog SpecDocs the vistas.yml no longer lists"
    },
    {
      "names": [
        "--strict"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "With --spec/--catalog: exit 1 when a ref does not exist or the edge index reports errors"
    },
    {
      "names": [
        "--json"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "With --spec/--catalog: print the list of reports as JSON"
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

usage: sldb notations sync [-h] [--notation NOTATION] [--palette PALETTE] [--store STORE] [--pythonpath PYTHONPATH]
