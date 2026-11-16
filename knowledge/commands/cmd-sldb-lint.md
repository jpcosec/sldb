---
sldb:
  by: agent
  at: '2026-11-16T20:55:32Z'
  authority: generated
  via: save_document_payload
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
provenance: parser:sldb.cli.parser:build_parser#lint; contract-sha256:d6f5a58f282387f65533ac029658b88c5f9b369a61000197125b881f1172e879
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
