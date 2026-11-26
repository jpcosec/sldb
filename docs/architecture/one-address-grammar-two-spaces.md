# ADR: One Address Grammar, Two Spaces, Under The Store

- Status: Draft. The owner liked the idea of two address spaces under the store (2026-11-25) but
  has not accepted this decision nor its execution: the review of the model and of the
  operations is still open, and the grammar may change with it (corrected 2026-11-26)
- Date: 2026-11-25
- Decision Maker: the owner (pending)
- Related repos: `sldb`, `IR` (specIR), `deskops`, `graph_ui`, `marcado`
- Plan: `desk/drawer/plans/direccion-unica-estructural-y-semantica/`

## Context

The work on a command taxonomy ([One Command Taxonomy, Served By FastMCP](one-command-taxonomy-served-by-fastmcp.md))
stopped on a prior question: the commands cannot be ordered because what they name is not
ordered. Measured on 2026-11-25:

- The same structural address is written four ways, and none covers everything:
  `st.{Model}.doc.field` (`sldb legacy`), `docs/Model/doc/field` (`fields`, `sections`),
  `Model:name` (relations, rules) and `sldb://document/Model:name` (graph, MCP). Sections are
  outside `st.`; graph ids stop at document and section and do not reach a value.
- The semantic address (`se.tag`, `gse.tag`) only exists under `sldb legacy`.
- A file path and a `module:Class` reference are used as if they were addresses. They are
  locations: a document can move without changing what it is.
- The graph has eight node types (store, model, field, document, section, tag, relation type,
  anchor). They are read alike and written through four different doors.
- A model is one node for every store (`qualify_id` leaves models, fields, tags, relation
  types and anchors unqualified), so "the `TaskDoc` of deskops" cannot be named in the graph.
- The 1,002 authored edges of this store all go from document to document. A `RelationDoc`
  cannot name a section or a field of a document.

[`addressability_model.md`](../addressability_model.md) already defined the two spaces
(`st.` structural, `se.` semantic, a store prefix). Later surfaces grew their own spellings
beside it.

## Decision

1. **Two address spaces, both under the namespace a store gives**, and independent of where a
   thing lives on disk:
   - **structural**: the position of a thing in the containment tree of the store. One thing
     has one structural address and one address names one thing. It is its identity.
   - **semantic**: what a thing is or is about, as a position in the DAG of tags. One address
     names a set of things and one thing answers to several addresses. It resolves to
     structural addresses.

2. **One grammar**, with one parser and one resolver in the store layer:

   ```
   [store:]st/<Model>                        a model
   [store:]st/<Model>/@<field>               a field of the model (schema)
   [store:]st/<Model>/<doc>                  a document
   [store:]st/<Model>/<doc>/<field>/<sub>…   a value inside the document
   [store:]st/<Model>/<doc>#<section>        a section
   [store:]se/<tag.with.dots>                everything that carries that meaning
   ```

   `store:` omitted is the local store. A relation type and an anchor are documents and are
   addressed as such; a tag is addressed in the semantic space.

3. **The structural address is the node id of the graph.** The `sldb://` ids are replaced by
   it. A value inside a document is not a node of its own: it is the document node plus the
   path inside it, as a URL fragment.

4. **Models are qualified by the store that owns them** (`deskops:st/TaskDoc`). This reverts
   the "one vocabulary across stores" rule for models and carries out points 1, 3 and 4 of
   [Model Federation On The Graph](model-federation-on-the-graph.md).

5. **An edge may end at any structural address**, not only at a document.

6. **The other spellings become input aliases.** `docs/Model/doc/field`, `Model:name`,
   `st.{Model}.doc.field` and `sldb://…` are normalised on the way in; every output prints the
   canonical form. They are removed once the consumers have migrated.

7. **What has to migrate, migrates.** Compatibility with the current ids is not a constraint
   on the design (owner, 2026-11-25).

## Consequences

- `EDGE_INDEX_VERSION` goes up and every edge index is rebuilt.
- specIR, deskops, `graph_ui` and `marcado` read or write the current ids and have to move.
  Files that name `sldb://` outside generated shards, on 2026-11-25: `sldb/src` 37,
  `sldb/tests` 42, `graph_ui` about 8 source files, `IR` 5, `deskops` 4. `marcado` has 1,091,
  all generated shards under the old `.sldb/runtime/` layout.
- The validation of an edge against its `RelationTypeDoc` checks model types today; with
  endpoints below the document it checks the model of the endpoint's document.
- The command taxonomy is written after this: an operation takes an address.
- The plan [grafo-datalog-daemon](../../desk/drawer/plans/grafo-datalog-daemon/) stores the
  same nodes and edges in an engine. The order between its storage node and the change of ids
  is open.

## Not solved by this

- A section address breaks when its heading changes, and a list position shifts when an item
  is inserted. `addressability_model.md` already says so.
- The four doors for writing (a document, the Python code of a model, `store.yaml`, and a tag
  that exists because something carries it) stay as they are.

## Not verified

- How many of the `sldb://` uses in `graph_ui` and specIR are ids kept in their own stored
  data, and not only code.
- Whether a rule can take as subject something that is not a document once the address
  reaches below it.
