---
id: cmd-sldb-selfdoc-check
system: sldb
command_path: selfdoc check
synopsis: Report documentation drift without writing.
tags: []
provenance: parser:sldb.cli.parser:build_parser#selfdoc check; contract-sha256:b99024e55bc43ebb5c33ecdabd62040815b279850d4a05a9e95d642e3bd36404
---

# selfdoc check

## Synopsis

Report documentation drift without writing.

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

usage: sldb selfdoc check [-h] [--factory FACTORY] [--pythonpath PYTHONPATH]
                          [--store STORE] [--include-hidden] [--system SYSTEM]
                          [--output OUTPUT]
