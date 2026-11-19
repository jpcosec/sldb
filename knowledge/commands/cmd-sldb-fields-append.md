---
sldb:
  by: agent
  at: '2026-11-19T08:51:48Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-fields-append
system: sldb
command_path: fields append
synopsis: Append
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#fields append; contract-sha256:c7e59cf45cda1e5b15e2eb94a0eeadf74751479287118e5579cf2f0561b8b9a9
---

# fields append

## Synopsis

Append

## Purpose

The `sldb fields append` command: Append

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'append'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "target"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "docs/<Doc>/<field> or docs/<Model>/<Doc>/<field>"
    },
    {
      "names": [
        "value"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Inline YAML/JSON value"
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
        "--string"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Take the value as literal text, without JSON/YAML parsing"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

fields append
