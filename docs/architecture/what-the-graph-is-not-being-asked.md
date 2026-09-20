# What the graph is not being asked

Review, 2026-09-20. Companion to the [absorption ADR](sldb-absorbs-kgdb.md) and its networkx
amendment. Written because the suspicion was raised that sldb underuses its own graph —
*including the parts that were sldb before the fusion* — and the suspicion was right.

## The graph that exists

pron's own store, a mid-sized one:

| | |
|---|---|
| nodes | 1812 |
| edges | 16013 |
| node classes | `sldb_section` 1361, `SurfaceDoc` 271, `sldb_field` 70, `semantic_tag` 37, `SpecDoc` 15, … |
| relations | `tagged_as` 13873, `has_section` 1361, **`implements` 349**, `has_document` 316, `has_field` 70, `semantic_parent` 26, … |

## What was being asked of it, before today

`edges_from`, `edges_to`, a BFS neighborhood, and a structured query with facet and relation
filters. All of them one hop, or a walk of one named relation. The eleven traversal primitives
in `store/graph/traversal.py` had three callers in `src/` between them.

Sixteen thousand edges, and the only questions asked were about one node at a time.

## What it can be asked now

`sldb graph path | cycles | order | components | central | similar`, and the same through
`sldb.api.graph`. On pron's store, immediately:

- **`central`** ranks `spec-11` first, `spec-14` second. That matches what those specs are — the
  addressing model and the MCP surface — and nothing in the repo said so.
- **`components --isolated --type SpecDoc`** returns exactly one: `spec-09`. It is the only spec
  no surface implements. That is a fact about the project nobody could have retrieved.
- **`cycles --relation semantic_parent`** is now part of `sldb edges check`, so a corrupt DAG is
  a check failure instead of a silent wrong answer.

## One correction: the first two are the same graph

This review first listed the semantic DAG and `tagged_as` as two findings. They are one.

A tag's dotted name **is** a path in a graph: `type.knowledge.anchor` serializes
`type -> knowledge -> anchor`. `tagged_as` is the incidence relation of that same structure.
sldb stores one graph as strings and then navigates the strings, next to a graph engine.

The cost is visible in pron's own tag list. Because a dotted name gives a tag exactly one
parent, a concept with two had to be duplicated into parallel trees:

| what it is | where it lives |
|---|---|
| `type.knowledge.anchor` | `workspace.knowledge.anchors` |
| `type.knowledge.surface` | `workspace.knowledge.surfaces` |
| `type.knowledge.explanation` | `workspace.knowledge.explanations` |
| `type.knowledge.projection` | `workspace.knowledge.projections` |
| `type.knowledge.cli_command` | `workspace.knowledge.commands` |
| `type.pron.move` | `workspace.knowledge.ledger` |
| `type.knowledge.spec` | `workspace.source.spec` |

Seven concepts, fourteen nodes, no edge between them. Plus five tags in a second syntax
(`domain:system_architecture`, `entity:cli_command`, `impl:here`, `kind:software`,
`system:pron`) that are isolated roots because they have no dots to hang from.

Once it is one graph: closure is `under(tag)` plus the `tagged_as` sources; multiple parents
collapse the fourteen nodes back into seven; document resemblance is the bipartite projection
of the same graph; `semantic_equivalent` stops being a separate file and is another edge; and
the colon tags stop being a second syntax.

## What is still not being asked, and should be

Three things, in order of how much is being left on the table. The first is now **half done** —
see the phase note at the end. All three are decisions, not just work.

### 1. The "semantic DAG" is the dotted names re-encoded

This is the big one, and it is about the part that was sldb long before kgdb.

`sync_semantic_dag` builds the `semantic_parent` edges from `_prefix_edges(tag)` — purely from
the dotted string. `type.knowledge.anchor` gets a parent `type.knowledge` because of its name,
not because anyone said so. Until 2026-09-20, `se.` navigation did not read those edges at all:
`semantic_children` matched by `startswith` and `get_semantic` matched the tag exactly, so
`se.type.knowledge` answered `[]` with 316 documents hanging under it. A graph of 26 edges and
37 nodes, and deleting it changed no answer.

**Half of this is now done** — the walk and the closure, see the phase note at the end. The two
readers exist; the DAG has a consumer.

What is still true: the edges are still *derived from names*, so the graph still carries no
information the strings did not carry. You cannot say `type.knowledge.anchor` is a kind of
`layer.topology` unless you rename one of them, and meaning goes on being smuggled into names.
Two things are missing for that — an authoring surface for a parent that is not a prefix (the
DAG file can already hold one; nothing writes it), and deciding what a tag's identity is once
it stops being a path.

### 2. `tagged_as` is 87% of the graph and was never a signal

13873 of 16013 edges. Until today nothing projected them: two documents carrying the same nine
tags had no computed relationship. `graph similar` now does the bipartite projection, but
nothing in sldb or pron *uses* it — not `find`, not pron's referent resolution, which is exactly
the place a semantic shell should be asking "what else is like this".

### 3. `find` does not rank

`sldb find` returns matches in whatever order the index yields. With centrality available over
the authored relations, the obvious thing is to rank retrieval by it: of the twelve documents
that match, the one the rest of the store leans on goes first. This is the cheapest of the
three and the one with no semantic decision attached.

## What was deliberately left alone

The hand-rolled BFS in `store/graph/{traversal,neighborhood,executor}.py`. It works, it is
tested, it has callers, and it is on the hot path of every `edges_from`. Rewriting it on
networkx would buy nothing but risk. networkx is for the questions the adjacency maps cannot
answer, not for the ones they answer well.


## Phase 1, done 2026-09-20

`se.` navigation now walks the DAG's edges (`sldb.store.semantic_dag_graph`) instead of matching
tag strings. Every edge is still derived from a name, so the answers are the same and the suite
proves it — except for one quirk the string matching had and nobody meant: it listed a child
only when that child had children of its own, so `se.layer` could not reach `layer.topology`
even though the tag existed. Leaves are navigable now.

What phase 1 buys is the door: a parent declared by hand in the DAG file, which has always been
possible to write and impossible to see, is now an edge like any other.

**Closure, same day.** `se.<tag>` now reaches the tag's whole subtree: `se.type.knowledge`
answers with its 316 documents instead of `[]` (271 surfaces, 15 specs, 13 explanations, 10
commands, 5 anchors, a projection and a readme). A glob keeps its old reading, so `se.type.*`
still matches tag by tag; only a plain tag names a subtree. `gse.` closes the same way — a
document is reachable by its own tags, by what they hang from, and by the global tags those are
declared equivalent to.

What is left of phase 2: an authoring surface for a parent that is not a prefix, and the
deduplication of the fourteen nodes.
