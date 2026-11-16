---
sldb:
  by: agent
  at: '2026-11-16T20:53:06Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-help
system: sldb
command_path: help
synopsis: Curated CLI help.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#help; contract-sha256:881fa6ebe51dcbc3297882736fcef2bf0a7f8756ab90f5c89979b3ab617cee1c
---

# help

## Synopsis

Curated CLI help.

## Purpose

The `sldb help` command: Curated CLI help.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'help'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "topic"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": "?",
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "stores, models, predicates, docs, fields, sections, ast, find, faq, inbox, explore, selfdoc, legacy"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

help
