---
sldb:
  by: agent
  at: '2026-11-06T20:44:53Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-find
system: sldb
command_path: find
synopsis: Unified semantic + physical retrieval.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#find; contract-sha256:d7641f6337c1fab6a753be7c7f4a1449f95e43a75787d5275294d1c23d8b446f
---

# find

## Synopsis

Unified semantic + physical retrieval.

## Purpose

The `sldb find` command: Unified semantic + physical retrieval.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'find'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

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
      "help": "Resource term, semantic tag, or physical token"
    },
    {
      "names": [
        "--in"
      ],
      "required": false,
      "default": "\"both\"",
      "choices": [
        "\"semantic\"",
        "\"physical\"",
        "\"both\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Use `physical` for names, paths, section titles, and field addresses"
    },
    {
      "names": [
        "--global"
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
        "--fuzzy"
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
        "--rebuild"
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
        "--type"
      ],
      "required": false,
      "default": "\"all\"",
      "choices": [
        "\"all\"",
        "\"store\"",
        "\"model\"",
        "\"doc\"",
        "\"section\"",
        "\"field\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
    },
    {
      "names": [
        "--select"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Comma-separated projection fields"
    },
    {
      "names": [
        "--where"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Predicate (docs/architecture/rules-language.md): has(f), f = \"v\", and/or/not, any(depends_on: ...)"
    },
    {
      "names": [
        "--explain"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "With --where: add `findings` (node, holds, clause, seen) for every document evaluated"
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

find
