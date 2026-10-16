---
id: cmd-sldb-graph-query
system: sldb
command_path: graph query
synopsis: Run a structured query from a JSON file.
tags: []
provenance: parser:sldb.cli.parser:build_parser#graph query; contract-sha256:890626ad11ee6b52a5820249e26ae223135d4d64ff124495d57d6ee01c29907c
---

# graph query

## Synopsis

Run a structured query from a JSON file.

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
        "--query-file"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Path to a JSON StructuredQuery file."
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

usage: sldb graph query [-h] --query-file QUERY_FILE [--store STORE] [--local] [--exclude-tag EXCLUDE_TAG]
