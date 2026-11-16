---
sldb:
  by: agent
  at: '2026-11-16T21:01:21Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-predicates-remove
system: sldb
command_path: predicates remove
synopsis: Remove a predicate definition.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#predicates remove; contract-sha256:7f33e4bf736bab2dd7a5b84172c1c916a904e583ed306c1eb9d9f1517e39eadf
---

# predicates remove

## Synopsis

Remove a predicate definition.

## Purpose

The `sldb predicates remove` command: Remove a predicate definition.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'remove'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
        "name"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Predicate name"
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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

predicates remove
