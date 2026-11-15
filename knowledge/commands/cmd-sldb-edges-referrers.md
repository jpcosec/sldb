---
id: cmd-sldb-edges-referrers
system: sldb
command_path: edges referrers
synopsis: 'Every reference to a document or project node: declared fields (scalar
  or list element) and mentions in prose.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges referrers; contract-sha256:733aa6178b3188e25515bc2d02df42f076966a7ee520aa377a0633d79310e82f
---

# edges referrers

## Synopsis

Every reference to a document or project node: declared fields (scalar or list element) and mentions in prose.

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
        "target"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name, Model/name, Model:name, tracked path, or a project graph node id (kind:identity)"
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

usage: sldb edges referrers [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] target
