---
sldb:
  by: agent
  at: '2026-11-16T20:55:51Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-mcp
system: sldb
command_path: mcp
synopsis: Serve the store to an MCP client over stdio (needs the `mcp` extra).
tags: []
provenance: parser:sldb.cli.parser:build_parser#mcp; contract-sha256:12e6075545b816a1b2c6bdce3a212889d37577bbe110c24ce6941fabc34e4a91
---

# mcp

## Synopsis

Serve the store to an MCP client over stdio (needs the `mcp` extra).

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
        "--store"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "The store directory (`<project>/.sldb`)."
    },
    {
      "names": [
        "--level"
      ],
      "required": false,
      "default": "0",
      "choices": [
        "0",
        "1",
        "2"
      ],
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Write level: 0 read only (default), 1 content, 2 rules as data."
    },
    {
      "names": [
        "--actor"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Who signs what this server writes (the global --actor, default agent:sldb-mcp)."
    },
    {
      "names": [
        "--extension"
      ],
      "required": false,
      "default": "[]",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Register the tools of a consumer: MODULE:FUNCTION is called as function(server, context). Repeatable."
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb mcp [-h] --store STORE [--level {0,1,2}] [--actor ACTOR] [--extension MODULE:FUNCTION]
