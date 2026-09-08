---
id: cmd-sldb-legacy-ls
system: sldb
command_path: legacy ls
synopsis: 'List the children of an address: models of the store, docs of a model,
  fields of a doc, child tags of a tag.'
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/commands/query.py
---

# legacy ls

## Synopsis

List the children of an address: models of the store, docs of a model, fields of a doc, child tags of a tag.

## Purpose

Walk the store as a tree without opening any file. `st` lists every registered model, `st.{Model}` its tracked docs, `st.{Model+}` the docs of the whole family, `st.{Model}.<doc>` the fields with their descriptions, `se` the top-level tag segments and `se.<prefix>` the child segments (or the docs tagged exactly `prefix` at a leaf).

## How It Works

Implemented under src/sldb/cli/parsers/legacy.py (parser) and src/sldb/cli/commands/query.py (QueryCLI), dispatched through LegacyCLI. The address root picks the engine: `st.` goes to sldb.store.query_engine.structural, `se.` to the semantic engine, `gse.` to the global semantic engine over linked stores. All of them load the store's runtime documents and select by address; nothing reads Markdown by hand.

## Arguments

address | required | st | st.{Model} | st.{Model+} | st.{Model}.<doc> | se | se.<prefix> | gse.<tag>
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

sldb legacy ls st --store .sldb --pythonpath .
sldb legacy ls 'st.{CliCommandDoc}' --store .sldb --pythonpath .
sldb legacy ls 'st.{CliCommandDoc}.cmd-sldb-find' --store .sldb --pythonpath .
sldb legacy ls se --store .sldb --pythonpath .
