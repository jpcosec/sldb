---
id: cmd-sldb-explore
system: sldb
command_path: explore
synopsis: Search markdown docs and Python docstrings.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#explore; contract-sha256:a613761e9381bfba81be759c3d73d96bc020a8bc3adc8211be387b3b949bd905
---

# explore

## Synopsis

Search markdown docs and Python docstrings.

## Purpose

The `sldb explore` command: Search markdown docs and Python docstrings.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'explore'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "term"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Search term or regex"
    },
    {
      "names": [
        "--source"
      ],
      "required": false,
      "default": "\"all\"",
      "choices": [
        "\"all\"",
        "\"docs\"",
        "\"docstrings\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    },
    {
      "names": [
        "--regex"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": ""
    },
    {
      "names": [
        "--docs-root"
      ],
      "required": false,
      "default": "\"docs\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Docs directory to scan"
    },
    {
      "names": [
        "--code-root"
      ],
      "required": false,
      "default": "\"src\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Python source directory to scan"
    },
    {
      "names": [
        "--max-results"
      ],
      "required": false,
      "default": "20",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
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
      "help": "Store used to anchor relative source roots"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

explore
