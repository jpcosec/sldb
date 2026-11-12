# Tag namespaces: declared in `store.yaml`, checked as a rule family, read as a tree

Node GD27 of the plan `generalizar-desde-deskops`. A document's tags (`tags` or
`semantic_tags`) may carry a namespace: `area:a.b` belongs to `area`, the text before the
first colon; what follows is the value (it may hold colons). A tag without a colon belongs to
no namespace and is never checked. The store declares its namespaces in `.sldb/store.yaml`,
beside `models` and `include`:

```yaml
tag_namespaces:
- name: area                 # what precedes the first colon
  hierarchical: true         # a.b.c is a path: a, a.b and a.b.c are tags too (default)
  folder_axis: true          # declarative: the value is the document's folder (tag_folder)
  anchored_by:               # optional: every required tag must be the `tag` of an Anchor
    model: Anchor
    field: tag
- name: kind
  hierarchical: false        # the value is one piece: no prefixes
- name: domain
  anchored_by:
    model: CrossroadDoc
    field: path
    value: bare              # the field holds `a.b`, the value without `domain:` (default: tag)
tag_models: [AtomDoc]        # optional: the family checks only these models and their descendants
```

`sldb.api.TagNamespace` (`src/sldb/api/stores/tag_namespace.py`) is one entry; its invariants
are its validators: a name without colon or blanks, `anchored_by` exactly `{model, field}`
plus an optional `value` (`tag` or `bare`), no other key; `StoreDeclaration.tag_namespaces` refuses a repeated name. A declaration without
the key reads and writes as before it existed. `sldb tags namespaces` lists what is declared.

### `anchored_by.value` (GD27 for deskops, CC35d H1)

`value: tag` (the default, and what a declaration without the key means) reads the anchor's
`field` as a complete tag: `area:a.b` anchors `area:a.b`, a value of another namespace anchors
nothing. `value: bare` reads it as the value without the namespace: a `CrossroadDoc.path` of
`a.b` anchors `domain:a.b`; a field that already carries `domain:` (or is blank, or is not text)
anchors nothing. `TagNamespace.anchor_tag(field_value)` is that decision; the tags the
namespace requires, `missing` and the tree are always complete tags.

### `tag_models` (GD27 for deskops, CC35d H2)

`StoreDeclaration.tag_models` (a list of model names, empty by default and then not dumped)
limits the family to the documents whose model is listed or has a listed one among its
`base_models`. The tags of other documents are not checked: neither `on_write`, `on_check`,
`rules check` nor `tags check` report them, and `rules explain` of the family on such a
document holds with `clause: model in tag_models` and `seen: {model, tag_models}`. The
anchors are never filtered: any local document of the `anchored_by` model anchors. In
`tag_tree`, a tag is used (and so orphan, or what places an anchor) only through documents in
scope; roots and anchors are as without it. It is store-wide, not per namespace, because the
case it solves is an undeclared namespace, which has no entry to say "does not apply". Model
names are not checked against the registered ones (a misspelt one leaves the scope empty).

## What the family checks

The checks are the built-in rule family `builtin:tag_namespace:<name>`
(`src/sldb/api/rules/builtin_tag_rules.py`), one rule per namespace a document names, not a
RuleDoc of the user (q3: the rules language has no anchor predicate). On a document, the rule
of namespace `<name>` holds when:

1. `<name>` is declared (`clause: namespace declared`; `seen: {namespace, tags, declared}`);
2. with `anchored_by`, every tag the namespace **requires** for each of its values is the
   `field` of a local document of `model` (`clause: each prefix anchored by Model.field`;
   `seen: {namespace, tags, missing}`, `missing` top-down, once each). A hierarchical
   namespace requires every prefix of the value, the whole value included (`area:a.b.c`
   requires `area:a`, `area:a.b` and `area:a.b.c`); a non-hierarchical one requires the value
   alone. The document being written counts as an anchor of the tag it carries in that field.

Without `anchored_by`, declaring the namespace is all a tag needs. Every finding is an
`error` with code `rules/builtin:tag_namespace:<name>`, the subject is the document's export
id and `what` is `<clause> (seen: <seen>)`, the form of a RuleDoc's finding (rules.md §4).

The family runs where the RuleDocs run (rules.md §9), also in a store that registers no
`RuleDoc` but declares `tag_namespaces`:

| Moment | Where | Effect |
|---|---|---|
| `on_write` | `save_document_payload` (so `fields update`, `docs update`, `transaction.update`, `apply_batch`, `POST /save`) and `replace_text` | an error is `SLDBRuleViolationError` (`rules/violation`, exit 1) and nothing is written |
| `on_check` | `stores check`, `on_check_findings` | the findings follow the `on_check` RuleDocs' (not cached) |
| `rules check [--subject]` | `rules_check` | the findings follow the RuleDocs', on the same documents |
| `rules explain builtin:tag_namespace:<name> DOC` | `rules_explain` | `{"rule", "subject", "finding": {node, holds, clause, seen}}`, also when it holds; without `tag_namespaces` the rule is an unknown target |
| `tags check` | `tag_check` | the same evaluation as `rules check` filtered to the family; exit 1 on an error |

`create_document` and `track_document_file` evaluate `on_write` as a save does (H4, so do
`apply_batch`, `POST /save` with create or track, `transaction.create` and `transaction.track`,
and `scaffold_store`): a document that enters with a tag whose prefixes are not anchored is
refused with `SLDBRuleViolationError` and nothing is written or tracked. There is no earlier
index for a new document: the family reads it with its model, its tags and the new payload,
and no previous edges. `stores build` (the batch tracking of `include`) does **not** evaluate
`on_write`: it is declarative, and `stores check` covers what it tracked with `on_check`
(a decision of the coordinator, revisable).

### Which documents the family sees (H7)

The family reads **indexed** documents only. A Markdown file written by hand has no findings
until it is tracked (`docs track`, `track_document_file`, `stores build`); an edited document is
evaluated over its indexed projection, i.e. what the index holds after the last write or
`stores update`, not over the text on disk. Run `stores update` after hand edits.

## `tag_tree`, `tag_folder`

`sldb.api.tag_tree(store, namespace)` (`sldb tags tree NAMESPACE --format json` emits the same
object, in the envelope's `data`):

```json
{"namespace": "area",
 "roots": [{"tag": "area:a", "document": "Anchor:a",
            "children": [{"tag": "area:a.b", "document": "Anchor:ab", "children": []}]}],
 "orphans": [{"tag": "area:c", "used_by": ["Note:n2"]}],
 "unplaced": [{"tag": "area:a.x", "document": "Anchor:ax"}]}
```

- Everything is limited to the namespace asked; tags are complete (`area:a.b`); each level
  is alphabetical by tag; an undeclared namespace is `SLDBStoreError`.
- With `anchored_by`, `roots` is the anchors' tree: every prefix of an anchored value is a
  node, `document` its anchor's export id or `null` for a prefix without one; `orphans` are
  the tags local documents use that no anchor declares (`used_by`: their export ids);
  `unplaced` are the anchors no local document uses, directly or, when hierarchical, through
  a tag under them (an anchor of `area:a` is placed by a document tagged `area:a.b`).
- Without `anchored_by`, `roots` nests the tags local documents use (`document: null`) and
  both lists are empty. A non-hierarchical namespace has roots without children.

`sldb.api.tag_folder(tag)` is a pure function of the text: `a.b` or `area:a.b` -> `a/b`, one
segment per part (`a` -> `a`); it never reads the store (`folder_axis` is the declaration that
tells a consumer to use it). A blank value, an empty segment (`a..b`, `.a`, `a.`) or a slash
inside a segment is a `ValueError` naming the value. It stays strict on purpose (CC35d H3):
a consumer that derives folders from a `folder_axis` namespace keeps those tags out of its own
documents (deskops forbids them in its atom pattern) instead of having them silently skipped.

## API and CLI

- `sldb.api.tag_namespaces(store) -> list[dict]`, `tag_tree(store, namespace) -> dict`,
  `tag_folder(tag) -> str`, `tag_check(store) -> list[Finding]`, `tag_evaluations(store) -> list[dict]` (also in `sldb.api.tags`);
  `sldb.api.TagNamespace`.
- `sldb.api` re-exports `sldb.api.semantic`: `add_semantic_parent`, `remove_semantic_parent`,
  `add_semantic_equivalence`, `semantic_tag`.
- `sldb tags namespaces | tree NAMESPACE | check` (`--store`, `--pythonpath`, `--format`,
  with envelope). `tags check` prints as `rules check` does; in JSON it is `{"findings": [...], "evaluations": [...]}` (H6): one entry `{document, namespace, rule, holds, clause, tags, missing}` per local document and namespace it carries, held or not, from the same pass as the findings. `Finding` has no new field: the node stays in `subject` and the clause in `what`; `rules explain` already returns `node, holds, clause, seen`.
- Helpers of the store layer (`src/sldb/store/semantic_tags.py`): `payload_tags`,
  `split_namespace`, `namespaced_tags`, `tag_prefixes`.

## Hypotheses

- The anchors are read from the local store only (linked stores do not anchor).
- `anchors_of` reads every local document per evaluation: a sweep over a store of N
  documents is O(N²) dictionary reads. Enough for the stores seen so far; a cache keyed by the
  rule graph is the next step if it is not.
- `tags check` and `stores check` recompute the family every time (no `.sldb_cache/rules`
  entry): the family has no `content_hash` to key it by.
