FILE:desk/tasks/task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest.md
---
sldb:
  by: agent
  at: '2026-11-17T15:02:32Z'
  authority: generated
  via: save_document_payload
id: task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/cli/parsers/graph.py
- src/sldb/cli/parsers/stores.py
- src/sldb/cli/commands/help_texts_graph.py
- src/sldb/store/graph/ingest_sldb.py
- src/sldb/selfdoc/python_source_graph.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Limpieza de cáscaras vacías de la API y de los residuos de kgdb (graph parser, help_texts_graph, ingest_sldb, python_source_graph)

## Rationale

_Explain why this task exists or the business driver behind it._

Quedan residuos de kgdb y cáscaras vacías: src/sldb/cli/parsers/graph.py, src/sldb/cli/parsers/stores.py (partes), src/sldb/cli/commands/help_texts_graph.py, src/sldb/store/graph/ingest_sldb.py y src/sldb/selfdoc/python_source_graph.py, además de módulos de la API que solo reexportan o no hacen nada. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

Cada uno de esos archivos y cada cáscara vacía de sldb.api queda borrado si nada lo usa, o reducido a lo que se usa, sin cambiar ningún comportamiento observable (CLI, API pública, tests).

## Scope

_State what is in scope and what is out of scope._

Entra: para cada archivo nombrado y cada módulo de src/sldb/api que no tenga lógica propia, buscar usuarios (grep de imports, entrada del CLI, selfdoc) y borrarlo o reducirlo; mantener la API pública declarada en los __all__; anotar en result-summary.md cada archivo con su decisión y su evidencia. CHANGELOG. No entra: cambiar comandos del CLI ni la API pública.

Precisiones (coordinador, bundle-1): cáscara = módulo de src/sldb/api cuyo cuerpo solo tiene docstring, imports, reexports o __all__. Uso = cualquier import o referencia por nombre en src/, tests/, tools/, docs/ o en los entry points de pyproject.toml. Un módulo usado solo para reexportar parte de la API pública declarada en un __all__ se conserva. No se retira ningún subcomando del CLI; en src/sldb/cli/parsers/stores.py solo salen funciones o constantes sin uso. result-summary.md del run-dir lleva la tabla archivo -> borrado|reducido|conservado con la evidencia de grep.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario con grep. 2) Borrar o reducir uno a uno, corriendo los tests de su vecindad. 3) Validation. 4) Informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_backend.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md tiene la tabla archivo -> borrado, reducido o conservado (evidencia); CHANGELOG y commit.

FILE:desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 'Atomize: break the work into the smallest possible child tasks.'
- 'Dedupe: merge overlapping items.'
- 'Clean: delete legacy content that the work makes obsolete (with deskops retire,
  closeout or drawer remove, never by hand).'
- 'Audit existing work before claiming anything is done: check git history for relevant
  commits, verify artifacts exist where specified, and run tests to confirm the current
  state.'
- Resolve contradictory end states between the desk and the repo.
- Bind the pills the task depends on (the task's pills field or deskops bind).
- Keep the Board current; deskops maintains it, so use deskops verbs instead of editing
  it.
- 'Execute with explicit boundaries: scope, touched files and validation targets stated
  in the task.'
- 'After each step, run the context audit: is every aspect of the task covered by
  a pill, are the bound pills still accurate, update or retire the stale ones, and
  bind new ones as needed.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Execution ritual

## Purpose

_Explain why this ritual exists._

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for sldb.

## Trigger

_State when this ritual should start._

Before starting any task, and after each step while implementing it.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-execution gate: ask whether any aspect of the task is ambiguous or not covered by its task file, pills and atoms. If not, proceed. If so, create or request the missing context first; do not proceed until the task is unambiguous.
- The Board (desk/tasks/Board.md) is the single entry point for active work: read it before starting any task.

## Validation

_List the checks that prove the ritual was performed correctly._

- Scope, touched files and validation targets are explicit in the task.
- Every desk reference points at durable repo context: task files, pills, atoms, drawer notes, inbox messages, source files, tests, docs and commits.

## Failure Modes

_List common mistakes this ritual prevents._

- Proceeding with an ambiguous task without creating or requesting the missing context.
- Creating implementation artifacts instead of referencing existing pills.
- Referencing surfaces below the current layer.
- Desk documents pointing at chat memory or other non-durable context.
- Trusting the task file over the code: the task file describes intent; git history is truth.

## Completion

_Describe what completion looks like._

The task's change is implemented within its stated scope and the testing ritual can start.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# Ordered prose steps; not document references
steps:
- 'Invalidate: check whether existing tests are broken by the change; update or delete
  the ones that no longer describe the behavior.'
- 'Verify: add new tests where the change needs them.'
- 'Test: run the relevant test or validation suite, smallest first, then the full
  suite when shared behavior changed. All required checks must pass.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Testing ritual

## Purpose

_Explain why this ritual exists._

No task is complete without testing. Run the smallest relevant validation first, then broaden coverage when sldb changes shared behavior.

## Trigger

_State when this ritual should start._

When the implementation of a task is done, before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- All required checks pass: the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims.

## Failure Modes

_List common mistakes this ritual prevents._

- Skipping tests to get it done.
- Declaring a check green from truncated output (a pipe through tail hides the exit status).

## Completion

_Describe what completion looks like._

Every required check passes on the final change.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- Update the CHANGELOG when the change is user-visible or release-relevant.
- 'Run the context audit: check the task''s pills, update stale ones, and retire the
  ones whose knowledge now lives in code or docs.'
- 'Close the task with deskops closeout (commit, or supersede/retire when it was already
  resolved): the task leaves the Board in the same atomic commit as its evidence.
  Completed tasks are not kept on the Board.'
- 'Commit atomically, only when the execution ritual is complete. Commit when a phase
  or slice objective is fully checked (a concise scoped message), for a critical bug
  fix mid-phase (fix(<scope>): <description>), or for chores such as dependencies
  or config (chore(<scope>): <description>). A slice that is not done is not a commit:
  work in progress is not committed.'
- 'Write commit messages as <type>(<scope>): <description>, with type one of feat,
  fix, docs, refactor, chore, test, perf, and scope the smallest accurate repo area,
  component, command or workflow surface.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Closeout ritual

## Purpose

_Explain why this ritual exists._

Close a sldb task only after validation passes, the board is updated, and the final change is ready to commit.

## Trigger

_State when this ritual should start._

When the testing ritual passes for a task.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-completion audit, git history: the commits match the completed work; on a mismatch, correct the commit history or update the task state to reflect reality.
- Pre-completion audit, artifacts: every specified output exists at the specified location; implement the missing ones.
- Pre-completion audit, tests: all pass; fix failing tests first.
- Pre-completion audit, clean tree: every untracked file is either gitignored or tracked; clean up a dirty tree before declaring done.
- Trust the code, not the task file: the task file describes intent, git history is truth.

## Validation

_List the checks that prove the ritual was performed correctly._

- deskops closeout verify reports the tests, commit and atom gates as passing, and the tree is clean.

## Failure Modes

_List common mistakes this ritual prevents._

- Marking a task complete without auditing git history.
- Committing with untracked files (gitignore or track them first).
- Force-pushing to hide failures.
- Committing work in progress.

## Completion

_Describe what completion looks like._

The closing commit exists, the task is off the Board, and the tree is clean.

FILE:desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 'Compile: rebuild when applicable (bundles, dist).'
- 'Audit: run the relevant tests and quality checks.'
- 'Regress: fix any test failure.'
- 'Flow: move the pill knowledge that is still needed into code or docs, capture phase-level
  learning into an atom, and retire the redundant pills.'
- 'Advance: clear the Board for the next phase and move on.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Phase ritual

## Purpose

_Explain why this ritual exists._

Close the active phase only when every task on the sldb board is complete, capture any phase-level learning into an atom, and clear the board for the next phase.

## Trigger

_State when this ritual should start._

When every task in a phase or delivery slice is done.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- Tests and quality checks pass and no pill repeats what code or docs already say.

## Failure Modes

_List common mistakes this ritual prevents._

- 

## Completion

_Describe what completion looks like._

The Board holds only the next phase's tasks.

FILE:src/sldb/cli/parsers/graph.py
"""`sldb graph`: query, traverse, analyse and snapshot the store's graph."""

from __future__ import annotations

import argparse

from sldb.cli.parsers.graph_analysis import add_analysis_commands
from sldb.cli.parsers.graph_project import add_project_commands


def add_graph_group(s: argparse._SubParsersAction) -> None:
    """Register `graph get|list|query|neighborhood|path|cycles|order|components|central|similar|snapshot|ingest-sldb|project`."""
    p = s.add_parser("graph", help="Query, traverse and snapshot the store's graph.")
    sub = p.add_subparsers(dest="graph_command", required=True)
    _add_read_commands(sub)
    add_analysis_commands(sub)
    _add_snapshot(sub)
    _add_ingest(sub)
    add_project_commands(sub)


def _add_read_commands(sub) -> None:
    _add_get(sub)
    _add_list(sub)
    _add_query(sub)
    _add_neighborhood(sub)


def _add_get(sub) -> None:
    p = sub.add_parser("get", help="One node from the store's edge index.")
    p.add_argument("node", help="Node id `sldb://<kind>/...` or export id `Model:name`.")
    _read_args(p)


def _add_list(sub) -> None:
    _read_args(sub.add_parser("list", help="All node ids in the store's edge index."))


def _add_query(sub) -> None:
    p = sub.add_parser("query", help="Run a structured query from a JSON file.")
    p.add_argument("--query-file", required=True, help="Path to a JSON StructuredQuery file.")
    _read_args(p)


def _add_neighborhood(sub) -> None:
    p = sub.add_parser("neighborhood", help="Nodes within a depth of a starting node.")
    p.add_argument("node", help="Starting node id.")
    p.add_argument("--depth", type=int, default=1, help="Hops to traverse (default 1).")
    p.add_argument("--direction", choices=["incoming", "outgoing", "both"], default="both", help="Direction to traverse.")
    _read_args(p)


def _add_snapshot(sub) -> None:
    snap = sub.add_parser("snapshot", help="Save or load the portable graph.")
    inner = snap.add_subparsers(dest="snapshot_command", required=True)
    _add_snapshot_save(inner)
    _add_snapshot_load(inner)


def _add_snapshot_save(inner) -> None:
    p = inner.add_parser("save", help="Export the store's edge index as node-link JSON.")
    p.add_argument("--output", required=True, help="Where to write the node-link JSON.")
    _read_args(p)


def _add_snapshot_load(inner) -> None:
    p = inner.add_parser("load", help="Read a node-link or snapshot JSON file.")
    p.add_argument("--input", required=True, help="The node-link or snapshot JSON file.")


def _add_ingest(sub) -> None:
    p = sub.add_parser("ingest-sldb", help="Convert an sldb semantic export into node-link JSON.")
    p.add_argument("--input", required=True, help="The sldb_kgdb_semantic_export JSON file.")
    p.add_argument("--output", required=True, help="Where to write the node-link JSON.")


def _read_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--local", action="store_true", help="Leave the linked stores out")
    p.add_argument("--exclude-tag", action="append", default=[], help="Leave out documents carrying this tag (repeatable)")

FILE:src/sldb/cli/parsers/stores.py
from __future__ import annotations
import argparse
from sldb.cli.parsers.stores_merge import add_merge_parsers

def add_stores_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("stores", help="Store lifecycle and federation.")
    sub = p.add_subparsers(dest="stores_command", required=True)
    _init(sub); _add(sub); _remove(sub); _check(sub); _update(sub); _reconcile(sub)
    _semantic_map(sub); _semantic_export(sub); _list(sub); _migrate_hashes(sub)
    _migrate_layout(sub); _declare(sub); _build(sub); _scaffold(sub); add_merge_parsers(sub)

def _init(s):
    i = s.add_parser("init", help="Init .sldb store.")
    i.add_argument("--path", default=".")
    i.add_argument("--force", action="store_true")

def _add(s):
    a = s.add_parser("add", help="Link federated store.")
    a.add_argument("path", help="Store path")
    a.add_argument("--name", help="Store name")
    a.add_argument("--store", help="Local store path")
    a.add_argument("--replace", action="store_true", help="Point a link already recorded under that name here")

def _remove(s):
    r = s.add_parser("remove", help="Remove a store link; refused while a model here is inherited from it.")
    r.add_argument("name", help="Link name")
    r.add_argument("--store", help="Local store path")

def _check(s):
    c = s.add_parser("check", help="Integrity check: reports each finding and its category.")
    c.add_argument("--store", help="Store path")
    c.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    c.add_argument("--quiet", action="store_true", help="Only the PASS/FAIL line, without per-document findings")
    c.add_argument("--apply", action="store_true", help="Run what the store's policy answers to each finding: `reindex` and `hook: <command>`")
    c.add_argument("--pythonpath", help="Project path")

def _update(s):
    u = s.add_parser("update", help="Recompute store hashes.")
    u.add_argument("--wait", action="store_true", help="Wait for store lock if busy")
    u.add_argument("--verbose", action="store_true", help="Print individual skip details")
    u.add_argument("--prune-missing", action="store_true", help="Untrack documents whose file no longer exists (reports which)")
    u.add_argument("--store", help="Store path")
    u.add_argument("--pythonpath", help="Project path")

def _migrate_hashes(s):
    m = s.add_parser("migrate-hashes", help="Rename hash_a..hash_d to store/model/source/content.")
    m.add_argument("--store", help="Store path")

def _migrate_layout(s):
    m = s.add_parser("migrate-layout", help="Move the cache from .sldb/runtime/ to .sldb_cache/ (sibling of .sldb/), drop the journal and fix the root .gitignore.")
    m.add_argument("--store", help="Store path")
    m.add_argument("--force", action="store_true", help="Replace an existing, non-empty .sldb_cache/")

def _reconcile(s):
    r = s.add_parser("reconcile", help="Explicitly reconcile a catalog against a subtree.")
    r.add_argument("--path", default=".", help="Subtree to discover")
    r.add_argument("--catalog", help="Catalog store path; defaults to ~/.sldb")
    r.add_argument("--apply", action="store_true", help="Replace catalog entries with discovered stores")
    r.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _semantic_map(s):
    m = s.add_parser("semantic-map", help="Map equivalent semantic concepts.")
    m.add_argument("concept_a", help="First concept")
    m.add_argument("concept_b", help="Second concept")
    m.add_argument("--store", help="Store path")

def _semantic_export(s):
    e = s.add_parser("semantic-export", help="Export semantic payloads.")
    e.add_argument("--store", help="Store path")
    e.add_argument("--pythonpath", help="Project path")
    e.add_argument("--format", choices=("sldb",), default="sldb", help="Payload contract: sldb_kgdb_semantic_export v1")
    e.add_argument("--encoding", choices=("json", "yaml"), default="json")
    e.add_argument("--output", "-o", default="-", help="Output path or -")
    e.add_argument("--rebuild", action="store_true", help="Refresh semantic and section indexes")

def _list(s):
    l = s.add_parser("list", help="List federated stores.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _declare(s):
    d = s.add_parser("declare", help="Print the store.yaml declaration the current index implies.")
    d.add_argument("--store", help="Store path")
    d.add_argument("--write", action="store_true", help="Write it to .sldb/store.yaml")

def _build(s):
    b = s.add_parser("build", help="Rebuild the store from .sldb/store.yaml, the tracked Markdown and the models.")
    b.add_argument("--store", help="Store path")
    b.add_argument("--check", action="store_true", help="Rebuild a scratch copy of the sources and compare, writing nothing here")
    b.add_argument("--keep", metavar="DIR", help="With --check: build the copy in DIR (new or empty) and leave it there, pass or fail, for a later step to read (sldb selfdoc check) without a second build")
    b.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _scaffold(s):
    b = s.add_parser("scaffold", help="Create the folders and seed files .sldb/store.yaml declares; without --apply, report what is pending.")
    b.add_argument("--store", help="Store path")
    b.add_argument("--apply", action="store_true", help="Write them (default: report only)")
    b.add_argument("--format", choices=("text", "json", "yaml"), default="text")

FILE:src/sldb/cli/commands/help_texts_graph.py
GRAPH_HELP = """sldb graph

Query, traverse, analyse and snapshot the store's graph (the edge index).

The graph layer is a structured query language (facet filters,
scope, relation filters) executed over the edge index's _out/_in maps, a BFS neighborhood,
node-link JSON snapshots readable by external consumers, and — on networkx — the analyses that
need the whole graph rather than one hop.

Which relations get walked
  The index mixes two things. `has_document`, `has_section`, `has_field`, `tagged_as` and the
  rest of the builtins are DERIVED: sldb writes them from the store's own structure, and they
  make every document of a model a neighbour of every other one. The rest are AUTHORED: someone
  wrote a RelationDoc saying this implements that.

  The analyses default to the authored relations, because a path or a ranking over the derived
  spine is a truism. Use --relation to name others (repeatable), or --all-relations to walk
  everything.

Examples:
  sldb graph get sldb://model/TaskDoc
  sldb graph list
  sldb graph query --query-file contracts/queries/sldb/documents_tagged_domain_contract.json
  sldb graph neighborhood sldb://model/TaskDoc --depth 2 --direction outgoing
  sldb graph path Spec:spec-11 Spec:spec-02
  sldb graph path Spec:spec-11 Spec:spec-02 --all --cutoff 4
  sldb graph cycles --relation semantic_parent
  sldb graph order --relation extends --layers
  sldb graph components --islands --type SpecDoc
  sldb graph components --isolated --type SpecDoc
  sldb graph central --kind pagerank --limit 10
  sldb graph similar Spec:spec-11 --limit 5
  sldb graph snapshot save --output graph.json
  sldb graph ingest-sldb --input export.json --output graph.json

Subcommands:
  get           One node from the store's edge index, as JSON
  list          All node ids in the store's edge index
  query         Run a StructuredQuery JSON file over the store's edge index
  neighborhood  Node ids within a depth of a starting node
  path          How two nodes connect: the shortest chain, or every route with --all
  cycles        Cycles in the relations walked; silence means it is a DAG
  order         The nodes in dependency order, or in levels with --layers
  components    What hangs together; --islands drops the largest, --isolated lists the loners
  central       What the store leans on: pagerank, betweenness, degree, in_degree, out_degree
  similar       What resembles a node, by targets they share (tags by default)
  snapshot      save: export the edge index as node-link JSON; load: read one back
  ingest-sldb   Convert an sldb_kgdb_semantic_export file into node-link JSON

--type filters different things on purpose
  For `components --islands` it restricts the graph: "which specs hang together" is a question
  about the subgraph the specs induce. For `components --isolated`, `central` and `similar` it
  filters the answer, because there the rest of the graph is what produces it — a spec every
  surface implements is not isolated just because no other spec points at it, and dropping the
  tags leaves nothing for two documents to resemble each other through.

PageRank needs scipy, which sldb does not require: `pip install 'structuredLanguageDB[graph]'`. Every other
analysis is pure networkx.
"""

FILE:src/sldb/store/graph/ingest_sldb.py
"""`sldb_kgdb_semantic_export` v1 -> GraphSnapshot.

The contract name is frozen with the `sldb://...` node ids: renaming a data contract breaks
every reader of files already written, so a format change goes behind a new contract version,
never a rename. sldb writes only `sldb_kgdb_semantic_export`. Unreleased main briefly wrote
`sldb_semantic_export`; a payload under that name is still read, never written.
"""

from __future__ import annotations

from typing import Any

from sldb.store.graph.ingest_sldb_nodes import (
    _document_node,
    _model_node,
    _section_node,
    _semantic_tag_node,
    _store_node,
)
from sldb.store.graph.snapshot import GraphSnapshot

CONTRACT_NAME = "sldb_kgdb_semantic_export"
LEGACY_CONTRACT_NAMES = ("sldb_semantic_export",)  # read, never written
CONTRACT_VERSION = 1


def sldb_semantic_export_to_snapshot(payload: dict[str, Any]) -> GraphSnapshot:
    """Convert an SLDB semantic export payload into a graph snapshot."""
    _validate_contract(payload)
    provenance = _base_provenance(payload)
    tag_ids = _collect_semantic_tags(payload)
    return GraphSnapshot(version="1.0", nodes=_build_nodes(payload, provenance, tag_ids), metadata=_metadata(payload))


def _validate_contract(payload: dict[str, Any]) -> None:
    contract = payload.get("contract", {})
    if contract.get("name") not in (CONTRACT_NAME, *LEGACY_CONTRACT_NAMES) or contract.get("version") != CONTRACT_VERSION:
        raise ValueError(f"Expected {CONTRACT_NAME} version {CONTRACT_VERSION}")


def _base_provenance(payload: dict[str, Any]) -> dict[str, Any]:
    return {"contract": payload["contract"], "producer": payload["producer"], "store": _store_provenance(payload["store"])}


def _store_provenance(store: dict[str, Any]) -> dict[str, Any]:
    return {"root": store["root"], "store_path": store["store_path"], "hash_a": store["hash_a"], "runtime_sources": store.get("runtime_sources", {})}


def _collect_semantic_tags(payload: dict[str, Any]) -> set[str]:
    tags: set[str] = set()
    for model in payload["models"]:
        tags.update(model["semantics"])
    for document in payload["documents"]:
        tags.update(document["semantic_tags"])
    for section in payload["sections"]:
        tags.update(section["semantic_tags"])
    return tags | _dag_tags(payload["semantic_dag"])


def _dag_tags(dag: dict[str, Any]) -> set[str]:
    tags: set[str] = set()
    for node in dag["nodes"]:
        tags.add(node["id"])
        tags.update(node["parents"])
    for tag, equivalents in dag["equivalences"].items():
        tags.add(tag)
        tags.update(equivalents)
    return tags


def _build_nodes(payload: dict[str, Any], provenance: dict[str, Any], tag_ids: set[str]) -> list:
    store_node_id = "sldb://store"
    nodes = [_store_node(payload, store_node_id, provenance)]
    nodes += [_semantic_tag_node(tag, payload, provenance) for tag in sorted(tag_ids)]
    nodes += [_model_node(m, _documents_of(payload, m), store_node_id, provenance) for m in payload["models"]]
    nodes += [_document_node(d, _sections_of(payload, d), provenance) for d in payload["documents"]]
    nodes += [_section_node(s, provenance) for s in payload["sections"]]
    return nodes


def _documents_of(payload: dict[str, Any], model: dict[str, Any]) -> list:
    return [d for d in payload["documents"] if d["model"] == model["name"]]


def _sections_of(payload: dict[str, Any], document: dict[str, Any]) -> list:
    return [s for s in payload["sections"] if s["document_id"] == document["id"]]


def _metadata(payload: dict[str, Any]) -> dict[str, Any]:
    return {"source_contract": payload["contract"], "producer": payload["producer"], "store": payload["store"], "generated_from": CONTRACT_NAME}

FILE:src/sldb/selfdoc/python_source_graph.py
"""Project static Python facts into a KGDB GraphSnapshot payload."""
from __future__ import annotations

from datetime import datetime, timezone

from .python_source_values import relative_module
from .python_reexports import module_bindings, resolve_import
from .python_shadowing import active, mark_shadowed
from .python_tag_inheritance import apply_effective_tags


def source_snapshot(files: list[dict], system: str) -> dict:
    """Build a self-contained, regenerable source graph snapshot."""
    symbols = {f"{file['module']}:{symbol['name']}": symbol["id"] for file in files for symbol in file["symbols"]}
    modules = {file["module"]: file["id"] for file in files}
    nodes = {file["id"]: _module_node(file, system) for file in files}
    nodes.update({symbol["id"]: _symbol_node(file, symbol, system) for file in files for symbol in file["symbols"]})
    apply_effective_tags(files, nodes)
    reexports = module_bindings(files)
    for file in files:
        mark_shadowed(file)
        _edges(file, nodes, modules, symbols, reexports)
    return {"version": "1.0", "created_at": _now(), "nodes": list(nodes.values()), "metadata": _metadata(files, system)}


def _module_node(file: dict, system: str) -> dict:
    return _node(file["id"], "python_module", file["metadata"], file, system)


def _symbol_node(file: dict, symbol: dict, system: str) -> dict:
    return _node(symbol["id"], "python_symbol", symbol["metadata"], file, system, symbol)


def _node(identity, kind, metadata, file, system, symbol=None) -> dict:
    ast = {"module": file["module"], "path": file["path"], "kind": kind}
    if symbol:
        ast.update({"name": symbol["name"], "node_kind": symbol["kind"], "line_start": symbol["line"], "line_end": symbol["end"]})
    return {"identity": {"node_id": identity, "node_type": kind}, "edges": [], "semantics": metadata,
            "ast": ast, "source": {"producer": "sldb.python_ast", "system": system, "sha256": file["hash"], "path": file["path"]}}


def _edges(file, nodes, modules, symbols, reexports) -> None:
    for symbol in file["symbols"]:
        _edge(nodes, symbol["parent"], symbol["id"], "contains", _evidence(file, symbol))
    bindings = _binding_targets(file, modules, symbols, reexports)
    for binding in bindings:
        _edge(nodes, binding["owner"], binding["target"], "imports", binding)
    _reference_edges(file, nodes, bindings, {symbol["id"]: symbol["parent"] for symbol in file["symbols"]})


def _reference_edges(file, nodes, bindings, parents) -> None:
    """One `references` edge per resolved annotation reference; the rest listed as unresolved."""
    for reference in file["references"]:
        target = _reference_target(reference, bindings, parents)
        if target:
            _edge(nodes, reference["owner"], target, "references", {**reference, **_evidence(file, reference)})
        else:
            file.setdefault("unresolved_references", []).append(f"{file['path']}:{reference['line']}: {reference['name']}")


def _reference_target(reference, bindings, parents) -> str | None:
    owner = reference["owner"]
    while owner:
        target = next((item["target"] for item in bindings if item["owner"] == owner and item["local"] == reference["name"] and active(item, reference["line"])), None)
        if target:
            return target
        owner = parents.get(owner)
    return None


def _binding_targets(file, modules, symbols, bindings) -> list[dict]:
    found = []
    for binding in file["imports"]:
        module = relative_module(file["module"], binding["module"], binding["level"], file["path"].endswith("__init__.py"))
        target, via = resolve_import(module, binding["name"], modules, symbols, bindings)
        found.append({**binding, "module": module, "target": target, **({"via": via} if via else {}), **_evidence(file, binding)})
    return found


def _edge(nodes, source, target, relation, metadata) -> None:
    if target not in nodes:
        nodes[target] = {"identity": {"node_id": target, "node_type": "python_external"}, "edges": [],
                         "semantics": {}, "ast": {}, "source": {"producer": "sldb.python_ast"}}
    nodes[source]["edges"].append({"target_id": target, "relation_type": relation, "metadata": metadata})


def _evidence(file, fact) -> dict:
    return {"origin": "python_ast", "path": file["path"], "sha256": file["hash"], "line_start": fact["line"], "line_end": fact["end"]}


def _metadata(files: list[dict], system: str) -> dict:
    unresolved = [entry for file in files for entry in file.get("unresolved_references", [])]
    return {"generated_from": "sldb_python_ast", "system": system, "files": len(files), "extractor_version": 1, "unresolved_references": unresolved}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

FILE:instruccion
Cold-bundle de la tarea task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_backend.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

