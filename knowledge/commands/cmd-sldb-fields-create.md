---
id: cmd-sldb-fields-create
system: sldb
command_path: fields create
synopsis: Create
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#fields create; contract-sha256:f16e020a25aa686c92d9beda66e41b536b8f9c223627b1309bd38dad0d5713f5
---

# fields create

## Synopsis

Create

## Purpose

The `sldb fields create` command: Create

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'create'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

fields create
