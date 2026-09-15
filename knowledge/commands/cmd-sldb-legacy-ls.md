---
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
provenance: parser:sldb.cli.parser:build_parser#legacy ls; contract-sha256:63daf0faff2bd65b3cfaccdff67236b194aeaf887b449ea566fb2f21268c910a
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
