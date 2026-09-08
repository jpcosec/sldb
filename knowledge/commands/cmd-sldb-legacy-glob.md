---
id: cmd-sldb-legacy-glob
system: sldb
command_path: legacy glob
synopsis: Expand a wildcard address into the concrete doc or field addresses it matches.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/commands/query.py
---

# legacy glob

## Synopsis

Expand a wildcard address into the concrete doc or field addresses it matches.

## Purpose

Enumerate addresses before reading them. On `st.` the doc and field segments take shell patterns (`st.{Book}.chapter-*.title`). On `se.` a `*` matches one tag segment and `**` any depth (`se.type.**`).

## How It Works

Implemented under src/sldb/cli/parsers/legacy.py (parser) and src/sldb/cli/commands/query.py (QueryCLI), dispatched through LegacyCLI. The address root picks the engine: `st.` goes to sldb.store.query_engine.structural, `se.` to the semantic engine, `gse.` to the global semantic engine over linked stores. All of them load the store's runtime documents and select by address; nothing reads Markdown by hand.

## Arguments

address | required | st.{Model}.<docpattern>[.<fieldpattern>] | se.<tagpattern>
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

sldb legacy glob 'st.{CliCommandDoc}.cmd-sldb-*.synopsis' --store .sldb --pythonpath .
sldb legacy glob 'se.type.*' --store .sldb --pythonpath .
