---
sldb:
  by: agent
  at: '2026-11-16T20:55:02Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-legacy-glob
system: sldb
command_path: legacy glob
synopsis: Expand wildcard addresses.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#legacy glob; contract-sha256:8bc907c5907537dcc2f3f646723dc8ee0e21f4c3c1abb07ec27f948b408a8683
---

# legacy glob

## Synopsis

Expand wildcard addresses.

## Purpose

Enumerate addresses before reading them. On `st.` the doc and field segments take shell patterns (`st.{Book}.chapter-*.title`). On `se.` a `*` matches one tag segment and `**` any depth (`se.type.**`).

## How It Works

Implemented under src/sldb/cli/parsers/legacy.py (parser) and src/sldb/cli/commands/query.py (QueryCLI), dispatched through LegacyCLI. The address root picks the engine: `st.` goes to sldb.store.query_engine.structural, `se.` to the semantic engine, `gse.` to the global semantic engine over linked stores. All of them load the store's runtime documents and select by address; nothing reads Markdown by hand.

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
        "address"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Wildcard address"
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

sldb legacy glob 'st.{CliCommandDoc}.cmd-sldb-*.synopsis' --store .sldb --pythonpath .
sldb legacy glob 'se.type.*' --store .sldb --pythonpath .
