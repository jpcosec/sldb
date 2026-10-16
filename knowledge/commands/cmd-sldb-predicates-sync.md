---
id: cmd-sldb-predicates-sync
system: sldb
command_path: predicates sync
synopsis: Make the store match a versioned predicates file (create/update; --prune
  removes the rest).
tags: []
provenance: parser:sldb.cli.parser:build_parser#predicates sync; contract-sha256:1c564728d7a93f8bba3ed61f0dda16d77cb88f385a16dcde73872e8f36a85c69
---

# predicates sync

## Synopsis

Make the store match a versioned predicates file (create/update; --prune removes the rest).

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
        "--file"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "YAML file: name -> {axis, description}; - for stdin"
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
      "help": "Remove store predicates absent from the file"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb predicates sync [-h] --file FILE [--prune] [--store STORE]
