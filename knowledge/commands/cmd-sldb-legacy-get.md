---
id: cmd-sldb-legacy-get
system: sldb
command_path: legacy get
synopsis: Get raw node data.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#legacy get; contract-sha256:7204a9a6d46e3b7771f2da62627ca6ec76519bdeef25383bcb08f5c8d591b0fb
---

# legacy get

## Synopsis

Get raw node data.

## Purpose

Read one value without opening the Markdown. `st.{Model}.<doc>` returns the whole payload, `st.{Model}.<doc>.<field>` the value, and the path keeps going into dict subfields by key and list items or table rows by position (`tasks.0.title`). `se.<tag>` returns the `st.` addresses of every document carrying the tag; `gse.<tag>` does it across linked stores.

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
      "help": "Address"
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
        "--format"
      ],
      "required": false,
      "default": "\"json\"",
      "choices": [
        "\"json\"",
        "\"yaml\"",
        "\"text\""
      ],
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": ""
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

sldb legacy get 'st.{CliCommandDoc}.cmd-sldb-find.synopsis' --format text --store .sldb --pythonpath .
sldb legacy get 'st.{Book}.book.tasks.0.title' --format text --store .sldb --pythonpath .
sldb legacy get 'se.type.documentation.atom' --store .sldb --pythonpath .
