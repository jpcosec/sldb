---
id: cmd-sldb-legacy-recover
system: sldb
command_path: legacy recover
synopsis: Recover links.
tags: []
provenance: parser:sldb.cli.parser:build_parser#legacy recover; contract-sha256:40e7a3f23c0583b8c65f7b1d6ebfd121d0563392b0c1c0a4cf33bb1a3f97f29d
---

# legacy recover

## Synopsis

Recover links.

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
        "doc"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name or path"
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
      "help": ""
    },
    {
      "names": [
        "--depth"
      ],
      "required": false,
      "default": "1",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Recovery depth (default: 1)"
    },
    {
      "names": [
        "--links-only"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Only return link targets"
    },
    {
      "names": [
        "--include-transclusions"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": ""
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb legacy recover [-h] [--store STORE] [--format {text,json,yaml}]
                           [--depth DEPTH] [--links-only]
                           [--include-transclusions]
                           doc
