---
id: cmd-sldb-legacy-find
system: sldb
command_path: legacy find
synopsis: Filter the documents of a model, a family or a tag scope with one predicate;
  prints their addresses.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/commands/query.py
---

# legacy find

## Synopsis

Filter the documents of a model, a family or a tag scope with one predicate; prints their addresses.

## Purpose

Answer 'every document of this family where field = value' in one command. The scope is `st.{Model}`, `st.{Model+}` (the model and every subclass, base registered or not) or `se.<pattern>`; the predicate is one of has(f), "x" in f, f ~ "regex", f = "v", f != "v", f >= n, f <= n, model <= Base.

## How It Works

Implemented under src/sldb/cli/parsers/legacy.py (parser) and src/sldb/cli/commands/query.py (QueryCLI), dispatched through LegacyCLI. The address root picks the engine: `st.` goes to sldb.store.query_engine.structural, `se.` to the semantic engine, `gse.` to the global semantic engine over linked stores. All of them load the store's runtime documents and select by address; nothing reads Markdown by hand.

## Arguments

address | required | st.{Model} | st.{Model+} | se.<pattern>
--where | required | One predicate: has(f) | "x" in f | f ~ "re" | f = "v" | f != "v" | f >= n | f <= n | model <= Base
--store | optional | Store path
--pythonpath | optional | Project path

## Usage

sldb legacy find 'st.{CliCommandDoc}' --where 'system = "sldb"' --store .sldb --pythonpath .
sldb legacy find 'st.{PrimitiveDoc+}' --where 'status = "active"' --store .sldb --pythonpath .
sldb legacy find 'se.type.knowledge.anchor' --where 'kind = "operation"' --store .sldb --pythonpath .
