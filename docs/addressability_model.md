# SLDB Addressability Model

The store is a database of addressable fields over Markdown. You never open a Markdown file to read or change a value: you name the value by address and SLDB reads it, filters it, or rewrites the file for you. The Markdown stays canonical; the address is how you reach into it.

This document describes the address spaces as implemented in `sldb.store.query` and the CLI surfaces that speak them. Everything here is exercised by `tests/test_address_surface.py`.

## One rule

**Read and write by address. SLDB owns the file.**

- A read is `store → model → document → field`. The store index gives the document's path and model, the model's template gives the field recipe, and SLDB returns the value.
- A write is the same address plus a new value. SLDB re-renders the whole document from the updated payload, checks the roundtrip, writes the file, updates `hash_c`/`hash_d`, rebuilds the semantic index, and cascades `hash_a`.

## Address spaces

### `st.` — structural (store, model, document, field)

| Address | Means | `ls` | `get` |
|---|---|---|---|
| `st` | the store | every `st.{Model}` registered | — |
| `st.{Model}` | one model | tracked doc names | — |
| `st.{Model+}` | a family: the model and every subclass | doc names across the family | — |
| `st.{Model}.<doc>` | one document | its fields with their descriptions | the whole payload |
| `st.{Model}.<doc>.<field>` | one field | — | the value |
| `st.{Model}.<doc>.<field>.<sub>` | a subfield: a key of a dict field | — | the nested value |
| `st.{Model}.<doc>.<field>.<i>` | an item of a list field or a table row, by position | — | the item |
| `st.{Model}.<doc>.<field>.<i>.<sub>` | a key inside that item | — | the nested value |

Fields have subfields. A `rev,dict•meta` marker or a field typed with another model is a dict, reached by key. A `rev,list•items` marker or a table row template is a list, reached by zero-based index; a table row is a dict keyed by its column markers, so `rows.2.status` is one cell. The path may mix both as deep as the payload goes. On the `fields` surface the same path is written with slashes: `docs/<doc>/rows/2/status`.

The family form `{Model+}` matches on class name through each document's model MRO, so the base does not need to be registered. `st.{PrimitiveDoc+}` selects every document whose model descends from `PrimitiveDoc` even when `PrimitiveDoc` itself has no documents.

Wildcards: `glob` accepts shell patterns on the document and field segments, e.g. `st.{Book}.chapter-*.title`.

### `se.` — semantic (tags and the DAG)

| Address | Means |
|---|---|
| `se` | the top-level tag segments |
| `se.<prefix>` | `ls`: child segments under the prefix, or the doc names tagged exactly `prefix` when it is a leaf |
| `se.<tag>` | `get`: the `st.` addresses of every document carrying the tag |
| `se.<pattern>` | `glob`: `*` matches one segment, `**` matches any depth |

Tags come from the model's `__semantics__` plus the document's `tags`/`semantic_tags` field, flattened to dotted form (`type.knowledge.anchor`). Dotted prefixes become the semantic DAG (`type → type.knowledge → type.knowledge.anchor`).

### `gse.` — global semantic (across linked stores)

| Address | Means |
|---|---|
| `gse.<tag>` | documents across the local and linked stores whose tags map to the global tag through each store's equivalences; results are prefixed `store:` |
| `gse.<tag>.se.{store}` | the local tags of one linked store that map to that global tag |

Equivalences are declared with `stores semantic-map`.

## Predicates (`--where`)

`find` takes one predicate per `--where`. There is no `and`/`or`; run two queries or narrow the address instead.

On documents (`legacy find 'st.{…}'`, `legacy find 'se.…'`, `find --type doc`):

| Predicate | Matches when |
|---|---|
| `has(field)` | the field is present and not empty |
| `"x" in field` | `x` is an item of a list field or a substring of a string field |
| `field ~ "regex"` | the field value matches; `doc ~ "regex"` matches the doc name |
| `field = "v"` / `field != "v"` | string equality |
| `field >= n` / `field <= n` | numeric comparison |
| `model <= Base` | the document's model is `Base` or a subclass |

On fields (`find --type field`): `value = "…"`, `value != "…"`, `doc = "…"`, `model = "…"`, `field = "…"`, `has(value)`.

On sections (`find --type section`, `sections find`): `title ~ "regex"`, `"term" in about`, `"term" in breadcrumbs`, `"tag" in semantic_tags`, `path = "…"`.

## The two spellings of the same surface

The raw address commands and the public `fields`/`find` commands reach the same engine.

| Question | Raw address | Public surface |
|---|---|---|
| value of one field | `legacy get 'st.{Book}.my-book.title'` | `fields show docs/my-book/title` |
| schema of one field | — | `fields show models/Book/title` |
| fields of one doc, with descriptions | `legacy ls 'st.{Book}.my-book'` | `ast show docs/my-book` |
| one field across every doc | `legacy glob 'st.{Book}.*.status'` then `get` | `fields query status [--global]` |
| docs of a family where … | `legacy find 'st.{Base+}' --where 'status = "open"'` | `find "" --type doc --where 'model <= Base'` then `--where 'status = "open"'` |
| docs by tag | `legacy get 'se.type.note'` | `find type.note --in semantic --type doc` |
| change a value | — | `fields update docs/my-book/title '"New"'` |
| add to a list | — | `fields append docs/my-book/tags '"x"'` |
| create a missing field / normalize a list | — | `fields create` / `fields clean` |
| replace the whole payload | — | `docs update my-book payload.yaml`, or `serve` `POST /save` |

`sldb legacy` is the compatibility spelling; the singular top-level aliases (`ls`, `get`, `glob`, `raw-find`) route to the same handler and are deprecated.

## Sections are addressed by path, not by `st.`

Sections live in the runtime sections index with their heading path (`overview/roadmap`), breadcrumbs, derived `about` terms and line range. Reach them with `sections show <doc>`, `sections find`, `sections fields <doc>/<section>`, or `find --type section`. A field's owning section is exposed by `fields query` and `ast show`.

## Stability

- **Document and field addresses are the stable ones.** A doc name is fixed at `track`/`create`; field names come from the model template.
- **Section paths break when a heading changes.** Treat them as navigational, not as long-lived links.
- **List positions shift.** `tasks.2` is a valid address for reading and `fields update`, but inserting or removing an item renumbers what follows. Give list items an id field if you need to link to them durably.
- **`find --type field` and `fields query` flatten dict subfields (`metadata.author`) but treat a list as one value.** To filter inside list items, read the list by address and filter the items.

## Cost

Every address read resolves through `load_runtime_documents`, which extracts every tracked document of the store before selecting. Addresses narrow the *answer*, not the *work*. This is an engine limitation, not part of the contract: a seek that goes index → path → one extraction is the obvious optimization and changes nothing above.

## Provenance

The `st.` form is what `stores semantic-export` and the KGDB ingest use as identity: `sldb://model/<Model>`, `sldb://document/<Model>:<doc>`, `sldb://section/<Model>:<doc>#<path>`. A graph consumer can always come back from a node to the address that produced it.
