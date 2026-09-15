---
id: cmd-sldb-example
system: sldb
command_path: example
synopsis: Unpack the bundled SLDB reference example.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#example; contract-sha256:a79207ee248dc6268dcdffa7431d62e7825f5eaee5bb3a5c50f26f499f072125
---

# example

## Synopsis

Unpack the bundled SLDB reference example.

## Purpose

The `sldb example` command: ==SUPPRESS==

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'example'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "path"
      ],
      "required": false,
      "default": "\".\"",
      "choices": null,
      "nargs": "?",
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

example
