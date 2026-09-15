---
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
provenance: parser:sldb.cli.parser:build_parser#legacy glob; contract-sha256:0bf5b38142a6a39eaeda1a1f1ea922ee0fe0ae33f8891d998976d17096a14cc6
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
