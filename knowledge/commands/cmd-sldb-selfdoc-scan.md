---
sldb:
  by: agent
  at: '2026-11-16T21:07:45Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-selfdoc-scan
system: sldb
command_path: selfdoc scan
synopsis: Inspect parser facts without writing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc scan; contract-sha256:a9ae0f82e4ee722ac40db39b5a99cd9f2f80f71ac01b8920af1a513edf79cdcc
---

# selfdoc scan

## Synopsis

Inspect parser facts without writing.

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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb selfdoc scan [-h] [--factory FACTORY] [--pythonpath PYTHONPATH]
                         [--store STORE] [--include-hidden]
