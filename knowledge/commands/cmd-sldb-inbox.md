---
sldb:
  by: agent
  at: '2026-11-16T20:53:25Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#inbox; contract-sha256:86f7c85a69ff1c87a3fde7cada1a131a181e20f8faaa7fe9ff2eb1025e3f15f4
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
