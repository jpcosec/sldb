# ADR: SLDB Absorbs KGDB — One Substrate, Two Internal Layers

- Status: Accepted
- Date: 2026-09-20
- Decision Maker: the owner
- Supersedes: [Keep SLDB As The Structured Text Layer And KGDB As The Graph Layer](sldb-text-layer-vs-kgdb-graph-layer.md) (2026-06-19, Proposed)
- Related repos: `sldb`, `kgdb`, `pron`, `graph_ui`, `deskops`

## Context

The 2026-06-19 ADR split the ecosystem in two products: SLDB owned the structured text layer, KGDB
owned the graph layer. It listed "put both text and graph behavior into SLDB" as Alternative 1 and
rejected it, on the grounds that one product would blur document operations and graph operations.

Three months of practice pointed the other way:

- The typed graph was never independent of the store. `kgdb ingest` read SLDB through its library and
  its export contract, and every node and edge it produced was derived from tracked documents. The
  graph was a projection with its own process, not a second source of truth.
- Keeping the projection outside the store cost a whole freshness protocol: a snapshot file that could
  be stale, a hash comparison to detect it, and a consumer-side fallback for when it was. Readers had
  two doors that had to agree, which capped what a reader could rely on to one hop.
- Two repos for one derivation meant two release cycles, two test suites and a subprocess boundary
  (`selfdoc/kgdb_sync.py` shelled out to the `kgdb` binary) for what is one operation.

On 2026-09-17 the assembly half was absorbed: the edge index became a store index, kept per-document
in shards with the same hash chain as `sections` and `semantic`, current after every write. That
removed the stale-snapshot problem and the second door. It also left the query half — traversal,
scope, structured query, portable snapshot — without a home, which this decision closes.

## Decision

**SLDB is one product with two internal layers: a text layer and a graph layer.** KGDB stops being a
separate product. Its capabilities move into SLDB; the `kgdb` package remains for a while as a
compatibility shim that re-exports from `sldb`, and is not deleted on this change.

The boundary the previous ADR drew between repos survives **as a boundary between modules**. It was
right about capability placement and wrong only about packaging. Concretely:

| layer | owns | lives in |
|---|---|---|
| text | authored documents, AST/IR, extraction and rendering, roundtrip, structural and semantic addressing, sections, links and composition, store indexes and hashes | `core/`, `runtime/`, `links/`, `store/` (minus the graph modules) |
| graph | nodes and typed edges derived from documents, traversal, scope, structured query, neighborhoods, portable snapshots | `store/edge_index/`, `store/graph/`, `api/graph/` |

A feature still has to answer the old question — *is this about what a document says, or about what
the corpus implies?* — but the answer now selects a module, not a repository.

### What the graph layer may do, that Consequence D of the previous ADR forbade

The previous ADR told SLDB not to grow multi-hop traversal as a first-class truth model, nor
graph-native analytics. That prohibition existed because the graph was a cache that could disagree
with the store. It cannot anymore: the edge index is rebuilt by the same write that changes the
document, keyed by the same `hash_c`. A traversal is now as trustworthy as reading a field.

So multi-hop traversal, scope, and structured query are in scope for the graph layer. Graph analytics
(centrality, ranking, community detection) stay out — not because of the boundary, but because
nothing in the ecosystem asks for them yet, and because they would bring a graph engine dependency
that the current implementation deliberately avoids (no networkx; adjacency maps and iterative BFS
over the composed index).

> **Amended 2026-09-20 — see [the amendment](#amendment-2026-09-20--networkx-comes-in-after-all).**
> Analytics are in, and networkx with them.

### The write journal belongs to the substrate

Every write that goes through `sldb.api` is recorded by SLDB, in a per-store journal chained by hash.
Until now the only trace of a write was pron's `MoveDoc`, which exists only when someone speaks
through pron: a write from the CLI, from `graph_ui`, from an MCP tool or from a library consumer left
no record at all.

The two records are different things and both stay:

- **a journal entry** is one write: the address, the values before and after, the hashes, the time,
  the actor;
- **a `MoveDoc`** is one turn of a conversation: the sentence, its interpretation, what was read, the
  referents, and the writes it caused.

One turn of pron produces one `MoveDoc` and one or more journal entries. The journal is written by
hand today; in v2 it is expected to fall out of the kernel, where every write is already a transaction.

### pron is a semantic shell

pron is not the door to the world; it is one way of speaking to it. What belongs to pron is the
lexicon derived from the world, the surface from sentence to forms, the dialogue (pending questions
and referents), the move with its prevalidation and its `MoveDoc`, and the projection as what a
speaker may name and do.

What does not belong to pron, and moves here: addressing and reading documents, reading the graph,
ranked retrieval, the low-level CLI, and the agent-facing MCP surface for reads. `graph_ui` is a
graphical UI over SLDB, not a surface over pron.

This is a subtraction for pron, and it is the point: roughly a third of `src/pron` was substrate
wearing a pron hat.

## Consequences

1. `sldb` grows a graph module with query, traversal and portable snapshots, ported from `kgdb` and
   reimplemented without networkx (amended the same week: networkx is now a dependency, see below).
2. `sldb` grows a write journal, and `stores check` gains a chain verification.
3. `kgdb` becomes a shim. Consumers outside this repo keep importing it until they migrate; that
   migration is not a precondition for this change.
4. `pron` sheds its store facade, its graph reader, its corpus and its self-documentation, and keeps
   the shell. Its spec 12 ("pron for an external runtime") shrinks: a runtime that only reads talks to
   SLDB.
5. The MCP surface splits in two levels: SLDB exposes addressing, query, graph and schema; pron
   exposes saying and evaluating forms, and moves with their ledger and undo.
6. The previous ADR stays in the repo as history. It is superseded, not deleted: its reasoning about
   where capabilities belong is what this decision preserves.

## Risks

- **Boundary drift, again.** With one repo, nothing structural stops the text layer from absorbing
  graph concerns or the reverse. The mitigation is the module table above and this document; there is
  no packaging constraint left to enforce it.
- **A larger product.** SLDB was already the biggest piece of the ecosystem; it gets bigger. If the
  split into bounded contexts sketched in `docs/target_architecture.md` ever happens, the graph layer
  is a natural seam.
- **Downstream breakage is deferred, not avoided.** Live consumers (`AWS_Infra`, `TraderBot`,
  `deskops`, `graph_ui`, `legos`, `kb_agent`) import `kgdb` today. The shim buys time; it does not
  remove the work.


## Amendment (2026-09-20) — networkx comes in after all

Four days after the fusion, with the two layers actually in one repo, the analytics prohibition
above was reversed. Recording why, because it reverses a clause of this same document.

### What changed

Two things, and neither is "we changed our minds".

**The reason for the prohibition was the dependency, and the dependency arrived anyway.** The clause
said analytics would "bring a graph engine dependency that the current implementation deliberately
avoids". That was written when the graph layer was a port. It is now the same product as the text
layer, and the consumers that still import `kgdb` do so precisely for its networkx view. The cost was
already being paid, one repo over, by everyone.

**"Nothing in the ecosystem asks for them yet" stopped being true the moment the index was
trustworthy.** A store of 1812 nodes and 16013 edges can be asked which documents nothing reaches,
what the rest leans on, whether the semantic DAG is really acyclic, and how two documents connect.
Before the fusion those questions had no honest answer, because the graph could disagree with the
store. Now they do, and nothing was reading them.

### What was built

`sldb.store.graph.analysis`, on networkx, exposed through `sldb.api.graph` and `sldb graph`:
paths between two nodes, cycles, topological order and layers, connected components and isolated
nodes, centrality (pagerank, betweenness, degree), and resemblance by shared targets.

### Two decisions inside it that are not obvious

**Derived relations are excluded by default.** The index mixes what sldb derives from the store's
structure (`has_document`, `has_section`, `tagged_as`...) with what someone asserted in a
`RelationDoc`. Every document of a model is two hops from every other through the model node, so a
path or a ranking over the derived spine is a truism. An analysis that is not told which relations
to walk walks the authored ones. This is the single most important thing about the layer.

**`node_types` means two different things, on purpose.** For `components` and `islands` it
restricts the graph: "which specs hang together" is a question about the subgraph the specs induce.
For `isolated`, `central` and `similar` it filters the answer, because there the rest of the graph
is what produces it. Both halves of this were found by using the thing, not by design: restricting
the view first made `similar` come back empty, because it deleted the tags two documents resemble
each other through; and the first real run of `components --isolated --type SpecDoc` listed specs
that were also in the top five by PageRank, because no spec implements another spec — every
`implements` edge comes from a surface.

### The dependency, precisely

`networkx>=3.0` is a hard dependency: pure Python, no compiled extensions. PageRank is the one
exception — networkx implements it on scipy — so it lives behind the `graph` extra and raises an
error that names the fix. Every other analysis works on a bare install.

### What this does not change

The ADR boundary holds: SLDB still answers what the ecosystem's documents say and imply about each
other. Analytics over the store's own graph is that question, asked of the whole graph instead of one
hop. Nothing here makes sldb a graph database, and the snapshot format is unchanged.
