---
id: cmd-sldb-graph-project-missing
system: sldb
command_path: graph project missing
synopsis: Declared targets that resolve to no node, with where each is declared.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph project missing; contract-sha256:39d91daf8ed49394348622b5a950c853c8c2f57c798f964228649eae2c7c0dcd
---

# graph project missing

## Synopsis

Declared targets that resolve to no node, with where each is declared.

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
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\"",
        "\"yaml\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Output format (default text)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb graph project missing [-h] [--store STORE] [--format {text,json,yaml}]
