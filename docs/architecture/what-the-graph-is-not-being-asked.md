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

## What is still not being asked, and should be

Three things, in order of how much is being left on the table. None of them is done; all three
are decisions, not just work.

### 1. The "semantic DAG" is the dotted names re-encoded

This is the big one, and it is about the part that was sldb long before kgdb.

`sync_semantic_dag` builds the `semantic_parent` edges from `_prefix_edges(tag)` — purely from
the dotted string. `type.knowledge.anchor` gets a parent `type.knowledge` because of its name,
not because anyone said so. And `se.` navigation does not read those edges at all:
`SemanticUtils.semantic_children` matches tags by `startswith`.

So there is a graph, with 26 `semantic_parent` edges and 37 `semantic_tag` nodes, that carries
no information the strings did not already carry, and that no reader consults. The only
hand-authored part of the semantic layer is `semantic_equivalent`.

What it costs: you cannot say `type.knowledge.anchor` is a kind of `layer.topology` unless you
rename one of them. Meaning has to be smuggled into names.

What it would take: let a tag declare parents that are not prefixes, and make the `se.` address
space walk `semantic_parent` instead of matching strings. That changes what an address space
means, so it is not a refactor — it is a decision.

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
