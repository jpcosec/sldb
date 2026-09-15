---
id: cmd-sldb-selfdoc-scan
system: sldb
command_path: selfdoc scan
synopsis: Inspect parser facts without writing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc scan; contract-sha256:bb57a398896543e28c5663b8eba16d51a9c2ec5b7849b823779e3a2e283cde03
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
