---
id: cmd-sldb-lint
system: sldb
command_path: lint
synopsis: Lint knowledge references for canonical paths.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#lint; contract-sha256:3e592c55f7905f39606c20f99f4056182a64aeecafa22acd438c662442d52939
---

# lint

## Synopsis

Lint knowledge references for canonical paths.

## Purpose

The `sldb lint` command: Lint knowledge references for canonical paths.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'lint'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

```json
{
  "arguments": [
    {
      "names": [
        "target"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": "?",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "File or directory to lint (default: recursive scan of repo)"
    },
    {
      "names": [
        "--repo-root"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Repository root path (default: auto-detect from cwd)"
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

lint
