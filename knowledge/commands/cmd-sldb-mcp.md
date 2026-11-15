---
id: cmd-sldb-mcp
system: sldb
command_path: mcp
synopsis: Serve the store to an MCP client over stdio (needs the `mcp` extra).
tags: []
provenance: parser:sldb.cli.parser:build_parser#mcp; contract-sha256:6a0232b148816ddab9121e23905270aa70b16d08c7b3c488ce806366bc11b251
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
