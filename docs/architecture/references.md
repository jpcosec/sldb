# Incoming references: find them and rewrite them

`sldb.api.referrers(store, target)` lists every place that refers to a document or to a project
graph node; `sldb.api.rewrite_references(store, target, replacement)` rewrites them all to name
something else, or removes them, in one transaction. This is node GD22 of the plan
`generalizar-desde-deskops`: the "find inbound references and rewrite them" that deskops kept
as a walk over `desk/` with a regex (atom merges, retire checks) becomes a read of the two
indexes sldb already keeps, the edge index (GD21 reads it too) and the project graph (GD21),
written through the transaction of GD24.

## What a reference is

Two kinds, told apart by `origin`:

| `origin` | Where it comes from | What it is |
|---|---|---|
| `schema` | The store's composed edge index (`edges_to`): every references or contains (containment) edge a declared field produces (`__references__`, `__reference_models__`, `__containment__`, and the `__doc_anchors__` fields of GO07). | A value of a tracked document's field: a scalar, or one element of a list (`index` is its position). The value is read as it was written (`metadata.declared`). |
| `mention` | The project graph of GD21 (`ProjectGraph.edges_to`): every edge a `MentionPattern` of `line_mentions` or `section_mentions` declared, located `line:N:<label>`. | A text a pattern captured on line `N` of a project file (tracked or not). `location` is `path:N`. |

Not references, by this node: the frontmatter declarations of untracked documents the project
graph reads through `reference_fields` and `fields_by_kind` (locator `frontmatter`), and the
YAML blocks of a body (`line:N:yaml`). They are declared fields of files sldb does not model,
so neither the index nor a line rewrite can change them safely; they stay in `graph edges --to`.

A `Referrer` is `{source, field, index, location, origin}`:

- `source`: the export id `Model:name` of the referring document (`schema`), or the
  project-relative path of the mentioning file (`mention`);
- `field`: the declared field (`schema`) or `null`;
- `index`: the position in a list field, `null` for a scalar or a mention;
- `location`: `path:line` of a mention, `null` for a field.

Fields come first, sorted by source, field and position; then mentions, by path and line.

## Naming the target

`target` (and `replacement`) is resolved in this order (q6):

1. a tracked document, by `name`, `Model/name`, `Model:name` or its tracked path (the rule of
   `doc_status` plus the export id form); several candidates are
   `SLDBDocumentTargetError` naming them (`Ambiguous document target: card-a (candidates:
   Card:card-a, Review:card-a)`);
2. a project graph node id, `kind:identity`, as `graph project nodes` prints it;
3. anything else is `SLDBDocumentTargetError` (`Unknown document target: ...`).

A document whose file sits on a document surface of the project graph is both: its mentions
are found through its node. A node id that is no document (a `source_file:src/app.py`, a card
that is not tracked) has only mentions. A store that declares no `project_graph` has only
fields.

## Rewriting

```python
from sldb import api

report = api.rewrite_references(store, "card-a", "card-a2")          # every reference now names card-a2
report = api.rewrite_references(store, "card-a", None)               # removed where a field allows it
report = api.rewrite_references(store, "card-a", "card-a2", dry_run=True)
with api.transaction(store) as tx:
    api.rewrite_references(store, "card-a", "card-a2", transaction=tx)  # joins; the block decides
```

| Reference | `replacement` given | `replacement` is `None` (remove) |
|---|---|---|
| scalar field | the field takes the new value | the field becomes `null`; the model decides whether it may (q7): a field that does not admit it fails validation, named in the error, and nothing of the batch is written |
| list field | the element is replaced in place; if the list already holds the new value, the replaced element is dropped instead (never a duplicate) | the element is dropped, no hole is left |
| mention | the captured text is replaced on its line, as a whole token (below) | the mention is kept and reported in `skipped`: prose is never deleted |

**The form of the value is kept (q15).** `replacement` is resolved like `target`. When it is a
tracked document, each value is written the way the original named the target: a bare `name`
becomes the replacement's name, `Model:name` its export id, a tracked path its path, and a
document anchor `doc:Model:name@sha256:...` becomes `doc:Model:name` of the replacement
*without* the hash, so the save pins it to the replacement's contract hash (GO07, q2). A
replacement that resolves to no document (a project node id, or anything else) is written as
given; a `__doc_anchors__` field then refuses it, as its validator refuses any non-anchor.

**Mentions are whole tokens (q16, q18).** A mention token is a run of `[A-Za-z0-9_:./-]`. The
text a `MentionPattern` captured is replaced only where the character before it is outside
that set (or the line starts) and what follows is outside it (or the line ends), so
`card:card-a` rewrites neither `card:card-ab` nor `card:card-a.b`. Dots that end the token and
are followed by a space or the end of the line are sentence punctuation, not part of it:
`Ver card:card-a.` and `card:card-a...` are rewritten and keep their dots. A line whose text is
no longer there, or where the text is not a whole token, goes to `skipped` with the reason. The
new text keeps the form of the mention too: the node id (`card:card-a` → `card:card-a2`), the
node's identity, its path, or the document's name or export id.

**All or nothing (GD24, q3, q9).** The writes run inside `sldb.api.transaction`: the one passed
in, or one the call opens. A document's payload is written with `transaction.update`, so it
goes through `save_document_payload`: the anchors are pinned, the `on_write` rules of GO08 and
the builtin tag family of GD27 run, the document is rendered and tracked again. A mentioning
file is rewritten with `replace_text` (GD27): a tracked document is validated under its model
and tracked again with the same model and name, a plain file is written with its sha256 as
guard. A failure anywhere (a model that refuses a payload, a rule, an I/O error) restores every
document written before it: bytes, index entries and shards.

**Validated before anything is written (q14).** Every new payload is validated and
round-tripped under its model in memory (`validate_model_data_roundtrip`), and the new text of
a tracked mentioning document under its model, before the transaction opens. With `dry_run`
that is all: the `RewriteReport` is computed, nothing is opened for writing, no file changes
(the test hashes every file before and after) and **the `on_write` rules do not run**: they
only run when a document is written.

**Nothing walks the project (q8, q17).** The index is the composed one sldb keeps per process
and the graph the memoized one of GD21; with both warm, `referrers` and a dry run make no
`os.walk`, no `Path.rglob` and no `os.scandir` outside the store's own directories (the shards
signature of the index stat-scans `.sldb_cache/edges`). A real write opens the transaction,
which records the store's signatures (`rglob` under `.sldb/`).

### The report

`RewriteReport` is `{changed, skipped}`:

- `changed`: `{source, field, index, location, before, after}` per reference, in the order of
  `referrers`; `after` is `null` for a removal; a mention's `before`/`after` are the token;
- `skipped`: `{source, location, reason}` per mention left alone.

## CLI and HTTP

```
sldb edges referrers TARGET [--store] [--pythonpath] [--format text|json|yaml]
sldb edges rewrite TARGET --to NEW | --remove [--dry-run] [--store] [--pythonpath] [--format]
GET  /edges/referrers?target=TARGET
POST /edges/rewrite {"target": TARGET, "replacement": NEW | null, "dry_run": false}
```

`--to` and `--remove` exclude each other and one is required (argparse: exit 2, `cli/usage`
under `--envelope`). With `--format json` the commands print the data object itself: the list
of `Referrer`, the `RewriteReport` (q13); `--envelope` wraps it in `data`, and an unknown or
ambiguous target, a refused payload or a rule are the envelope's typed errors (`docs/missing`,
`docs/ambiguous`, `validate/rejected`, `rules/violation`). The HTTP bodies are exactly those
objects (q10): the referrers list, the report. In `POST /edges/rewrite`, `replacement` is
required (`null` removes; absent is 400) and `dry_run` optional (a boolean); a missing or
invalid parameter is 400, an unknown target 404, an ambiguous one 409, a refused write 400
with nothing written (q11).

## Where it lives

- `src/sldb/api/edges/referrers.py`: `referrers`, the target resolution and the search;
  `referrer.py` the `Referrer` model.
- `src/sldb/api/edges/rewrite_values.py`: the field hits read from the index and the payload
  rewritten in the value's form; `rewrite_mentions.py`: the mention hits read from the graph
  and the line rewritten as whole tokens; `rewrite_references.py`: the plan, the in-memory
  validation, the dry run and the transaction; `rewrite_report.py` the `RewriteReport`.
- `src/sldb/cli/commands/edges_rewrite.py`, `src/sldb/cli/parsers/edges.py`,
  `src/sldb/cli/serve/edges_rewrite_routes.py`.
- Tests: `tests/api/test_referrers.py`, `tests/api/test_rewrite_references.py`,
  `tests/test_serve.py` (the HTTP routes against the CLI).

What deskops keeps without reason once it reads this: `_find_inbound_atom_references` and
`_rewrite_inbound_atom_references` (`services/atoms.py`, through `operations.py`), the regex
walk over `desk/` they share, and the inbound check of `services/retire.py`.
