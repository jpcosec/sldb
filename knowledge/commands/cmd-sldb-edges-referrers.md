---
sldb:
  by: agent
  at: '2026-11-16T20:47:32Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-edges-referrers
system: sldb
command_path: edges referrers
synopsis: 'Every reference to a document or project node: declared fields (scalar
  or list element) and mentions in prose.'
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges referrers; contract-sha256:544071e9d3ea04e16d4cd55477a95ff669f2e2656894181ec3c0b37141a4b20a
---

# edges referrers

## Synopsis

Every reference to a document or project node: declared fields (scalar or list element) and mentions in prose.

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
        "target"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Doc name, Model/name, Model:name, tracked path, or a project graph node id (kind:identity)"
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
      "help": "Output format (default text)"
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb edges referrers [-h] [--store STORE] [--pythonpath PYTHONPATH] [--format {text,json,yaml}] target
