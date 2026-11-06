# Selectors: choosing tracked documents by ref, prefix, path, model and predicate

`sldb.api.select_documents(store, selector, expect="many" | "one")` answers which tracked
documents a selector names. It is node GD23 of the plan `generalizar-desde-deskops`: it absorbs
the `resolve_selector` rule deskops kept in its own `desk_paths` (exact name first, then a
unique prefix, anything else an error that lists the candidates) and gives it to every consumer
with the other ways sldb already names documents.

## The selector

A selector is a mapping (the pydantic model `sldb.api.Selector`) whose keys combine by
conjunction: a document is chosen only when every key given keeps it.

| Key | Keeps the documents whose... | Notes |
|---|---|---|
| `ref` | name, tracked path, `Model/name` or `Model:name` is the reference | exactly what `doc_status` accepts; `alias:ref` reaches the store linked directly as `alias` even without `include_linked`; `local:` is the local store |
| `prefix` | name starts with the prefix | with `expect="one"`, an exact name wins over the prefix matches (the deskops rule) |
| `path_glob` | path relative to the project root matches the shell pattern | `*` and `?` stop at `/`, `**` crosses directories (`sub/**/*.md` is every `.md` under `sub/`, at any depth), `[seq]` as in `fnmatch` |
| `model` | model is `X` or extends `X` | the family read from each model index's `base_models`; an inherited model answers with its owner's |
| `where` | payload holds the predicate | the rules language (`docs/architecture/rules-language.md`), evaluated by the store's own evaluator over the edge index's payload projection (GO04): nothing is extracted from a file |
| `include_linked` | (bool, default false) also read every store linked directly to this one | their rows carry `alias:`; links of links are never read |

A key given as an empty or blank string, or a key the selector does not know, is rejected with
`pydantic.ValidationError`; a `where` the parser does not understand raises
`WherePredicateError` with the parser's message, before anything is read.

## The answer

A list of `{export_id, model, name, path}` rows:

- `export_id` is the document's node id in the edge index: `Model:name`, or
  `alias:Model:name` for a document of a linked store;
- `path` is relative to the project root of the store that tracks it (posix);
- the order is stable: the local store's rows by path, then each linked store's rows, by alias
  and then by path.

`expect="many"` returns every match; a prefix keeps every name starting with it (the exact
name included) and never fails for ambiguity. `expect="one"` returns a list of exactly one row:
by prefix, the exact name wins, else the one prefix match. With no match it raises the
existing `SLDBDocumentTargetError` (`Unknown document: prefix='x', model='Y'`); with several,
`AmbiguousSelectionError` (a subclass of it, in `sldb.core.exceptions` and `sldb.api`) whose
`candidates` holds the export ids in the order above, also listed in the message. The
`AmbiguousDocument` of `resolve_indexed_document` is a different question (a `Model:name` asked
under a base model that several submodels track) and stays as it is.

```python
from sldb import api

api.select_documents(store, {"prefix": "task-a"}, expect="one")
# [{"export_id": "BaseDoc:task-a", "model": "BaseDoc", "name": "task-a", "path": "task-a.md"}]
api.select_documents(store, {"model": "BaseDoc", "path_glob": "sub/**/*.md", "where": 'status = "open"'})
api.select_documents(store, {"ref": "deskops:task-x"}, expect="one")   # one linked store, by its alias
```

## Where it lives

The rule itself is the store's: `sldb.store.query_engine.document_selection.select_rows`
reads the candidates from the documents indexes (never a model import), applies the filters of
`document_selection_filters` and the prefix tier, and evaluates `where` with
`compose_edge_index`, `index_view` and `findings`, the same evaluator `GraphBackend.eval` and
`sldb.api.where` use. `sldb.api.select_documents` is its public face: it opens the store,
splits the `ref`'s alias as `doc_status` does, and turns `expect="one"` into the errors above.
The store cannot import `sldb.api` (`tests/test_store_seams.py`), which is why the core sits
below the API.

`glob_structural` and `find_structural` (`sldb query glob|find` over `st.{Model}`,
`st.{Model+}` and `alias:st.…`) choose the documents of their scope through the same core (the
model, exact or family); the name pattern, the expansion to fields, the address form of the
results (`st.{M+}.doc.field`) and `find`'s `--where` stay in `structural_queries`. Their output
does not change: `find --where` keeps evaluating on each document's own extracted payload, so a
predicate on a field the index does not project (nested, or outside `__indexed__`) reads as before.

## CLI and HTTP

```
sldb docs select [--ref R] [--prefix P] [--path-glob G] [--model M] [--where W] [--one] [--include-linked] [--store S] [--format text|json|yaml]
GET /docs/select?ref=&prefix=&path_glob=&model=&where=&one=1&include_linked=1
```

There is no short selector string: the CLI takes only flags, and the route the same names as
query parameters. Both answer the same JSON, `{"selector": {...}, "expect": "one" | "many",
"documents": [rows]}`; the text form prints `export_id -> path` per row. The CLI exits 1 with the
error's message when `--one` finds none or several (`--envelope`: `docs/missing` exit 1,
`docs/ambiguous` exit 2, the usual table of `sldb.cli.error_types`); the route answers 404 for
none, 409 with `candidates` for several, and 400 for a blank key or an unparseable `where`.
