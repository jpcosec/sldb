---
sldb:
  by: agent
  at: '2026-11-16T20:44:43Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-bench
system: sldb
command_path: bench
synopsis: Measure sldb and deskops speed on desk copies, cold and warm.
tags: []
provenance: parser:sldb.cli.parser:build_parser#bench; contract-sha256:b57cc7aacc1e9c922ae302130a825541600fd254a0eb80ea92a9ebdbcba3b5b0
---

# bench

## Synopsis

Measure sldb and deskops speed on desk copies, cold and warm.

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
        "--desk"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Desk to copy and measure; repeatable."
    },
    {
      "names": [
        "--ops"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Comma list from: sldb-help, deskops-help, update-noop, update-one, check, doctor, status, build-check. Default: sldb-help, deskops-help, update-noop, update-one, check, doctor, status."
    },
    {
      "names": [
        "--modes"
      ],
      "required": false,
      "default": "\"cold,warm\"",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "cold, warm or both (default: cold,warm)."
    },
    {
      "names": [
        "--repeat"
      ],
      "required": false,
      "default": "1",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.int",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Measured runs per operation and mode (default 1)."
    },
    {
      "names": [
        "--timeout"
      ],
      "required": false,
      "default": "7200.0",
      "choices": null,
      "nargs": null,
      "value_type": "builtins.float",
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Seconds before one run is killed (default 7200)."
    },
    {
      "names": [
        "--touch"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Document changed by update-one (default: first tracked .md)."
    },
    {
      "names": [
        "--sibling"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._AppendAction",
      "const": "null",
      "help": "Copied beside the desks for relative store links, not measured."
    },
    {
      "names": [
        "--workdir"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Where the copies go (default: $TMPDIR/sldb-bench); deleted at the end."
    },
    {
      "names": [
        "--keep"
      ],
      "required": false,
      "default": "false",
      "choices": null,
      "nargs": 0,
      "value_type": null,
      "action": "argparse._StoreTrueAction",
      "const": "true",
      "help": "Keep the work directory."
    },
    {
      "names": [
        "--deskops"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "deskops executable (default: the one on PATH)."
    },
    {
      "names": [
        "--output"
      ],
      "required": false,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Write the JSON result to this file."
    },
    {
      "names": [
        "--format"
      ],
      "required": false,
      "default": "\"text\"",
      "choices": [
        "\"text\"",
        "\"json\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "stdout: table (text) or the JSON."
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb bench [-h] --desk NAME=PATH [--ops OPS] [--modes MODES] [--repeat REPEAT] [--timeout TIMEOUT] [--touch NAME=PATH] [--workdir WORKDIR] [--keep] [--deskops DESKOPS] [--output OUTPUT] [--format {text,json}]
