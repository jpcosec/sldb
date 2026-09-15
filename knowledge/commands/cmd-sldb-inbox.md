---
id: cmd-sldb-inbox
system: sldb
command_path: inbox
synopsis: Log unclear points or suggestions into the repo desk.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#inbox; contract-sha256:b37fc2b83589982b1a055c20bfd6530f3c12e39a9b782fc5064574784b15ec1c
---

# inbox

## Synopsis

Log unclear points or suggestions into the repo desk.

## Purpose

The `sldb inbox` command: Log unclear points or suggestions into the repo desk.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'inbox'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "message"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": "?",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Inbox note body"
    },
    {
      "names": [
        "--kind"
      ],
      "required": false,
      "default": "\"unclear\"",
      "choices": [
        "\"unclear\"",
        "\"suggestion\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Type of desk note to write"
    },
    {
      "names": [
        "--title"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Short title for the note"
    },
    {
      "names": [
        "--desk-root"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Desk root directory override"
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
      "help": "Store path used to resolve the target project root"
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
      "help": "Project path used when auto-tracking inbox notes"
    },
    {
      "names": [
        "--author"
      ],
      "required": false,
      "default": "\"cli\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Source label for the inbox note"
    },
    {
      "names": [
        "--list"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "List desk inbox notes"
    },
    {
      "names": [
        "--show"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Show one inbox note"
    },
    {
      "names": [
        "--limit"
      ],
      "required": false,
      "default": "20",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Limit listed notes"
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

inbox
