---
id: cmd-sldb-models-metadata-edit
system: sldb
command_path: models metadata edit
synopsis: Edit model metadata in draft.
tags: []
provenance: parser:sldb.cli.parser:build_parser#models metadata edit; contract-sha256:1bb04ccd84807ee8c6fdcf1617aa1f80f56cf657d7113e68a82adcd6ed0fdea4
---

# models metadata edit

## Synopsis

Edit model metadata in draft.

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
        "--containment"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Containment mapping as JSON/YAML text or file"
    },
    {
      "names": [
        "--references"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "References list as JSON/YAML text or file"
    },
    {
      "names": [
        "--compositions"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Compositions mapping as JSON/YAML text or file"
    },
    {
      "names": [
        "--semantics"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Semantics mapping as JSON/YAML text or file"
    },
    {
      "names": [
        "--authority"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Authority string"
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

usage: sldb models metadata edit [-h] [--containment CONTAINMENT] [--references REFERENCES] [--compositions COMPOSITIONS] [--semantics SEMANTICS] [--authority AUTHORITY] [--store STORE] [--pythonpath PYTHONPATH] model
