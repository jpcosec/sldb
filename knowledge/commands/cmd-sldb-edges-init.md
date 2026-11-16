---
sldb:
  by: agent
  at: '2026-11-16T20:47:15Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-edges-init
system: sldb
command_path: edges init
synopsis: Register RelationTypeDoc/RelationDoc and track the builtin relation types.
tags: []
provenance: parser:sldb.cli.parser:build_parser#edges init; contract-sha256:e46033da023344d18ae692b286caa1bd47626b20bcfd8e6dcae8035f49309064
---

# edges init

## Synopsis

Register RelationTypeDoc/RelationDoc and track the builtin relation types.

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
    }
  ],
  "exclusive_groups": []
}
```

## Usage

usage: sldb edges init [-h] [--store STORE] [--pythonpath PYTHONPATH]
