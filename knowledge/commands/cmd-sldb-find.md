---
id: cmd-sldb-find
system: sldb
command_path: find
synopsis: Unified semantic + physical retrieval.
tags:
- system:sldb
- domain:retrieval
- kind:software
- impl:external
- entity:cli_command
provenance: src/sldb/cli/parsers/
---

# find

## Synopsis

Unified semantic + physical retrieval.

## Purpose

The `sldb find` command: Unified semantic + physical retrieval.

## How It Works

Implemented under src/sldb/cli/parsers/ as the argparse subcommand 'find'. It parses the listed arguments and dispatches to its handler in the sldb CLI runtime over the .sldb store.

## Arguments

term | required | Resource term, semantic tag, or physical token (use "" to match everything)
--in | optional | semantic, physical or both (default both)
--global | optional | Include linked stores
--regex | optional | Treat the term as a regex
--fuzzy | optional | Use fuzzy matching
--rebuild | optional | Rebuild the section indexes before searching
--type | optional | Restrict to store, model, doc, section or field
--select | optional | Comma-separated projection fields
--where | optional | One predicate. Docs: has(f), "x" in f, f ~ "re", f = "v", f != "v", f >= n, f <= n, model <= Base. Fields: value = "v", doc = "d", model = "M", has(value). Sections: title ~ "re", "x" in about|breadcrumbs|semantic_tags, path = "p"
--store | optional | Store path
--pythonpath | optional | Project path
--format | optional | text, json or yaml

## Usage

find
