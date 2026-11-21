---
sldb:
  by: agent
  at: '2026-11-21T02:21:47Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-notations-from-graph
system: sldb
command_path: notations from-graph
synopsis: Compile an sldb graph (snapshot JSON or store index) or a Python tree into
  a component spec.
tags: []
provenance: parser:sldb.cli.parser:build_parser#notations from-graph; contract-sha256:0c840f2c2e96d75e0f140a0657f02a25a02eb3e564572bffa8253584e5f98168
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
        "--label-field"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Payload field that gives each document node its label (default: the document id). Needs --store; a --snapshot has no payload, only the id and the model"
    },
    {
      "names": [
        "--kind-field"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Payload field, or tag:<namespace> (the first tag '<namespace>:x' gives 'x'), that gives each document node its kind (default: the model). Needs --store"
    },
    {
      "names": [
        "--group-field"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Payload field or tag:<namespace>: documents with the same value go into one container node (kind 'group') with contains edges. Needs --store"
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
