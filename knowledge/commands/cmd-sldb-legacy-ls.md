---
sldb:
  by: agent
  at: '2026-11-16T20:55:11Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-legacy-ls
system: sldb
command_path: legacy ls
synopsis: List raw nodes.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#legacy ls; contract-sha256:243f46da64c4151a8ac014fd3cbf41f4d58a89dc3dc2f8be5a55f682713f2de2
---

# legacy ls

## Synopsis

List raw nodes.

## Purpose

Walk the store as a tree without opening any file. `st` lists every registered model, `st.{Model}` its tracked docs, `st.{Model+}` the docs of the whole family, `st.{Model}.<doc>` the fields with their descriptions, `se` the top-level tag segments and `se.<prefix>` the child segments (or the docs tagged exactly `prefix` at a leaf).

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
      "help": "Address (st.*, se.*)"
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

sldb legacy ls st --store .sldb --pythonpath .
sldb legacy ls 'st.{CliCommandDoc}' --store .sldb --pythonpath .
sldb legacy ls 'st.{CliCommandDoc}.cmd-sldb-find' --store .sldb --pythonpath .
sldb legacy ls se --store .sldb --pythonpath .
