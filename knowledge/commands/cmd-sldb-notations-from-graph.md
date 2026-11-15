---
id: cmd-sldb-notations-from-graph
system: sldb
command_path: notations from-graph
synopsis: Compile an sldb graph (snapshot JSON or store index) or a Python tree into
  a component spec.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations from-graph; contract-sha256:cbab49dd2d9752c23b2b287abf0f23fc0485edc7c47aa4dc1f8cc1ffa6791073
---

# notations from-graph

## Synopsis

Compile an sldb graph (snapshot JSON or store index) or a Python tree into a component spec.

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
        "--snapshot"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Node-link JSON (`sldb graph snapshot save`, or the Python source graph of `sldb selfdoc python-sync`)"
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
      "help": "Read the edge index of this .sldb (or project) dir via sldb.api"
    },
    {
      "names": [
        "--python"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Directory of .py files, scanned with sldb.code (extra [code]); nodes module/class/external"
    },
    {
      "names": [
        "--node-type"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Node type to keep (document, model, semantic_tag, ...); repeatable. Default: document, model"
    },
    {
      "names": [
        "--model"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Keep only documents of this model (e.g. AtomDoc); repeatable"
    },
    {
      "names": [
        "--relation"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Keep only these relations; repeatable. Overrides the default exclusions"
    },
    {
      "names": [
        "--exclude-relation"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Drop this relation; repeatable. Default: structural relations"
    },
    {
      "names": [
        "--drop-isolated"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Drop nodes left without edges after filtering"
    },
    {
      "names": [
        "--module-prefix"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Keep only Python nodes of this module or below; repeatable. With --python, the one root package"
    },
    {
      "names": [
        "--id"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Spec id. Defaults to the file stem, 'sldb-graph', or the parent dir of --python"
    },
    {
      "names": [
        "--title"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Spec title. Defaults to '<id> graph' ('<id> AST Architecture' with --python)"
    },
    {
      "names": [
        "--output"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Write the YAML spec here instead of stdout"
    }
  ],
  "exclusive_groups": [
    {
      "required": true,
      "arguments": [
        "snapshot",
        "store",
        "python"
      ]
    }
  ]
}
```

## Usage

usage: sldb notations from-graph [-h] (--snapshot SNAPSHOT | --store STORE | --python PYTHON) [--node-type NODE_TYPES] [--model MODELS] [--relation RELATIONS] [--exclude-relation EXCLUDE_RELATIONS] [--drop-isolated] [--module-prefix MODULE_PREFIXES] [--id SPEC_ID] [--title TITLE] [--output OUTPUT]
