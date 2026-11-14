# Composed views: a `ViewDoc` with sections, evaluated by `run_view`

`sldb.api.run_view(store, name, params)` evaluates a composed view: a `ViewDoc` (the model of
`sldb.models.notation_models`, SV01) whose `sections` say which documents to read and what each
row carries. It is node GD25 of the plan `generalizar-desde-deskops`: a status view, a list or a
report that a consumer used to assemble in its own code is now a document of the store that
sldb evaluates, serves and revisions. A `ViewDoc` without `sections` is a projection view of
the graph (SV02, `/views/projection*`), untouched.

There is no extension point in Python (decision DA1): no view provider, no `computed` field.
A fact sldb does not derive (the result of a build, a review that happened outside) is a
document the consumer writes to the store, linked to the document it is about; the view reads
it through `select`, `edges` or `rules` like any other document.

## The document

```yaml
id: tablero
name: tablero            # the view's name; `projection` is reserved and refused on write
title: Tablero
params:                # list of {name, required, default}; every value is a string
  - {name: owner, default: ana}
sections:              # ordered; each key is a key of the result
  - key: cards
    select: {model: Item}                 # a selector of `select_documents` (selectors.md)
    fields: [title, status, owner]        # projected fields of each row; `*` = all (default)
    group_by: status                      # groups the rows by this field...
    group_order: [open, review, done]     # ...in this order (a value without rows still appears)
    edges:                                # neighbour ids added to each row, one key per entry
      - {relation: depends_on, direction: out, as: depends_on}
      - {relation: depends_on, direction: in, as: blocked_by}
      - {relation: item, direction: in, as: receipts}
    rules: [owned]                        # RuleDocs evaluated on each row (`findings`)
    transitions: {from_field: stage, relation: moves_to}   # `holding` and `blocked` per row
  - key: mine
    select: {model: Item, where: "owner = {owner}"}
    fields: [title]
```

What one document must say on its own is checked by the model's validators when it is
written (`create_document`, `save_document_payload`, `sldb docs ...`): `params` is a list of
`{name, required, default}` with unique identifier names (a required param has no default);
section keys are unique; `select` is a non-empty mapping of selector keys (`ref`, `prefix`,
`path_glob`, `model`, `where`, `include_linked`) whose strings are not blank and whose
`where` parses; every `{param}` a selector value references is declared; `edges` entries have
a `relation` and a `direction` (`out` | `in`); `transitions` is exactly `{from_field,
relation}`; the name `projection` is refused. A rejected document is not written.

Whether a rule names a RuleDoc the store has depends on the store, so `run_view` checks it:
an unknown rule is `SLDBDocumentTargetError` naming the view, the section and the rule.

## Params

`{name}` in a selector value is filled when the view runs. In `where` the value enters as a
string literal of the predicate (`owner = {owner}` runs as `owner = "ana"`; a value holding a
double quote is refused); in any other key it enters as text (`prefix: "{team}-"`). Values
are strings by every route: `--param k=v` (repeatable; a repeated key is a usage error),
`?k=v` on HTTP, a `dict[str, str]` in Python. A param not declared is an error naming it; a
required one that is absent is an error naming it; a default applies when the param is absent.
The result's `params` are the values the view ran with.

## The result

```json
{"view": "tablero", "params": {"owner": "ana"}, "revision": "<sha256>",
 "sections": {"cards": {"groups": [{"value": "open", "rows": [...]}, ...]},
              "mine": {"rows": [...]}}}
```

A section without `group_by` is `{"rows": [...]}`, in selection order (by path, the local
store's rows first). With `group_by` it is `{"groups": [{"value", "rows"}]}`: first the
values of `group_order`, each present even with no rows (the columns of a status view do not disappear),
then the other values sorted, then, only when there are such rows, the rows without the field
under `"value": null`.

Each row is `{export_id, model, name, path, fields}`, `fields` being the projected fields the
section asked for (the edge index's payload projection: top-level scalars and lists of
scalars, never a re-extraction; `*` = all of them; a field the document lacks is `null`), plus,
only when the section declares them:

| Key | Declared by | Value |
|---|---|---|
| one per `edges` entry, named by its `as` (default `<direction>:<relation>`) | `edges` | the sorted ids reached along that relation in that direction: the index's neighbours (a relation type, or a declaring field of a references or contains (containment) edge) first, then, when the store declares a `project_graph` (GD21), the project graph's for the same relation, each as the document's export id when the index tracks it and as its project node id otherwise, without duplicates |
| `findings` | `rules` | the findings (`Finding.as_dict()`: level, code `rules/<name>`, subject, what, fix, document) of the named rules that apply to the row's document and do not hold, as `sldb rules check` reports them; `what` carries the clause that decided it |
| `holding`, `blocked` | `transitions` | what `edges_holding` and `edges_blocked` answer for the node whose id is the row's `from_field` value (`Model:name`), with the row's projected payload as subject and the row's document for its `on_transition` rules: each edge with its `effects` and, in a store with RuleDocs, its `findings`; an `error` finding moves every edge to `blocked`. Both empty when the row has no `from_field` value |

## The revision

`revision` is the sha256 of: the `source_hash` of every document in the rows (sorted), the
`content_hash` of the ViewDoc and of every RuleDoc a section used, and the store's shards
signature. The shards signature is always in, because a new edge reaching a row (another
document that starts pointing at it) moves the shards and not the row's own document; so
edges, rules and transitions are covered. Writing a document of the rows, editing the ViewDoc
or a RuleDoc, or writing any document that moves the shards changes it; two evaluations with
nothing written in between give the same value. A surface no document models (a file the
project graph reads, say) does not move it.

## A view from a linked store

A `ViewDoc` need not live in the store that runs it (H9; deskops ships its views only in its
package store, decision DA4, and a desk reaches them through the link). `run_view`, `list_views`
and therefore `views run|list` and `GET /views[/<name>]` read the composed index (the store and
the stores it links to, where a linked document is `<link>:ViewDoc:<name>`):

- **Which one a name means.** The local `ViewDoc:<name>` first; else the only linked ViewDoc with
  that name; `<link>:<name>` names a linked one directly. Two or more linked ViewDocs with the
  name and no local one is `SLDBDocumentTargetError('Ambiguous view: <name> (linked in <s1>, <s2>)')`
  (`docs/missing`, 404): sldb does not pick one.
- **Where its file is read.** From the root of the store that tracks it (the linked one), which
  the index records in the node's `facets.source.store_path`, through the read guard of
  `sldb.store.source_read`: a path that resolves outside that root or is a symlink is not read
  (`SLDBDocumentTargetError` naming `outside-root` or `symlink`).
- **What it reads.** The sections select, project and join over the store that calls, never over
  the store the ViewDoc comes from: the view is a definition, the calling store is the data.
- **The catalogue.** `list_views` lists local and linked views by name; a linked view whose name
  another view also has (local or linked) is listed `<link>:<name>`, which `run_view` accepts.
- **The revision** takes the ViewDoc's `content_hash` from the shard of the store that tracks it,
  so editing a linked view moves it too.

## What a run reads (H11)

`run_view` composes the edge index of the calling store alone; it reads the linked stores too
only when something the view evaluates can name one: a section whose `select` has
`include_linked` true or a `ref` or `prefix` behind a link's alias (after the params are filled),
a section with `edges` or `transitions` when a declared reference of the calling store's own
documents names a document behind a link alias, or a ViewDoc that only a linked store tracks
(H9). The criterion reads the definition, never a fixed list, and is conservative: when any
section needs the linked stores, all of them are read. The result does not change: the
revision's shards signature is the calling store's, and a change in a linked store moves the
revision of a view that selects from it (through the rows it reads) and no other.

The composed index outlives the process: `.sldb_cache/composed/<request>.json` of the calling
store holds it (plain JSON, never executed) with the key it was composed under: every federated
store's shard and document-shard state, the models' contracts and this sldb's index version.
Another key, a missing or unreadable file is a miss: the shards are read as before and the file
rewritten. The files a document moved to from outside sldb (`stale`) are checked on every read
against the files on disk, as before.

## CLI and HTTP

- `sldb views run NAME [--param k=v ...] [--store] [--pythonpath] [--format]`: the result
  (`--format json` emits it exactly; the text form lists each section's groups and ids).
- `sldb views list`: `{"views": [{name, title, params, sections: [key...]}]}` of the ViewDocs
  with sections, by name. The projection views stay in `sldb notations` / `GET /views/projection`.
- Both take the standard envelope (`--envelope`): `ok`, `command`, `store`, `data` (the JSON
  above), `warnings`; on failure `error: {type, message}` (`docs/missing` for an unknown view
  or rule, `validate/rejected` for a param or a projection view, `cli/usage` for a malformed
  or repeated `--param`).
- `GET /views` answers what `views list --format json` prints. `GET /views/<name>?k=v` answers
  what `views run` prints, with `ETag: "<revision>"`; a request whose `If-None-Match` names it
  (weak or strong, or `*`) gets `304 Not Modified` with the `ETag` and no body. 404 for an
  unknown view, 400 for a projection view or a param the view rejects. `/views/projection*`
  (SV02) keeps answering as before.

## Reading cost

One evaluation loads the edge index once, builds the rule graph once (only when a section has
`rules` or `transitions`) and reads it over one view of the index shared by every row, and
builds the project graph once (only when `store.yaml` declares one and a section has `edges`).
The tablero above over 200 items evaluates warm in well under a second (q12, measured in
`tests/api/test_views.py`).
