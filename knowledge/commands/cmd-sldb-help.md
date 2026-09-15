---
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
provenance: parser:sldb.cli.parser:build_parser#help; contract-sha256:3a232bac71000b48414029113e6c0651e15a539fe9609d760f282d62fb6e89a7
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
