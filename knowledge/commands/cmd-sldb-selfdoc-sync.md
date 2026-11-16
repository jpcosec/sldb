---
sldb:
  by: agent
  at: '2026-11-16T21:07:57Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-selfdoc-sync
system: sldb
command_path: selfdoc sync
synopsis: Update generated fields and track reference documents.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc sync; contract-sha256:43ec30cc0ad54dbd57f5d7819b517841f08016a6f7248a5551e9b1bbfdea46bb
---

# selfdoc sync

## Synopsis

Update generated fields and track reference documents.

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
        "--factory"
      ],
      "required": false,
      "default": "\"sldb.cli.parser:build_parser\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Trusted module:callable returning ArgumentParser"
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
      "help": "Import path, relative to the selected project root"
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
      "help": "Store path or linked alias; otherwise nearest ancestor store"
    },
    {
      "names": [
        "--include-hidden"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Include commands/options with suppressed help"
    },
    {
      "names": [
        "--system"
      ],
      "required": false,
      "default": "\"sldb\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Stable lowercase tool identifier"
    },
    {
      "names": [
        "--output"
      ],
      "required": false,
      "default": "\"knowledge\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Documentation directory relative to the store root"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb selfdoc sync [-h] [--factory FACTORY] [--pythonpath PYTHONPATH]
                         [--store STORE] [--include-hidden] [--system SYSTEM]
                         [--output OUTPUT]
