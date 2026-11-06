# Project graph: declared edges and source nodes, configured by data

`sldb.api.project_graph(store)` is the declared-edge graph of a project (a desk, a repository):
its documents and files as nodes, and the references its documents declare as edges. The
project only configures *where* its documents live, *which* files are nodes and *which* fields,
sections and patterns declare references; sldb reads the rest from the store's edge index and
from the files. It is node GD21 of the plan `generalizar-desde-deskops`: the project graph the
deskops closeout kept as Python (extractors and a `closed_document` hook) becomes data a
`store.yaml` declares, served by the CLI and by `sldb serve`.

## The configuration

`sldb.api.ProjectGraphConfig` and its parts are frozen pydantic models and **plain data**:
`ProjectGraphConfig.from_mapping(mapping)` loads them from a YAML-shaped mapping and
`config.to_mapping()` dumps them back, so that `from_mapping(to_mapping(c)) == c`. A store
declares the configuration in `.sldb/store.yaml` under the key `project_graph`
(`sldb.api.StoreDeclaration.project_graph`); the same `from_mapping` validates it there.

| Key | Type | Meaning |
|---|---|---|
| `document_extractor`, `file_extractor`, `edge_extractor` | str | The `extractor` stamped on document nodes, file nodes, edges and missing targets (name and version of the reading). |
| `surfaces` | list of `DocumentSurface` | Where one kind of document lives: `kind`, `directory`, `pattern` (glob below the directory), `suffixes`, `excluded_names`, `excluded_parts`, `identity` (`path`, `document_id`, `document_id_or_slug`), `closed` (see below). The node id is `kind:identity`. |
| `file_rules` | list of `FileRule` | Ordered rules making project files nodes (`kind`, `file_kind`, `path_prefixes`, `suffixes`, `hidden_name`, `stem_keywords`); the first match wins; the node id is `kind:path`. |
| `exclusions` | `FileExclusions` | What the file walk never reads: `directories` (names, at any depth), `path_prefixes`, `suffixes`, `path_endings`. |
| `declared_file_targets` | list of `DeclaredFileTargets` | A frontmatter `field` (in `directory`/`pattern` documents) whose value is a project file that must be a node (`kind`, `file_kind`, `source_kind`). |
| `reference_fields` | list of `ReferenceField` | Mapping fields (frontmatter, fenced YAML blocks) holding references: `path` (keys from the top), `target_prefix`, `default_role`, `allowed_roles`, `scalar_only`, `index_owned`. |
| `read_yaml_blocks` | bool | Also read `reference_fields` in fenced YAML blocks of the body (default true). |
| `fields_by_kind` | map kind → list of fields | Model-declared reference fields of each node kind, read from frontmatter. |
| `fields_by_model` | map model → list of fields | Fields whose edges the store index owns, per tracked model (the document's text is not read for them). |
| `kind_by_model` | map model → kind | Node kind of each model, naming the targets the index leaves unresolved. |
| `provenance_fields` | list of fields | Fields recording where a document came from: they link while the source exists and are never missing. |
| `section_mentions` | list of `SectionMentions` | Patterns read under headings: `headings` (lower-cased), `patterns` (`MentionPattern`: `regex`, `target` template), `role`, `kinds`. |
| `line_mentions` | list of `LineMentions` | Patterns read on every line of some `kinds`: `patterns`, `role`, `locator`, `excluded_path_prefixes`, `skipped_frontmatter_fields`. |
| `missing_target_kinds` | list of `MissingTargetKind` | The kind a dangling path target gets: `parts`, `one_of_first`, `ending`, `kind`. |

Loading refuses, with a `ValueError` whose message names the path of the key:

- a key that is no field of the model (`project_graph.surfaces[0].closed_document: unknown key`);
- a value that is not a scalar, a list or a mapping (`project_graph.surfaces[0].closed:
  function is not data`), which can only arrive through a Python mapping;
- a value of the wrong type or a missing required field (pydantic's message, prefixed with
  the path).

`store.yaml` fails the same way when it is loaded (`load_declaration`), so a store that names
a bad `project_graph` is refused by every command that reads its declaration.

### `closed`: which documents are history

A document is *history* (its edges carry `record: true`) when its frontmatter says
`record: true`, or when its surface's `closed` predicate holds. `closed` is a predicate of the
rules language (`docs/architecture/rules-language.md`, the language of `sldb find --where`),
evaluated with `sldb.api.where_matches` on the document's payload: the edge index's payload
projection when the store tracks the document (nothing is re-extracted), its frontmatter
mapping otherwise. A surface without `closed` is never closed by it; a predicate the language
does not parse is refused when the surface is built.

Transition: `ProjectGraphConfig(closed_document=callable)` still exists as a Python-only
argument, marked deprecated (`DeprecationWarning` when the configuration is built). It never
loads (`closed_document` is an unknown key to `from_mapping` and to `store.yaml`) and never
dumps (`to_mapping` raises naming it). Where a surface declares `closed`, the predicate
decides; the callable only answers for kinds whose surface declares none. It is removed when
its last consumer migrates.

## A neutral example

```yaml
project_graph:
  document_extractor: docs_v1
  file_extractor: files_v1
  edge_extractor: edges_v1
  surfaces:
    - {kind: card, directory: cards, pattern: "*.md", identity: document_id}
    - {kind: note, directory: notes, pattern: "*.md"}
    - {kind: issue, directory: issues, pattern: "*.md", identity: document_id_or_slug, closed: 'status = "closed"'}
  file_rules:
    - {kind: test_file, file_kind: test, path_prefixes: [tests], suffixes: [".py"]}
    - {kind: source_file, file_kind: source, path_prefixes: [src], suffixes: [".py"]}
  exclusions: {directories: [build], path_prefixes: [src/vendored]}
  reference_fields:
    - {path: [topics], target_prefix: "topic:", default_role: mentions, allowed_roles: [mentions, defines]}
  fields_by_kind: {card: [depends_on, notes]}
  fields_by_model: {Card: [notes, depends_on]}
  kind_by_model: {Card: card}
  section_mentions:
    - {headings: [related cards], patterns: [{regex: '\bcard-[a-z0-9-]+\b', target: "card:{0}"}], role: relates}
  line_mentions:
    - {kinds: [card], patterns: [{regex: '(?<![\w/.-])(?P<path>src/[A-Za-z0-9_./-]+\.py)', target: "{path}"}], role: touches, locator: path}
  missing_target_kinds:
    - {parts: [src], ending: ".py", kind: source_file}
```

With `cards/card-a.md` saying `Touches src/app.py and src/gone.py.` on its line 11 and a
`## Related cards` section listing `card-b`, the graph has the nodes `card:card-a`,
`card:card-b`, `source_file:src/app.py`, …; the edges `card:card-a -touches->
source_file:src/app.py` (provenance `cards/card-a.md`, `line:11:path`) and `card:card-a
-relates-> card:card-b`; and the missing target `source_file:src/gone.py` declared at the same
line. The fixture `tests/api/test_project_graph.py` is this example.

## Reading the graph

`sldb.api.project_graph(store)` → `sldb.api.ProjectGraph`:

- `graph.nodes.documents` / `graph.nodes.files`: every `DocumentNode` and `FileNode`;
- `graph.edges_from(node_id)` / `graph.edges_to(node_id)`: the declared edges leaving or
  reaching a node, the same `ProjectEdge` records (`source_id`, `target_id`, `role`,
  `source_kind`, `confidence`, `provenance_path`, `provenance_locator` — `frontmatter` or
  `line:N:<label>` —, `extractor`, `record`), sorted by key;
- `graph.missing_from(node_id)` / `graph.extraction().missing_targets`: declared targets that
  resolve to no node (`MissingProjectTarget`, with the same provenance).

`edges_to` comes from one inverse map of every edge type, built from the whole extraction the
first time it is asked; there are no partial inverse maps per type.

### One graph per process

`project_graph(store)` keeps the graph per process, keyed by the resolved store path, and
rebuilds it only when its signature moves: the store's shards signature
(`store/edge_index/shard_signature.py`), the composed edge index object it read (so the
existing cache invalidation of `sldb.api.transaction` — `forget_caches`, which drops the
composed indexes — drops the graph too), `(path, mtime_ns, size)` of every file it read or
included (surface documents, declaring documents, the files its rules kept after the
exclusions, `store.yaml`) and the mtime of every directory it walked (a new file in one of
them moves it). Checking the signature stats that list: a second call without changes makes
no `os.walk` and no `rglob`; touching an included file, adding a file to a walked directory or
editing `store.yaml` makes the next call rebuild. Excluded files are not observed. Nothing
persists on disk.

## CLI and HTTP

`sldb graph project ...` (with `--store`, `--format text|json|yaml` and the global
`--envelope`):

| Command | Payload |
|---|---|
| `nodes [--kind K]` | `{kind, nodes: [DocumentNode \| FileNode ...]}`, sorted by id |
| `edges --from ID` / `edges --to ID` | `{from, to, edges: [ProjectEdge ...]}`; exactly one of the two (argparse usage error, exit 2, otherwise) |
| `missing` | `{missing: [MissingProjectTarget ...]}` |

`sldb serve` answers the same JSON (no envelope) at `GET /project-graph/nodes?kind=`,
`GET /project-graph/edges?from=|to=` and `GET /project-graph/missing`: 200 with the payload the
command prints with `--format json`; 400 `{"ok": false, "error": ...}` for `edges` with none or
both of `from`/`to`, and for a store whose `store.yaml` declares no (or a bad) `project_graph`.

`GET /edges?from=|to=` also takes `include_linked` (`true`, the default and the output as it
always was; `false` leaves the linked stores out, as `edges_from(..., include_linked=False)`).
