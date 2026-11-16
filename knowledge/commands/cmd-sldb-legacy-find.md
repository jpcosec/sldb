---
sldb:
  by: agent
  at: '2026-11-16T20:54:44Z'
  authority: generated
  via: save_document_payload
id: cmd-sldb-legacy-find
system: sldb
command_path: legacy find
synopsis: Filter raw query results.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: parser:sldb.cli.parser:build_parser#legacy find; contract-sha256:9966a9cb2db957d54b51a001d2fb56a68c586c3a9bf4a6b490d6bd46ebbddd2e
---

# legacy find

## Synopsis

Filter raw query results.

## Purpose

Answer 'every document of this family where field = value' in one command. The scope is `st.{Model}`, `st.{Model+}` (the model and every subclass, base registered or not) or `se.<pattern>`; the predicate is one of has(f), "x" in f, f ~ "regex", f = "v", f != "v", f >= n, f <= n, model <= Base.

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
      "help": "Address scope"
    },
    {
      "names": [
        "--where"
      ],
      "required": true,
      "default": "null",
      "choices": null,
      "nargs": null,
      "value_type": null,
      "action": "argparse._StoreAction",
      "const": "null",
      "help": "Predicate expression"
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

sldb legacy find 'st.{CliCommandDoc}' --where 'system = "sldb"' --store .sldb --pythonpath .
sldb legacy find 'st.{PrimitiveDoc+}' --where 'status = "active"' --store .sldb --pythonpath .
sldb legacy find 'se.type.knowledge.anchor' --where 'kind = "operation"' --store .sldb --pythonpath .
