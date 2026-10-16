---
id: cmd-sldb-serve
system: sldb
command_path: serve
synopsis: Serve the store over HTTP using the same methods as the CLI.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#serve; contract-sha256:5e0a5281eea874003c108026b2a999676f80d85a74106e8e7fe0dc4b2fac8f69
---

# serve

## Synopsis

Serve the store over HTTP using the same methods as the CLI.

## Purpose

The `sldb serve` command: Serve the store over HTTP using the same methods as the CLI.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'serve'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "--host"
      ],
      "required": false,
      "default": "\"127.0.0.1\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    },
    {
      "names": [
        "--port"
      ],
      "required": false,
      "default": "8787",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
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
        "--cors"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Send permissive CORS headers (for browser clients)"
    },
    {
      "names": [
        "--token"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Require 'Authorization: Bearer <TOKEN>' on every request (default: $SLDB_SERVE_TOKEN, or no auth)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

serve
