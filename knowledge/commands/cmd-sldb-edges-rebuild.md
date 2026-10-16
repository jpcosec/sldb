---
id: cmd-sldb-edges-rebuild
system: sldb
command_path: edges rebuild
synopsis: Bring the edge index current; only what moved is rewritten.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges rebuild; contract-sha256:66c142041f3ea4a5fdab267403f1a2924f31f0c68fe0c771dd069a1d448e972f
---

# edges rebuild

## Synopsis

Bring the edge index current; only what moved is rewritten.

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

usage: sldb edges rebuild [-h] [--store STORE] [--pythonpath PYTHONPATH]
