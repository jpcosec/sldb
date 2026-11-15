---
id: cmd-sldb-docs-replace
system: sldb
command_path: docs replace
synopsis: Replace exactly N occurrences of a literal text in a tracked document (validated
  and tracked again) or in a plain file under the project root.
tags: []
provenance: parser:sldb.cli.parser:build_parser#docs replace; contract-sha256:377a86d05df89446a44d85fb06c352f2a94f5d0c6c9d04055d68d3efbf38aa43
---

# docs replace

## Synopsis

Replace exactly N occurrences of a literal text in a tracked document (validated and tracked again) or in a plain file under the project root.

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
        "ref"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name, Model/DocName or tracked path; else a path relative to the project root"
    },
    {
      "names": [
        "--old"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The literal text to replace (not a regex)"
    },
    {
      "names": [
        "--new"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Its replacement"
    },
    {
      "names": [
        "--count"
      ],
      "required": false,
      "default": "1",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Exactly how many non-overlapping occurrences there must be (default 1)"
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

usage: sldb docs replace [-h] --old OLD --new NEW [--count COUNT] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] ref
