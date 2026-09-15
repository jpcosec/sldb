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
provenance: parser:sldb.cli.parser:build_parser#serve; contract-sha256:8870c19f460bf1dd636e7c56d19b084013febc33b8efc31c81c0641fcc6b6b1d
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

serve
