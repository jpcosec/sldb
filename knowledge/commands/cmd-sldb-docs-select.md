---
sldb:
  by: agent
  at: '2026-11-16T20:46:20Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-docs-select
system: sldb
command_path: docs select
synopsis: Which tracked documents a selector names (keys combined by conjunction).
tags: []
provenance: parser:sldb.cli.parser:build_parser#docs select; contract-sha256:65b86734e84b7ab6a6f69f6ba5aec4f413f273f1965c382f40742f402775bc10
---

# docs select

## Synopsis

Which tracked documents a selector names (keys combined by conjunction).

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
        "--ref"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name, Model/DocName, Model:DocName or tracked path; 'alias:ref' reaches a directly linked store"
    },
    {
      "names": [
        "--prefix"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Name prefix; with --one an exact name wins over the prefix matches"
    },
    {
      "names": [
        "--path-glob"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Shell pattern over the path relative to the project root ('**' crosses directories)"
    },
    {
      "names": [
        "--model"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "A model name: it and every model extending it"
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
      "help": "A predicate of the rules language over the indexed payload"
    },
    {
      "names": [
        "--one"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Expect exactly one document: error when none or several match"
    },
    {
      "names": [
        "--include-linked"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Also read the stores linked directly to this one"
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
      "help": "Output format (default text)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb docs select [-h] [--ref REF] [--prefix PREFIX] [--path-glob PATH_GLOB] [--model MODEL] [--where WHERE] [--one] [--include-linked] [--store STORE] [--format {text,json,yaml}]
