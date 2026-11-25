FILE:desk/tasks/task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update.md
---
sldb:
  by: agent
  at: '2026-11-16T07:45:47Z'
  authority: generated
  via: save_document_payload
id: task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-edgeindex-stale-go04-d7eefdeb-manda-a-reconstruir-pero-rebuild-edges-no-resuelve-una-edición-externa.md
depends_on: []
pills:
- desk/contexts/pill-pill-texto-de-la-alerta-y-test-existente-de-stale.md
files:
- src/sldb/store/edge_index/edge_index.py
- src/sldb/api/edges/edge_reading.py
- src/sldb/cli/commands/edges.py
- tests/api/test_api_edges.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# EdgeIndex.stale manda a la operación correcta: una edición externa se resuelve con sldb stores update, no con edges rebuild

## Rationale

_Explain why this task exists or the business driver behind it._

Desde GO04 (d7eefdeb) live_stale compara cada archivo trackeado con el source_hash de su shard: una edición externa deja el documento en EdgeIndex.stale. Pero los textos que acompañan a stale mandan a reconstruir: la descripción del campo (src/sldb/store/edge_index/edge_index.py:19, "run the rebuild"), la docstring de load_edge_index (src/sldb/api/edges/edge_reading.py:17-18, "rebuild_edges brings them current") y la alerta edges/stale de la CLI (src/sldb/cli/commands/edges.py:73, fix "sldb edges rebuild"). rebuild_edges compara con el hash registrado del store y da docs_written=0, así que stale queda para siempre y graph_ui bloquea el grafo. La docstring de rebuild_edges (src/sldb/api/edges/rebuild_edges.py:21-23) ya dice que la edición externa se resuelve con update_store_indexes. Origen: desk/inbox/inbox-note-edgeindex-stale-go04-d7eefdeb-manda-a-reconstruir-pero-rebuild-edges-no-resuelve-una-edición-externa.md.

## Goal

_Describe the concrete result this task must produce._

Los tres textos nombran `sldb stores update` (API update_store_indexes) como la operación que resuelve un documento stale por edición externa, y un test prueba que después de stores update el documento editado sale de stale.

## Scope

_State what is in scope and what is out of scope._

Entra: cambiar la descripción del campo stale en edge_index.py, la docstring de load_edge_index en edge_reading.py y la alerta de _report_findings en src/sldb/cli/commands/edges.py (what: "tracked file changed since its shard was built", fix: "sldb stores update"). Test nuevo en tests/api/test_api_edges.py: editar a mano un documento de un store de prueba -> aparece en load_edge_index(...).stale -> rebuild_edges no lo saca -> update_store_indexes sí. Si el test muestra que update_store_indexes tampoco lo saca, la tarea se detiene y el ejecutor reporta el caso (no se cambia rebuild_edges en esta tarea). CHANGELOG.md. No entra: que rebuild_edges rehashee archivos, ni stale por documento en graph_ui.

Precisiones (preflight-1): textos exactos. Descripción del campo stale: "Export ids of tracked documents whose shard is missing, built from another hash_c or EDGE_INDEX_VERSION, from a file since edited outside sldb, or under another contract_signature of the model: `sldb stores update` (update_store_indexes) brings them current; `sldb edges rebuild` only rebuilds shards from the hashes the store already recorded." Docstring de load_edge_index: reemplazar "`rebuild_edges` brings them current" por "`update_store_indexes` (`sldb stores update`) brings them current". Alerta: alert("edges/stale", s, "tracked file changed since its shard was built", "sldb stores update"). Del grep solo se cambian los mensajes cuyo texto habla de stale o de documentos editados fuera de sldb; los que hablan de reconstruir el índice por versión o por shards faltantes quedan. tests/api/test_composition_edges.py se corre como regresión y no se modifica. El store de prueba se arma como en los tests existentes de tests/api/test_api_edges.py.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer los cuatro archivos citados. 2) Escribir primero el test. 3) Cambiar los textos. 4) grep -rn "edges rebuild" src/sldb docs/ para encontrar otros mensajes que manden a reconstruir por stale y alinearlos.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/api/test_composition_edges.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (stale -> stores update -> no stale); los mensajes ya no dicen rebuild para stale; CHANGELOG y commit; aviso a graph_ui con deskops message send --to graph_ui.

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

FILE:desk/contexts/pill-pill-texto-de-la-alerta-y-test-existente-de-stale.md
---
sldb:
  by: agent
  at: '2026-11-16T07:45:27Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-texto-de-la-alerta-y-test-existente-de-stale
status: active
summary: texto de la alerta y test existente de stale
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: texto de la alerta y test existente de stale

## What

_Define the context or guardrail this pill carries._

Las respuestas del bundle-1 de la tarea: precisiones de implementación que la revisión en frío pidió y que el contrato deja abiertas.

## Why

_Explain why this context matters for safe execution._

La revisión cold-bundle (bundle-1) mostró que sin estas precisiones el ejecutor tendría que inventar estos detalles.

## When

_Describe when an agent should apply this pill._

Al ejecutar la tarea, antes de tocar código.

## Where

_Name the files, surfaces, or scope this pill applies to._

src/sldb/cli/commands/edges.py, tests/api/test_api_edges.py

## How

_Describe the correct way to apply this guidance._

El texto de la alerta cubre todas las causas de stale: 'shard out of date (missing, built by another version, or the file changed outside sldb)', con fix 'sldb stores update'. El test se hace extendiendo el que ya existe (test_a_hand_edit_reaches_the_index_through_stores_update): antes de stores update se afirma que el documento está en stale y que rebuild_edges no lo saca. Del grep solo se cambian los textos que mandan a 'edges rebuild' para resolver stale.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.

FILE:src/sldb/store/edge_index/edge_index.py
"""The composed edge index: every node and edge of a store (and its linked stores), in memory."""

from __future__ import annotations

from pydantic import BaseModel, Field, PrivateAttr

from sldb.store.edge_index.node_ids import as_node_id
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.store.models import EdgeNodeRecord, EdgeRecord


class EdgeIndex(BaseModel):
    """What the shards say, composed: the one door for reading edges. Ids are node ids
    (`sldb://document/Model:name`...); a bare export id `Model:name` is read as its document's."""

    nodes: dict[str, EdgeNodeRecord] = Field(default_factory=dict, description="Every node by id; the same id contributed twice is one node.")
    edges: list[EdgeRecord] = Field(default_factory=list, description="Every edge, cross-document rules applied (inherited conditions, reverse edges, edges to nothing dropped).")
    problems: list[str] = Field(default_factory=list, description="Authored edges left out because an endpoint is not a node; reported, never stored.")
    stale: list[str] = Field(default_factory=list, description="Export ids of tracked documents whose shard is missing, built from another hash_c or EDGE_INDEX_VERSION, from a file since edited outside sldb, or under another contract_signature of the model: run the rebuild.")
    payload_fields: dict[str, list[str]] = Field(default_factory=dict, description="Per model, the fields a `payload` facet filter may name (`ModelEdges.projected_fields`); a filter naming none of them is rejected.")
    unresolved_references: list[UnresolvedReference] = Field(default_factory=list, description="Declared reference and containment values that name no document; inspected, never stored as edges.")
    _out: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)
    _in: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)

    def edges_from(self, node_id: str, relation: str | None = None) -> list[EdgeRecord]:
        """Edges leaving `node_id`, of one relation or of all."""
        self._ensure_maps()
        return [e for e in (self._out or {}).get(as_node_id(node_id), []) if relation in (None, e.relation)]

    def edges_to(self, node_id: str, relation: str | None = None) -> list[EdgeRecord]:
        """Edges pointing at `node_id`, of one relation or of all."""
        self._ensure_maps()
        return [e for e in (self._in or {}).get(as_node_id(node_id), []) if relation in (None, e.relation)]

    def node(self, node_id: str) -> EdgeNodeRecord | None:
        """The node with that id (or that export id), None when the index has none."""
        return self.nodes.get(as_node_id(node_id))

    def nodes_of_type(self, node_type: str) -> list[EdgeNodeRecord]:
        """Nodes of one class, sorted by id; a document's class is its model's name."""
        return sorted((n for n in self.nodes.values() if n.node_type == node_type), key=lambda n: n.id)

    def _ensure_maps(self) -> None:
        if self._out is not None:
            return
        self._out, self._in = {}, {}
        for e in self.edges:
            self._out.setdefault(e.source, []).append(e)
            self._in.setdefault(e.target, []).append(e)

FILE:src/sldb/api/edges/edge_reading.py
"""Read the edge index of a store: the one door to edges and nodes."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.compose import compose_edge_index
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.models import EdgeNodeRecord, EdgeRecord


def load_edge_index(store: str | Path | None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> EdgeIndex:
    """The store's edge index composed from its shards (and its linked stores').

    Reading never rebuilds: every sldb write keeps the shards current. `EdgeIndex.stale` names
    the documents a write from outside sldb left behind; `rebuild_edges` brings them current.

    Args:
        store: The store (path, alias, or None to discover it).
        include_linked: Also read the linked stores, their document ids qualified `store:Model:name`.
        exclude_tags: Leave out the documents carrying one of these tags (the index holds them all).

    Returns:
        The composed index; kept and shared while the shards do not move, so read-only.
    """
    return compose_edge_index(open_store(store, mode="readonly").store_path, include_linked, exclude_tags, model_type_of)


def model_type_of(model_ref: str, root: Path) -> Any | None:
    """A store's model class for the stale check: imported as the rebuild imports it (the
    working directory, then the store's own root); None when it cannot be loaded."""
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.core.exceptions import SLDBModelError

    for candidate in (None, str(root)):
        try:
            return resolve_model_ref(model_ref, candidate)
        except SLDBModelError:
            continue
    return None


def edges_from(store: str | Path | None, export_id: str, relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeRecord]:
    """Edges leaving a document (`Model:name`) or any node (`sldb://<kind>/...`).

    Args:
        store: The store (path, alias, or None to discover it).
        export_id: A document's export id, or a full node id.
        relation: Only edges of this relation type; None for all.
        include_linked: As in `load_edge_index`.
        exclude_tags: As in `load_edge_index`.

    Returns:
        `{source, target, relation, metadata}` records, in a stable order.
    """
    return load_edge_index(store, include_linked, exclude_tags).edges_from(export_id, relation)


def edges_to(store: str | Path | None, export_id: str, relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeRecord]:
    """Edges pointing at a document or node; arguments and result as in `edges_from`."""
    return load_edge_index(store, include_linked, exclude_tags).edges_to(export_id, relation)


def edge_node(store: str | Path | None, node_id: str, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> EdgeNodeRecord | None:
    """The node with that node id (or document export id); None when the index has none."""
    return load_edge_index(store, include_linked, exclude_tags).node(node_id)


def edge_nodes_of_type(store: str | Path | None, node_type: str, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeNodeRecord]:
    """Nodes of one class (`sldb_model`, `semantic_tag`, `relation_type`, a model name...), by id."""
    return load_edge_index(store, include_linked, exclude_tags).nodes_of_type(node_type)

FILE:src/sldb/cli/commands/edges.py
"""`sldb edges` handlers: thin printing wrappers over `sldb.api`'s edge index functions."""

from __future__ import annotations

import json
from typing import Any

from sldb.cli.commands.edges_rewrite import edges_referrers, edges_rewrite
from sldb.cli.commands.edges_unknown_node import unknown_node_message
from sldb.api import check_edges, edges_from, edges_holding, edges_to, init_relations, open_store, rebuild_edges, runtime_document, unresolved_references


class EdgesCLI:
    """Noun-first surface of the edge index."""

    def run(self, args: Any) -> int:
        """Dispatch `edges init|rebuild|show|check|unresolved|referrers|rewrite`; 0 on success, 1 when a check fails."""
        handler = {"init": self._init, "rebuild": self._rebuild, "show": self._show, "check": self._check, "unresolved": self._unresolved, "referrers": edges_referrers, "rewrite": edges_rewrite}[args.edges_command]
        return handler(args)

    def _init(self, args: Any) -> int:
        print(f"Initialized relations: {init_relations(args.store, args.pythonpath).summary()}")
        return 0

    def _rebuild(self, args: Any) -> int:
        report = rebuild_edges(args.store, args.pythonpath)
        print(f"Edges: {report.docs_written} shard(s) written, {report.docs_reused} reused, {report.models_walked} model(s) walked")
        return 0

    def _show(self, args: Any) -> int:
        if args.holds_for and args.to:
            raise SystemExit("--holds-for reads the edges leaving the node; it does not combine with --to")
        edges = self._edges(args)
        if not edges and (unknown := unknown_node_message(args)):
            raise SystemExit(unknown)
        edges = _with_evidence(args, edges) if args.evidence else edges
        print(json.dumps([e.model_dump() for e in edges], indent=2, ensure_ascii=False))
        return 0

    def _edges(self, args: Any) -> list:
        if args.holds_for:
            doc = runtime_document(open_store(args.store, mode="readonly").store_path, args.pythonpath, args.holds_for)
            return edges_holding(args.store, args.node, dict(doc.payload), args.relation, not args.local, args.exclude_tag, _export_id(doc))
        return (edges_to if args.to else edges_from)(args.store, args.node, args.relation, not args.local, args.exclude_tag)

    def _check(self, args: Any) -> int:
        """Exit 1 only on an error; a shard built from another `hash_c` is an alert."""
        report = check_edges(args.store, not args.local, args.exclude_tag)
        _report_findings(report)
        if report.linked_errors or report.linked_stale:
            print(f"note: linked stores: {len(report.linked_errors)} error(s), {len(report.linked_stale)} stale, theirs to fix (run `edges check` there, or this with --local to leave them out)")
        if report.untracked_builtins:
            print(f"note: builtin relation type(s) not tracked here, checked against sldb's own: {', '.join(report.untracked_builtins)} (`sldb edges init` tracks them)")
        print("Edges OK" if report.ok else f"{len(report.errors)} error(s), {len(report.stale)} stale")
        return 1 if report.errors else 0

    def _unresolved(self, args: Any) -> int:
        """A report, not a check: 0 whatever it finds."""
        found = unresolved_references(args.store, not args.local, args.exclude_tag)
        if args.format == "json":
            print(json.dumps([r.model_dump() for r in found], indent=2, ensure_ascii=False))
            return 0
        for r in found:
            print(f"{r.reason}: {r.source} .{r.field} -> {r.target}" + (f" ({r.target_export_id})" if r.target_export_id else ""))
        print(f"{len(found)} unresolved reference(s)")
        return 0


def _report_findings(report: Any) -> None:
    from sldb.cli import alert_sink
    from sldb.core.finding import alert, error

    stale = [alert("edges/stale", s, "the shard was built from another hash_c of the document", "sldb edges rebuild") for s in report.stale]
    alert_sink.report([error("edges/invalid", "edges", e) for e in report.errors] + stale)


def _export_id(doc: Any) -> str:
    """`Model:name` of a runtime document (`store:Model:name` behind a link): its `on_transition` rules run (GO08)."""
    prefix = "" if doc.store_name in ("local", "", None) else f"{doc.store_name}:"
    return f"{prefix}{doc.model_name}:{doc.name}"


def _with_evidence(args: Any, edges: list) -> list:
    from sldb.api.edges.edge_evidence import stamp_evidence

    return stamp_evidence(args.store, edges, not args.local)

FILE:tests/api/test_api_edges.py
"""`sldb.api` edge index: per-document shards on the hash chain, read through one door.

Covers: every write keeps its own shard current and touches no other document's; an untracked
document loses its shard; relation types, relations and anchors become nodes and edges, not
document nodes; cross-document rules (inherited condition and axis, reverse edges, orphans)
apply on read and are reported, not stored; `exclude_tags` is the reader's; a linked store's
documents come back qualified by the link's name; `init_relations` is idempotent.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.store.layout import edges_model_shard_path, edges_shard_path, edges_store_shard_path

MODULE = "sldb_edges_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Table(StructuredNLDoc):
    __semantics__ = {"type": ["restaurant", "table"]}
    __template__ = "# ⸢rev•title⸥\\n\\nCapacity: ⸢rev•capacity⸥\\n\\n## Notes\\n\\n⸢rev,markdown•notes⸥"
    title: str = Field(description="Title.")
    capacity: int = Field(description="Seats.")
    notes: str = Field(default="", description="Notes.")


class Booking(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nSize: ⸢rev•party_size⸥"
    title: str = Field(description="Title.")
    party_size: int = Field(description="People.")


class Move(StructuredNLDoc):
    __semantics__ = {"type": ["pron", "move"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Alias(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "anchor"]}
    __template__ = "# ⸢rev•symbol⸥\\n\\nRef: ⸢rev•ref⸥"
    symbol: str = Field(description="Word.")
    ref: str = Field(description="What it names.")
'''


class EdgeWorld:
    """A store prepared for relations, with the models above registered."""

    def __init__(self, base: Path, name: str = "world") -> None:
        self.root, self.py = base / name, str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Table", "Booking", "Move", "Alias"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str, source: list[str], target: list[str], **extra) -> None:
        payload = {"title": name, "name": name, "direction": "directed", "cardinality": "many_to_many", "axis": "WHERE", "source_types": source, "target_types": target, "condition": "", "description": f"{name}."}
        self.create("RelationTypeDoc", f"rt-{name}", {**payload, **extra})

    def relation(self, name: str, src: str, tgt: str, rtype: str, condition: str = "", **extra) -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": rtype, "condition": condition, "notes": "", **extra})


@pytest.fixture
def world(tmp_path: Path) -> EdgeWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    w = EdgeWorld(tmp_path)
    w.create("Table", "t12", {"title": "Table 12", "capacity": 6, "notes": "By the window."})
    w.create("Table", "t14", {"title": "Table 14", "capacity": 8, "notes": ""})
    w.create("Booking", "b1", {"title": "Ana", "party_size": 6})
    w.relation_type("assigned_to", ["Booking"], ["Table"], cardinality="many_to_one", condition="capacity >= {party_size}")
    w.relation("b1-t12", "Booking:b1", "Table:t12", "assigned_to")
    return w


def _pairs(edges) -> list[tuple[str, str]]:
    return [(e.target, e.relation) for e in edges]


def test_a_write_leaves_a_shard_per_document_model_and_store(world: EdgeWorld):
    assert edges_shard_path(world.store, "Table", "t12").exists()
    assert edges_model_shard_path(world.store, "Table").exists()
    assert edges_store_shard_path(world.store).exists()
    assert api.load_edge_index(world.store).stale == []


def test_structural_edges_and_typed_nodes(world: EdgeWorld):
    assert ("sldb://document/Table:t12", "has_document") in _pairs(api.edges_from(world.store, "sldb://model/Table"))
    assert ("sldb://section/Table:t12#table-12/notes", "has_section") in _pairs(api.edges_from(world.store, "Table:t12"))
    assert ("sldb://semantic_tag/type.restaurant.table", "tagged_as") in _pairs(api.edges_from(world.store, "Table:t12", "tagged_as"))
    assert api.edge_node(world.store, "Table:t12").node_type == "Table"
    assert [n.id for n in api.edge_nodes_of_type(world.store, "Booking")] == ["sldb://document/Booking:b1"]
    field = api.edge_node(world.store, "sldb://field/Table.capacity")
    assert field.node_type == "sldb_field" and field.semantics["kind"] == "integer"
    assert [e.source for e in api.edges_to(world.store, "sldb://model/Table", "has_model")] == ["sldb://store"]


def test_a_relation_doc_is_an_edge_that_inherits_from_its_type(world: EdgeWorld):
    [edge] = api.edges_from(world.store, "Booking:b1", "assigned_to")
    assert (edge.source, edge.target) == ("sldb://document/Booking:b1", "sldb://document/Table:t12")
    assert edge.metadata == {"origin": "relation_doc", "relation_doc": "b1-t12", "condition": "capacity >= {party_size}", "axis": "WHERE"}
    assert api.edges_to(world.store, "Table:t12", "assigned_to") == [edge]
    assert api.edge_node(world.store, "RelationDoc:b1-t12") is None
    applies = api.edges_from(world.store, "sldb://relation_type/assigned_to")
    assert _pairs(applies) == [("sldb://model/Booking", "applies_to_source"), ("sldb://model/Table", "applies_to_target")]
    assert api.check_edges(world.store).ok


def test_editing_one_document_rewrites_only_its_shard(world: EdgeWorld):
    shards = {name: edges_shard_path(world.store, model, name) for model, name in (("Table", "t12"), ("Table", "t14"), ("Booking", "b1"), ("RelationDoc", "b1-t12"))}
    before = {name: path.stat().st_mtime_ns for name, path in shards.items()}
    old_hash = api.edge_node(world.store, "Table:t14").semantics["hash_c"]
    api.save_document_payload(world.store, "Table", "t14", {"title": "Table 14", "capacity": 10, "notes": ""}, world.py)
    after = {name: path.stat().st_mtime_ns for name, path in shards.items()}
    assert [name for name in shards if before[name] != after[name]] == ["t14"]
    assert api.edge_node(world.store, "Table:t14").semantics["hash_c"] not in ("", old_hash)
    assert api.load_edge_index(world.store).stale == []
    assert api.rebuild_edges(world.store, world.py).docs_written == 0


def test_untracking_a_document_drops_its_shard_and_reports_the_orphan(world: EdgeWorld):
    api.untrack_document(world.store, "t12", world.py)
    assert not edges_shard_path(world.store, "Table", "t12").exists()
    assert api.edge_node(world.store, "Table:t12") is None
    assert api.edges_from(world.store, "Booking:b1", "assigned_to") == []
    assert api.check_edges(world.store).errors == ["relation 'b1-t12': target 'Table:t12' is not a tracked document"]


def test_undirected_types_read_both_ways_and_bad_classes_are_reported(world: EdgeWorld):
    world.relation_type("near", ["Table"], ["Table"], direction="undirected")
    world.relation("t12-t14", "Table:t12", "Table:t14", "near")
    [back] = api.edges_from(world.store, "Table:t14", "near")
    assert back.target == "sldb://document/Table:t12" and back.metadata["reverse"] is True
    world.relation("b1-near", "Booking:b1", "Table:t14", "near")
    errors = api.check_edges(world.store).errors
    assert any("source class 'Booking' not in source_types ['Table']" in e for e in errors)


def test_exclude_tags_is_the_readers_choice(world: EdgeWorld):
    world.create("Move", "m1", {"title": "a move"})
    assert api.edge_node(world.store, "Move:m1") is not None
    hidden = api.load_edge_index(world.store, exclude_tags=["type.pron.move"])
    assert hidden.node("Move:m1") is None
    assert hidden.edges_from("sldb://model/Move", "has_document") == []
    assert hidden.node("sldb://semantic_tag/type.pron.move") is not None


def test_anchors_name_what_their_ref_points_at(world: EdgeWorld):
    world.create("Alias", "mesa", {"symbol": "mesa", "ref": "model:Table"})
    world.create("Alias", "cupo", {"symbol": "cupo", "ref": "(field Table capacity)"})
    assert _pairs(api.edges_from(world.store, "sldb://anchor/mesa")) == [("sldb://model/Table", "names")]
    assert _pairs(api.edges_from(world.store, "sldb://anchor/cupo")) == [("sldb://field/Table.capacity", "names")]
    assert api.edge_node(world.store, "Alias:mesa") is None


def test_linked_store_documents_come_back_qualified(world: EdgeWorld, tmp_path: Path):
    other = EdgeWorld(tmp_path, "other")
    other.create("Table", "t99", {"title": "Table 99", "capacity": 2, "notes": ""})
    api.link_store(world.store, other.store, "annex")
    world.relation("b1-t99", "Booking:b1", "annex:Table:t99", "assigned_to")
    index = api.load_edge_index(world.store)
    assert index.node("annex:Table:t99").semantics["store"] == "annex"
    assert "sldb://document/annex:Table:t99" in [e.target for e in index.edges_from("sldb://model/Table", "has_document")]
    assert [e.target for e in index.edges_from("Booking:b1", "assigned_to")] == ["sldb://document/Table:t12", "sldb://document/annex:Table:t99"]
    assert api.load_edge_index(world.store, include_linked=False).node("annex:Table:t99") is None


def test_init_relations_is_idempotent(world: EdgeWorld):
    report = api.init_relations(world.store, world.py)
    assert (report.models_added, report.types_written, report.predicates_added) == ([], [], [])
    assert (world.root / "sldb" / "relation_types" / "tagged_as.md").exists()
    assert "sldb://relation_type/has_document" in [n.id for n in api.edge_nodes_of_type(world.store, "relation_type")]


def test_cli_edges_uses_the_api(world: EdgeWorld, capsys):
    from sldb.cli import main as cli_main

    assert cli_main(["edges", "show", "Booking:b1", "--relation", "assigned_to", "--store", str(world.store)]) == 0
    assert '"target": "sldb://document/Table:t12"' in capsys.readouterr().out
    assert cli_main(["edges", "check", "--store", str(world.store)]) == 0
    assert cli_main(["edges", "rebuild", "--store", str(world.store), "--pythonpath", world.py]) == 0
    assert "0 shard(s) written" in capsys.readouterr().out
    world.relation("orphan", "Booking:b1", "Table:nowhere", "assigned_to")
    assert cli_main(["edges", "check", "--store", str(world.store)]) == 1
    assert cli_main(["help", "edges"]) == 0


def test_a_hand_edit_reaches_the_index_through_stores_update(world: EdgeWorld):
    others = {name: edges_shard_path(world.store, "Table", name).stat().st_mtime_ns for name in ("t14",)}
    old_hash = api.edge_node(world.store, "Table:t12").semantics["hash_c"]
    path = world.root / "t12.md"
    path.write_text(path.read_text(encoding="utf-8").replace("By the window.", "By the door."), encoding="utf-8")
    assert api.update_store_indexes(world.store, world.py).complete
    assert api.edge_node(world.store, "Table:t12").semantics["hash_c"] != old_hash
    assert edges_shard_path(world.store, "Table", "t14").stat().st_mtime_ns == others["t14"]
    assert api.load_edge_index(world.store).stale == []


def test_a_wiped_index_reads_as_stale_and_rebuild_brings_it_back(world: EdgeWorld):
    import shutil

    before = api.load_edge_index(world.store)
    shutil.rmtree(world.store.parent / ".sldb_cache" / "edges")
    wiped = api.load_edge_index(world.store)
    assert "Table:t12" in wiped.stale and wiped.node("Table:t12") is None
    assert api.rebuild_edges(world.store, world.py).docs_written == len(wiped.stale)
    rebuilt = api.load_edge_index(world.store)
    assert rebuilt.stale == [] and rebuilt.nodes == before.nodes and rebuilt.edges == before.edges
    edges_shard_path(world.store, "Table", "t14").unlink()  # one shard lost, its model's cache key intact
    assert api.load_edge_index(world.store).stale == ["Table:t14"]
    assert api.rebuild_edges(world.store, world.py).docs_written == 1
    assert api.load_edge_index(world.store).nodes == before.nodes


def test_a_relation_carries_free_attributes_to_its_edge(world: EdgeWorld):
    """spec2viz loses a class relation's multiplicities and roles, a transition's action."""
    world.create("Booking", "b2", {"title": "Luis", "party_size": 2})
    world.relation("b2-t14", "Booking:b2", "Table:t14", "assigned_to", attributes={"multiplicity": "1..*", "role": "guest"})
    edge = next(e for e in api.load_edge_index(world.store).edges_from("sldb://document/Booking:b2", "assigned_to"))
    assert edge.metadata["attributes"] == {"multiplicity": "1..*", "role": "guest"}
    plain = next(e for e in api.load_edge_index(world.store).edges_from("sldb://document/Booking:b1", "assigned_to"))
    assert "attributes" not in plain.metadata, "an edge without attributes keeps its shard"


def test_query_snapshot_runs_a_query_without_a_store(world: EdgeWorld, tmp_path: Path):
    from sldb.api import graph as graph_api

    output = tmp_path / "snap.json"
    graph_api.snapshot_save(world.store, output, include_linked=False)
    query = graph_api.StructuredQuery(scope=graph_api.GraphScope(node_id_prefix="sldb://document/Table:"))
    assert sorted(n.id for n in graph_api.query_snapshot(graph_api.snapshot_load(output), query)) == sorted(n.id for n in graph_api.execute_query(world.store, query, include_linked=False))
    assert graph_api.Edge and graph_api.SystemIdentity

FILE:instruccion
Cold-bundle de la tarea task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/api/test_composition_edges.py

