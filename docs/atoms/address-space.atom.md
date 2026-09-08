# Address Space

## Related Concepts

- [Store](store.atom.md)
- [Tracked Document](tracked-document.atom.md)
- [StructuredNLDoc Model](structurednldoc-model.atom.md)
- [Semantic vs Physical Search](semantic-vs-physical.atom.md)

## What It Is

The address space is how every field, subfield and list item of every tracked document is named and reached without opening its Markdown. A structural address is `st.{Model}.<doc>.<field>`, extended by key into dict subfields and by position into list items or table rows (`tasks.0.title`); `st.{Model+}` names the model and every subclass; `se.<tag>` names the documents carrying a semantic tag; `gse.<tag>` does the same across linked stores. The `fields` surface spells the same address as `docs/<doc>/<field>/<sub>`.

## Why It Matters

Without addresses the store is only an integrity index and every consumer re-parses Markdown by hand. With addresses the store is a database of fields: one command reads a value, one command filters a family of documents by a predicate, one command changes a value and SLDB rewrites the file. This is the contract downstream tools should build on instead of loading and filtering payloads themselves.

## How It Works

A read resolves store index to document path and model, applies the model's compiled template recipe to that document and returns the field. A write takes the same address plus a new value, re-renders the whole document from the updated payload, verifies the render extracts back to the same payload, writes the file, updates `hash_c` and `hash_d`, rebuilds the semantic index and cascades `hash_a`. Family scope `{Model+}` matches by class name through each document's model MRO, so an unregistered base still names a family. `--where` takes one predicate: `has(f)`, `"x" in f`, `f ~ "regex"`, `f = "v"`, `f != "v"`, `f >= n`, `f <= n`, `model <= Base`.

## When It Shows Up

In `sldb legacy ls|get|glob|find` (the raw address spelling), in `fields show|query|update|create|append|clean` and `find --type doc|field|section --where` (the public spelling), in `serve` `/graph` and `POST /save`, and in the `sldb://` node ids that `stores semantic-export` hands to KGDB.

## Where It Lives

The engine is `sldb.store.query` (`get_structural`, `list_structural`, `glob_structural`, `find_structural`, and the `se`/`gse` engines) plus `sldb.store.query_engine.filter` for predicates. Writes go through `sldb.cli.commands.fields_save.save_payload`. The full model is `docs/addressability_model.md`.

## Who Uses It

Anyone reading or changing a value in a tracked document, and any tool built over the store (kgdb ingest, pron, deskops materializers) that wants a field or a family of documents without parsing Markdown itself.
