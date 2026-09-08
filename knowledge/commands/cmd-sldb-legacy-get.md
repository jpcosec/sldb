---
id: cmd-sldb-legacy-get
system: sldb
command_path: legacy get
synopsis: Read a document payload, a field, a subfield or a list item by address;
  or the docs carrying a tag.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/commands/query.py
---

# legacy get

## Synopsis

Read a document payload, a field, a subfield or a list item by address; or the docs carrying a tag.

## Purpose

Read one value without opening the Markdown. `st.{Model}.<doc>` returns the whole payload, `st.{Model}.<doc>.<field>` the value, and the path keeps going into dict subfields by key and list items or table rows by position (`tasks.0.title`). `se.<tag>` returns the `st.` addresses of every document carrying the tag; `gse.<tag>` does it across linked stores.

## How It Works

Implemented under src/sldb/cli/parsers/legacy.py (parser) and src/sldb/cli/commands/query.py (QueryCLI), dispatched through LegacyCLI. The address root picks the engine: `st.` goes to sldb.store.query_engine.structural, `se.` to the semantic engine, `gse.` to the global semantic engine over linked stores. All of them load the store's runtime documents and select by address; nothing reads Markdown by hand.

## Arguments

address | required | st.{Model}.<doc>[.<field>[.<sub>|.<i>]...] | se.<tag> | gse.<tag>
--format | optional | json (default), yaml or text
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

sldb legacy get 'st.{CliCommandDoc}.cmd-sldb-find.synopsis' --format text --store .sldb --pythonpath .
sldb legacy get 'st.{Book}.book.tasks.0.title' --format text --store .sldb --pythonpath .
sldb legacy get 'se.type.documentation.atom' --store .sldb --pythonpath .
