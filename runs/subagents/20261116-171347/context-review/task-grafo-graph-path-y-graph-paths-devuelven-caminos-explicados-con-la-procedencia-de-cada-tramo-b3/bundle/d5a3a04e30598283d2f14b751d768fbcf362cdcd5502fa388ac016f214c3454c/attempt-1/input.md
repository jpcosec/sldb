FILE:desk/tasks/task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3.md
---
sldb:
  by: agent
  at: '2026-11-16T16:20:43Z'
  authority: generated
  via: save_document_payload
id: task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/graph/analyze.py
- src/sldb/store/graph/backend/networkx_backend.py
- src/sldb/cli/parsers/graph_analysis.py
- src/sldb/cli/commands/graph_analysis.py
- src/sldb/cli/serve/graph_routes.py
- tests/api/test_api_graph_analysis.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Grafo: graph_path y graph_paths devuelven caminos explicados con la procedencia de cada tramo (B3)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: las reglas e impacto de specIR (IR10) deben apoyarse en sldb. Hoy graph_path y graph_paths en sldb.api.graph devuelven solo listas de ids, sin decir por qué relación ni con qué procedencia se une cada tramo.

## Goal

_Describe the concrete result this task must produce._

Caminos explicados: por cada tramo, origen, destino, tipo de relación, dirección recorrida y procedencia de la arista.

## Scope

_State what is in scope and what is out of scope._

Verificado hoy: graph_path y graph_paths (módulo analyze de sldb.api.graph) devuelven list[str]; el módulo traverse tiene solo targets, sources, children y similares sin camino. No existe pedido ni tarea previa. Añadir una variante o un parámetro que devuelva el camino explicado sin romper la forma actual (compatibilidad con la CLI de graph y sus goldens), pasar por el protocolo GraphBackend, exponerlo en la CLI y en sldb serve si ya exponen graph path. La procedencia sale de la arista del índice (RelationDoc o campo de referencia); cuando una arista tiene varias, decidir y documentar.

Precisiones (coordinador, 2026-11-16): si entre a y b hay varias aristas que pasan el filtro, se listan todas en el tramo (steps[i].edges), ordenadas por precedencia relation_doc > schema > structural > alias; una arista espejo con metadata.reverse true no se lista aparte: aparece como su arista directa con direction backward; evidence no entra en provenance. La forma sin explain no cambia.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Un módulo nuevo path_steps.py en el paquete sldb.store.graph.analysis con explain_path(index, nodes, relations, directed): por cada par consecutivo (a, b) toma las aristas a->b (direction forward) o b->a (direction backward) de index.edges_from/edges_to filtradas por analysis.relations.resolve(index, relations) y emite {source, target, relation, direction, provenance}. provenance = {origin, relation_doc o field, from_store} tomado de EdgeRecord.metadata. 2) Registrar las operaciones path_explained y paths_explained en _OPERATIONS de src/sldb/store/graph/backend/networkx_backend.py componiendo path_between/paths_between con explain_path; las operaciones path y paths no cambian (goldens intactos). 3) src/sldb/api/graph/analyze.py: graph_path y graph_paths ganan explain: bool = False que elige la operación. 4) CLI --explain en src/sldb/cli/parsers/graph_analysis.py y su manejo en src/sldb/cli/commands/graph_analysis.py (70 líneas: la impresión va a un módulo nuevo); sldb serve: path_payload acepta ?explain=1 y agrega steps junto a path. 5) Tests en tests/api/test_api_graph_analysis.py (AnalysisWorld y el índice del propio repo).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_backend.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; graph_path(..., explain=True) sobre el índice del propio repo devuelve tramos con origin y relation_doc o field; los goldens de tests/fixtures/graph_goldens/ no cambian; `sldb graph path --explain` y GET con ?explain=1 lo exponen; CHANGELOG y commit; aviso a IR anotado en result-summary.md.

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

FILE:src/sldb/api/graph/analyze.py
"""Whole-graph analysis of a store: the questions that need more than one hop.

Each function composes the store's edge index, hands it to a `GraphBackend` with `load`, and
asks for one operation with `analyze`. Today the backend is networkx; the commands and the
library see no difference. `relations=None` still means the authored relations — the ones
somebody asserted — because the derived spine makes every document a neighbour of every other
one.

A caller may pass `backend=` to use another implementation (the tests' spy, or a future
engine). Without it, the store's `.sldb/store.yaml` decides, with networkx as the default.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_declaration import declared_graph_backend
from sldb.core.exceptions import SLDBGraphArgumentError
from sldb.store.graph.backend import GraphBackend, make_backend


def graph_path(store, source: str, target: str, relations: object = None, directed: bool = False, backend: GraphBackend | None = None, **index) -> list[str] | None:
    """The shortest chain of nodes connecting two nodes, or None."""
    return _run(store, "path", {"source": source, "target": target, "relations": relations, "directed": directed}, index, backend)


def graph_paths(store, source: str, target: str, relations: object = None, cutoff: int | None = None, limit: int = 10, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """Up to `limit` distinct chains between two nodes, shortest first."""
    return _run(store, "paths", {"source": source, "target": target, "relations": relations, "cutoff": cutoff, "limit": limit}, index, backend)


def graph_cycles(store, relations: object = None, limit: int = 10, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """Cycles in the relations walked; empty when they form a DAG."""
    return _run(store, "cycles", {"relations": relations, "limit": limit}, index, backend)


def graph_order(store, relations: object = None, backend: GraphBackend | None = None, **index) -> list[str]:
    """Every node in dependency order; raises `SLDBGraphCycleError` when not a DAG."""
    return _run(store, "order", {"relations": relations}, index, backend)


def graph_layers(store, relations: object = None, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """The dependency order as levels, each depending only on earlier ones."""
    return _run(store, "layers", {"relations": relations}, index, backend)


def graph_components(store, relations: object = None, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """What hangs together, largest group first."""
    return _run(store, "components", {"relations": relations, "node_types": node_types}, index, backend)


def graph_islands(store, relations: object = None, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[list[str]]:
    """Every group but the largest: what never reaches the main body of the store."""
    return _run(store, "islands", {"relations": relations, "node_types": node_types}, index, backend)


def graph_isolated(store, relations: object = None, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[str]:
    """Nodes with no edge at all in the relations walked."""
    return _run(store, "isolated", {"relations": relations, "node_types": node_types}, index, backend)


def graph_central(store, kind: str = "pagerank", relations: object = None, node_types: object = None, limit: int = 20, backend: GraphBackend | None = None, **index) -> list[tuple[str, float]]:
    """The nodes the rest of the store leans on, with their score."""
    return _run(store, "central", {"kind": kind, "relations": relations, "node_types": node_types, "limit": limit}, index, backend)


def graph_similar(store, node_id: str, relations: object = ("tagged_as",), limit: int = 10, node_types: object = None, backend: GraphBackend | None = None, **index) -> list[tuple[str, int]]:
    """Nodes sharing the most targets with this one: what resembles it, and how much."""
    return _run(store, "similar", {"node_id": node_id, "relations": relations, "limit": limit, "node_types": node_types}, index, backend)


def _run(store: Any, op: str, arguments: dict[str, Any], options: dict[str, Any], backend: GraphBackend | None) -> Any:
    """Compose the index, load it into the backend, and ask for the operation."""
    index = _index(store, options)
    engine = backend if backend is not None else backend_for(open_store(store, mode="readonly").store_path)
    engine.load(index, None)
    return engine.analyze(op, **arguments)


def backend_for(store_path: str | Path | None = None) -> GraphBackend:
    """The backend the store declares; an absent declaration or key means networkx."""
    return make_backend(declared_graph_backend(store_path))


def _index(store, options: dict):
    linked: bool = options.pop("include_linked", True)
    tags: Iterable[str] = options.pop("exclude_tags", ())
    if options:
        raise SLDBGraphArgumentError(f"Unexpected arguments: {', '.join(sorted(options))}")
    return load_edge_index(store, linked, tags)

FILE:src/sldb/store/graph/backend/networkx_backend.py
"""The networkx implementation of the `GraphBackend` seam.

It wraps `sldb.store.graph.analysis` unchanged: every operation receives the composed index
and returns what the analysis returned. The index is kept private; callers only ask for an
operation by name. `eval` is the whole predicate language of GO05 (paths included) over the
index's graph view (`index_view`), on a payload, an `export_id` read through the projection,
or the whole domain.

The seam exists so that a future engine (Kùzu, Neo4j, Datalevin) can sit behind the same three
methods. See `docs/architecture/graph-backend.md`.
"""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.graph import analysis
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_api import findings, node_finding
from sldb.store.graph.language.predicate_view import node, with_node

_OPERATIONS: dict[str, Callable[..., Any]] = {
    "path": analysis.path_between,
    "paths": analysis.paths_between,
    "cycles": analysis.cycles,
    "order": analysis.topological_order,
    "layers": analysis.layers,
    "components": analysis.components,
    "islands": analysis.islands,
    "isolated": analysis.isolated,
    "central": analysis.central,
    "similar": analysis.similar_to,
}


class NetworkXBackend:
    """The current engine: `sldb.store.graph.analysis` over the composed edge index."""

    def __init__(self) -> None:
        self._index: Any = None
        self._projection: dict[str, dict[str, Any] | None] | None = None

    def load(self, index: Any, projection: dict[str, dict[str, Any] | None] | None = None) -> None:
        """Keep the composed index and the optional export-id projection; return nothing."""
        self._index = index
        self._projection = projection
        return None

    def analyze(self, op: str, **args: Any) -> Any:
        """Run one analysis operation with the arguments the analyses already take."""
        if self._index is None:
            raise RuntimeError("GraphBackend.analyze called before load")
        operation = _OPERATIONS.get(op)
        if operation is None:
            raise ValueError(f"Unknown graph operation: {op}")
        return operation(self._index, **args)

    def eval(self, predicate: Any, subject: Any = None) -> list[dict[str, Any]]:
        """`eval(predicate, subject)` of rules-language.md §6 over the loaded index: the
        subject's finding (a payload, or an export id read through the projection), or, with
        no subject, one per document of the domain. Paths read the index's edges."""
        view = index_view(self._index, self._projection)
        if subject is None:
            return findings(predicate, view)
        item = self._subject(view, subject)
        return [node_finding(predicate, with_node(view, item), item)]

    def _subject(self, view: dict[str, Any], subject: Any) -> dict[str, Any]:
        if isinstance(subject, str):
            return {**(view["node"](subject) or node(subject, None, {})), "payload": self._projected(subject)}
        if isinstance(subject, dict):
            return self._payload_subject(view, subject)
        raise TypeError("el sujeto de eval es un payload (dict) o un export_id (str)")

    def _payload_subject(self, view: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        node_id = str(payload.get("id") or payload.get("name") or "")
        known = view["node"](node_id)
        if known is not None:
            return {**known, "payload": payload}
        return node(node_id, payload.get("model"), payload, payload.get("base_models") or ())

    def _projected(self, export_id: str) -> dict[str, Any]:
        if self._projection is None or export_id not in self._projection:
            raise ValueError(f"sin proyección para {export_id}")
        return self._projection[export_id] or {}

FILE:src/sldb/cli/parsers/graph_analysis.py
"""`sldb graph path|cycles|order|components|central|similar`: the whole-graph questions."""

from __future__ import annotations

import argparse

from sldb.store.graph.analysis import KINDS


def add_analysis_commands(sub) -> None:
    """Register the six analysis subcommands under `sldb graph`."""
    _add_path(sub)
    _add_cycles(sub)
    _add_order(sub)
    _add_components(sub)
    _add_central(sub)
    _add_similar(sub)


def _add_path(sub) -> None:
    p = sub.add_parser("path", help="How two nodes are connected.")
    p.add_argument("source", help="Node id to start from.")
    p.add_argument("target", help="Node id to reach.")
    p.add_argument("--directed", action="store_true", help="Follow edges only the way they point")
    p.add_argument("--all", action="store_true", help="Every route, not just the shortest")
    p.add_argument("--cutoff", type=int, help="With --all, the longest route to consider, in hops")
    p.add_argument("--limit", type=int, default=10, help="With --all, how many routes to print (default 10)")
    _walk_args(p)


def _add_cycles(sub) -> None:
    p = sub.add_parser("cycles", help="Cycles in a relation that should be a DAG.")
    p.add_argument("--limit", type=int, default=10, help="How many cycles to print (default 10)")
    _walk_args(p)


def _add_order(sub) -> None:
    p = sub.add_parser("order", help="The nodes in dependency order.")
    p.add_argument("--layers", action="store_true", help="Group the order into levels")
    _walk_args(p)


def _add_components(sub) -> None:
    p = sub.add_parser("components", help="What hangs together, and what hangs alone.")
    p.add_argument("--islands", action="store_true", help="Only the groups outside the largest one")
    p.add_argument("--isolated", action="store_true", help="Only the nodes with no edge at all")
    _walk_args(p)


def _add_central(sub) -> None:
    p = sub.add_parser("central", help="Which nodes the rest of the store leans on.")
    p.add_argument("--kind", choices=list(KINDS), default="pagerank", help="How to measure (default pagerank)")
    p.add_argument("--limit", type=int, default=20, help="How many nodes to print (default 20)")
    _walk_args(p)


def _add_similar(sub) -> None:
    p = sub.add_parser("similar", help="Which nodes resemble this one, by shared targets.")
    p.add_argument("node", help="Node id to compare against.")
    p.add_argument("--limit", type=int, default=10, help="How many nodes to print (default 10)")
    _walk_args(p, default_relation="tagged_as")


def _walk_args(p: argparse.ArgumentParser, default_relation: str | None = None) -> None:
    hint = f" (default {default_relation})" if default_relation else " (default: the authored ones)"
    p.add_argument("--relation", action="append", default=[], help=f"Relation to walk, repeatable{hint}")
    p.add_argument("--all-relations", action="store_true", help="Walk every relation, derived spine included")
    p.add_argument("--type", action="append", default=[], dest="node_type", help="Keep only nodes of this class, repeatable")
    p.add_argument("--store", help="Store path")
    p.add_argument("--local", action="store_true", help="Leave the linked stores out")
    p.add_argument("--exclude-tag", action="append", default=[], help="Leave out documents carrying this tag (repeatable)")

FILE:src/sldb/cli/commands/graph_analysis.py
"""`sldb graph path|cycles|order|components|central|similar` handlers.

Printing wrappers over `sldb.api.graph`'s analysis functions. `--relation` with nothing given
means the authored relations: see `sldb.store.graph.analysis.relations`.
"""

from __future__ import annotations

import json
from typing import Any

from sldb.api.graph import (
    graph_central,
    graph_components,
    graph_cycles,
    graph_islands,
    graph_isolated,
    graph_layers,
    graph_order,
    graph_path,
    graph_paths,
    graph_similar,
)
from sldb.core.exceptions import SLDBError
from sldb.store.graph.analysis import ALL


class GraphAnalysisCLI:
    """The whole-graph questions, as commands.

    `backend` is injected by Python for tests and future engines; without it each analysis
    function selects the store's backend (networkx unless `.sldb/store.yaml` says otherwise).
    """

    def __init__(self, backend: Any = None) -> None:
        self.backend = backend

    def run(self, args: Any) -> int:
        handlers = {
            "path": self._path,
            "cycles": self._cycles,
            "order": self._order,
            "components": self._components,
            "central": self._central,
            "similar": self._similar,
        }
        return handlers[args.graph_command](args)

    def _path(self, args: Any) -> int:
        if args.all:
            return _print(graph_paths(args.store, args.source, args.target, _rel(args), args.cutoff, args.limit, backend=self.backend, **_index(args)))
        found = graph_path(args.store, args.source, args.target, _rel(args), args.directed, backend=self.backend, **_index(args))
        if found is None:
            print(f"No path from {args.source} to {args.target}.")
            return 1
        return _print(found)

    def _cycles(self, args: Any) -> int:
        found = graph_cycles(args.store, _rel(args), args.limit, backend=self.backend, **_index(args))
        if not found:
            print("No cycles: the relations walked form a DAG.")
            return 0
        return _print(found)

    def _order(self, args: Any) -> int:
        call = graph_layers if args.layers else graph_order
        try:
            return _print(call(args.store, _rel(args), backend=self.backend, **_index(args)))
        except SLDBError as cyclic:
            print(str(cyclic))
            return 1

    def _components(self, args: Any) -> int:
        if args.isolated:
            return _print(graph_isolated(args.store, _rel(args), _types(args), backend=self.backend, **_index(args)))
        call = graph_islands if args.islands else graph_components
        return _print(call(args.store, _rel(args), _types(args), backend=self.backend, **_index(args)))

    def _central(self, args: Any) -> int:
        try:
            ranked = graph_central(args.store, args.kind, _rel(args), _types(args), args.limit, backend=self.backend, **_index(args))
        except SLDBError as needs_scipy:
            print(str(needs_scipy))
            return 1
        return _print([{"node": node, "score": score} for node, score in ranked])

    def _similar(self, args: Any) -> int:
        ranked = graph_similar(args.store, args.node, _rel(args), args.limit, _types(args), backend=self.backend, **_index(args))
        return _print([{"node": node, "shared": shared} for node, shared in ranked])


def _rel(args: Any) -> object:
    if args.all_relations and not args.relation:
        return ALL
    return args.relation or _default_relation(args)


def _default_relation(args: Any) -> object:
    return ["tagged_as"] if args.graph_command == "similar" else None


def _types(args: Any) -> object:
    return args.node_type or None


def _index(args: Any) -> dict:
    return {"include_linked": not args.local, "exclude_tags": args.exclude_tag}


def _print(payload: object) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0

FILE:src/sldb/cli/serve/graph_routes.py
"""GET /graph/* routes: whole-graph analysis over the real graph API."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sldb.api.graph.analyze import (
    graph_central,
    graph_components,
    graph_cycles,
    graph_isolated,
    graph_path,
)
from sldb.api.graph.neighborhood import collect_neighborhood
from sldb.cli.serve.params import optional_int, query_params, require_param, require_params


def dispatch_graph(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
) -> tuple[dict[str, Any], int]:
    route = urlparse(handler.path).path
    callback = GRAPH_ROUTES.get(route)
    if callback is None:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return callback(handler, store_path)


def neighborhood_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    node, error = require_param(params, "node")
    if error is not None:
        return error, 400
    depth, error = optional_int(params, "depth", 1)
    if error is not None:
        return error, 400
    nodes = collect_neighborhood(store_path, [node], depth)
    return {"nodes": sorted(nodes)}, 200


def path_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    values, error = require_params(params, "source", "target")
    if error is not None:
        return error, 400
    found = graph_path(store_path, values[0], values[1])
    if found is None:
        return {"ok": False, "error": f"No path from {values[0]} to {values[1]}."}, 404
    return {"path": found}, 200


def cycles_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    limit, error = optional_int(query_params(handler), "limit", 10)
    if error is not None:
        return error, 400
    return {"cycles": graph_cycles(store_path, limit=limit)}, 200


def components_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    return {"components": graph_components(store_path)}, 200


def central_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    limit, error = optional_int(query_params(handler), "limit", 20)
    if error is not None:
        return error, 400
    ranked = graph_central(store_path, limit=limit)
    return {"central": [{"node": node, "score": score} for node, score in ranked]}, 200


def isolated_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    return {"isolated": graph_isolated(store_path)}, 200


GRAPH_ROUTES = {
    "/graph/neighborhood": neighborhood_payload,
    "/graph/path": path_payload,
    "/graph/cycles": cycles_payload,
    "/graph/components": components_payload,
    "/graph/central": central_payload,
    "/graph/isolated": isolated_payload,
}

FILE:tests/api/test_api_graph_analysis.py
"""The whole-graph analyses over a real store, and the `sldb graph` commands that print them."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.graph import graph_central, graph_components, graph_cycles, graph_isolated, graph_order, graph_path, graph_similar
from sldb.cli import main as cli_main

MODULE = "sldb_analysis_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Spec(StructuredNLDoc):
    __semantics__ = {"type": ["doc", "spec"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


class AnalysisWorld:
    """A store whose specs form a chain: 3 -> 2 -> 1, plus one spec nobody relates to."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        api.add_model(self.store, f"{MODULE}:Spec", self.py)
        api.init_relations(self.store, self.py)
        self._populate()

    def _populate(self) -> None:
        for name in ("s1", "s2", "s3", "lonely"):
            self.create("Spec", name, {"title": name.upper()})
        self.relation_type("refines")
        self.relation("s2-s1", "Spec:s2", "Spec:s1")
        self.relation("s3-s2", "Spec:s3", "Spec:s2")

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str) -> None:
        self.create("RelationTypeDoc", f"rt-{name}", {"title": name, "name": name, "direction": "directed", "cardinality": "many_to_many", "axis": "WHY", "source_types": ["Spec"], "target_types": ["Spec"], "condition": "", "description": f"{name}."})

    def relation(self, name: str, src: str, tgt: str) -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": "refines", "condition": "", "notes": ""})


@pytest.fixture
def world(tmp_path: Path) -> AnalysisWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    return AnalysisWorld(tmp_path)


S1, S2, S3 = (f"sldb://document/Spec:{n}" for n in ("s1", "s2", "s3"))


def test_the_authored_relation_is_what_gets_walked_not_the_structural_spine(world: AnalysisWorld):
    """Without this, every pair of specs is two hops apart through their model node."""
    assert graph_path(world.store, S3, S1) == [S3, S2, S1]
    assert graph_path(world.store, S3, S1, relations=["has_document"]) == [S3, "sldb://model/Spec", S1]


def test_order_and_cycles_over_what_the_store_asserts(world: AnalysisWorld):
    assert graph_cycles(world.store) == []
    order = graph_order(world.store)
    assert order.index(S1) < order.index(S2) < order.index(S3)


def test_a_document_nobody_relates_to_shows_up_as_isolated(world: AnalysisWorld):
    """Restricted to one class: unrestricted, every field and section node is isolated too."""
    assert graph_isolated(world.store, node_types=["Spec"]) == ["sldb://document/Spec:lonely"]
    assert graph_components(world.store, node_types=["Spec"])[0] == [S1, S2, S3]
    assert "sldb://field/RelationDoc.condition" in graph_isolated(world.store)


def test_centrality_and_resemblance_over_a_real_store(world: AnalysisWorld):
    assert graph_central(world.store, kind="in_degree", limit=1) == [(S1, 1.0)]
    resembling = dict(graph_similar(world.store, S1, node_types=["Spec"]))
    assert resembling == {S2: 3, S3: 3, "sldb://document/Spec:lonely": 3}


def test_the_cli_prints_each_analysis(world: AnalysisWorld, capsys):
    for argv in (["graph", "cycles"], ["graph", "order"], ["graph", "components"], ["graph", "central", "--kind", "degree"], ["graph", "similar", S1], ["graph", "path", S3, S1]):
        assert cli_main([*argv, "--store", str(world.store)]) == 0
    assert S1 in capsys.readouterr().out


def test_the_cli_says_so_when_there_is_no_path_and_exits_nonzero(world: AnalysisWorld, capsys):
    assert cli_main(["graph", "path", S1, "sldb://document/Spec:lonely", "--store", str(world.store)]) == 1
    assert "No path" in capsys.readouterr().out

FILE:instruccion
Cold-bundle de la tarea task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_backend.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

