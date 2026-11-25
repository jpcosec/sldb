FILE:desk/tasks/task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co.md
---
sldb:
  by: agent
  at: '2026-11-16T16:29:43Z'
  authority: generated
  via: create_document
id: task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-101851-suggestion-sldb-serve-list-views-compone-el-ndice-federado-de-toda-la-m-quina-en-fr-o-y-sin-lock-2-5-gb-por-proceso.md
depends_on: []
pills: []
files:
- src/sldb/api/views/list_views.py
- src/sldb/store/edge_index/compose.py
- tests/api/test_views_linked.py
- tests/store/test_shard_cache_copies.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
---

# sldb serve: list_views deja de componer el índice federado de toda la máquina y compose_edge_index compone una sola vez por clave aunque lleguen peticiones concurrentes

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui midió en robocop2 (2026-11-16) que el sldb serve que levanta su test se va a 2-5 GB por proceso: seis hilos de petición estaban en list_views -> load_edge_index(include_linked=True) -> compose_edge_index -> read_or_compose -> ... -> load_edges_shard con model_copy(deep=True); componer una vez federa 7 stores, 15.617 shards, 178.756 aristas, 35,5 s y 1,2 GB. list_views (src/sldb/api/views/list_views.py:24) pide la federación entera solo para listar nodos ViewDoc; compose_edge_index (src/sldb/store/edge_index/compose.py) guarda en un dict de módulo _COMPOSED sin lock, así que dos llamadas en frío componen dos veces a la vez. Bloquea los tests de graph_ui. Origen: desk/inbox/20261116-101851-suggestion-sldb-serve-list-views-compone-el-ndice-federado-de-toda-la-m-quina-en-fr-o-y-sin-lock-2-5-gb-por-proceso.md (evidencia en UIs/graph_ui/runs/subagents/20261116-sldb-serve-rss/ del workspace SLDB_1).

## Goal

_Describe the concrete result this task must produce._

list_views devuelve las mismas vistas que hoy (locales y de stores enlazados, H9) sin llamar a compose_edge_index, y N llamadas concurrentes en frío a compose_edge_index con la misma clave componen una sola vez; el caso mínimo de graph_ui ya no pasa de 1 GB.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) Un módulo nuevo view_nodes.py en el paquete sldb.api.views con una función que, para cada (ruta, nombre) de federated_stores(store_path, True) (src/sldb/store/edge_index/federation.py), lee solo los shards de aristas del modelo ViewDoc con compose_edges_documents(ruta, "ViewDoc", copy=False) (src/sldb/store/io/shard_compose.py), califica los nodos con qualify(part, nombre) como hace la composición, estampa facets.source.store_path y se queda con los nodos de node_type "ViewDoc"; list_views (src/sldb/api/views/list_views.py) la usa en lugar de load_edge_index. Se mantiene la federación transitiva que hay hoy. (2) Un módulo nuevo compose_lock.py en el paquete sldb.store.edge_index con un single-flight por clave: un threading.Lock de módulo que guarda un dict clave -> Lock; compose_edge_index toma el lock de su clave en la rama de fallo de caché y vuelve a mirar _COMPOSED adentro antes de componer. (3) Tests: en tests/api/test_views_linked.py, list_views con compose_edge_index parcheado para lanzar sigue listando la vista local y la enlazada; en tests/store/test_shard_cache_copies.py, 8 hilos que llaman a la vez compose_edge_index en frío sobre la misma clave cuentan una sola composición (monkeypatch del compositor interno con un contador). CHANGELOG.md. Al cerrar, aviso a graph_ui con deskops message send --to graph_ui. No entra: leer sin copia en read_store_contributions para todas las lecturas del índice (cambio global de semántica de copias; otra tarea si hace falta), limitar hilos en sldb serve, timeouts del cliente.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer list_views.py, view_reading.py (run_view ya empieza local y amplía con widen), compose.py, composed_reading.py, federation.py, shard_compose.py y src/sldb/store/io/shards.py (camino copy=False). 2) Escribir view_nodes.py y cambiar list_views. 3) Escribir compose_lock.py y usarlo en compose_edge_index. 4) Tests. 5) Medir el caso mínimo de graph_ui (comando en el README de su evidencia) con /usr/bin/time -v y anotar el RSS máximo en result-summary.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views_linked.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_shard_cache_copies.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_run_view_reads.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los dos tests nuevos; result-summary.md tiene el RSS máximo del caso mínimo de graph_ui antes y después (después < 1 GB); CHANGELOG y commit; aviso a graph_ui.

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

FILE:desk/atoms/atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta.md
---
id: atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
title: Una vista es un documento que declara qué leer y sldb la ejecuta
five_wh_one_plus: what
tags:
- system:sldb
- topic:views
provenance: docs/architecture/views.md
---

# Una vista es un documento que declara qué leer y sldb la ejecuta

## Answer

Una vista de sldb es un ViewDoc (el de SV01) con params y sections, sin código: cada sección declara select (un selector de GD23, con sustitución {param}), fields, edges (vecinos por relación y dirección), group_by y group_order, rules (RuleDocs de GO06 cuyos findings se agregan a cada fila) y transitions (aristas que se cumplen y bloqueadas, de GO08/GO09). sldb.api.run_view(store, name, params) devuelve las secciones con una revision (sha256 de lo leído) y sldb serve la expone en GET /views/<name> con ETag y 304. Un hecho que sldb no calcula entra como documento que la vista lee, nunca como proveedor computed en Python (DA1). El nombre projection queda reservado para las rutas de SV02. Implementado en GD25 (plan generalizar-desde-deskops).

FILE:src/sldb/api/views/list_views.py
"""The composed views a store holds (GD25, q11), and the loading of one ViewDoc by name.

A ViewDoc is read from its own file through its model (the index's projection keeps no
nested `sections`); the `ViewDoc` nodes of the composed index (the store's and its linked
stores', H9) say which exist, `view_source` which one a name means and where its file is."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.open_store import open_store
from sldb.api.views.view_source import VIEW_MODEL, bare_name, qualified_name, read_view_node, readable_view_node, view_node
from sldb.core.exceptions import SLDBValidationError
from sldb.models.notation.view_doc import ViewDoc


def list_views(store: str | Path | None) -> list[dict[str, Any]]:
    """`[{name, title, params, sections: [key...]}]` of the ViewDocs with sections, local and
    linked, by name; a linked view whose name another view also has is listed `<link>:<name>`.
    The projection views (no sections) are listed by `list_projection_views` (SV02)."""
    index = load_edge_index(open_store(store, mode="readonly").store_path, include_linked=True)
    nodes = index.nodes_of_type(VIEW_MODEL)
    clashes = Counter(n.semantics["export_id"] for n in nodes)
    named = [(listed_name(n, clashes), view) for n in nodes if (view := readable_view_node(n)) is not None]  # a refused path is warned, not listed
    return [summary(name, view) for name, view in sorted(named, key=lambda nv: nv[0]) if view.sections]


def listed_name(node: Any, clashes: Counter) -> str:
    """The view's bare name, or `<link>:<name>` for a linked view sharing its name."""
    return qualified_name(node) if clashes[node.semantics["export_id"]] > 1 else bare_name(node)


def summary(name: str, view: ViewDoc) -> dict[str, Any]:
    return {"name": name, "title": view.title, "params": [p.model_dump() for p in view.params], "sections": [s.key for s in view.sections]}


def load_view(name: str, index: Any) -> tuple[ViewDoc, Any]:
    """The composed ViewDoc `name` and its index node (`view_source.view_node`); unknown or
    ambiguous is `SLDBDocumentTargetError`, a projection view (no sections) is
    `SLDBValidationError`, both naming it."""
    node = view_node(index, name)
    view = read_view_node(node)
    if not view.sections:
        raise SLDBValidationError(f"view {name!r} is a projection view (it has no sections); use /views/projection")
    return view, node

FILE:src/sldb/store/edge_index/compose.py
"""Shards -> one EdgeIndex: every store's contributions merged (the same node id is one node,
the first contributor's), the cross-document rules applied. Composed once per state of the
shards: the result is kept while no shard file, and no store index, has moved."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.store.edge_index.composed_reading import read_or_compose, with_live_stale
from sldb.store.edge_index.composition_targets import resolve_composition_edges
from sldb.store.edge_index.doc_anchor_states import with_anchor_states
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.federation import federated_stores, qualify
from sldb.store.edge_index.live_stale import ModelTypeOf
from sldb.store.edge_index.resolve import resolve_edges_reporting
from sldb.store.edge_index.shard_reading import read_store_contributions
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.io import load_store_index
from sldb.store.models import EdgeContribution, EdgeNodeRecord, EdgeRecord, ModelEdges

_COMPOSED: dict[tuple, tuple[tuple, EdgeIndex, list]] = {}


def compose_edge_index(store_path: Path, include_linked: bool = True, exclude_tags: Iterable[str] = (), model_type_of: ModelTypeOf | None = None) -> EdgeIndex:
    """The store's edge index, read from its shards (never rebuilt here).

    Args:
        store_path: The store's `.sldb` directory.
        include_linked: Also read the linked stores' indexes, their ids qualified by name.
        exclude_tags: Documents carrying one of these tags are left out (their nodes, their
            sections, their edges); the index itself holds everything.
        model_type_of: Loads a model class (`(model_ref, project_root) -> class | None`), so
            `stale` also names documents built under another contract of their model, and a
            document node's payload gains `<field>__anchor_state` for each of its model's
            `__doc_anchors__` (GO07: on copies, never in a shard; without it, none).

    Returns:
        The composed index; shared between callers, so treat it as read-only. Its `stale` is
        checked on every call against the files on disk (`live_stale`), not only the shards.
    """
    stores = federated_stores(Path(store_path), include_linked)
    key = (str(stores[0][0]), include_linked, frozenset(exclude_tags), model_type_of)
    signature = tuple(shards_signature(path) for path, _ in stores)
    hit = _COMPOSED.get(key)
    if hit is None or hit[0] != signature:
        hit = _COMPOSED[key] = (signature, *read_or_compose(stores, include_linked, frozenset(exclude_tags), model_type_of, _compose))
    return with_live_stale(hit[1], stores, hit[2], model_type_of)


def invalidate_composed_edge_indexes() -> None:
    """Forget every composed index (tests, or a caller that rewrote shards by hand)."""
    _COMPOSED.clear()


def _compose(stores: list[tuple[Path, str | None]], exclude_tags: frozenset[str], model_type_of: ModelTypeOf | None) -> EdgeIndex:
    nodes: dict[str, EdgeNodeRecord] = {}
    edges: list[EdgeRecord] = []
    stale: list[str] = []
    fields: dict[str, list[str]] = {}
    for path, name in stores:
        stale += _merge_store(path, name, exclude_tags, nodes, edges, fields)
    nodes = with_anchor_states(nodes, [path for path, _ in stores], model_type_of, fields)
    kept, problems, unresolved = resolve_edges_reporting(nodes, resolve_composition_edges(nodes, edges))
    return EdgeIndex(nodes=nodes, edges=kept, problems=problems, stale=stale, unresolved_references=unresolved, payload_fields=fields)


def _merge_store(path: Path, name: str | None, exclude_tags: frozenset[str], nodes: dict, edges: list[EdgeRecord], fields: dict[str, list[str]]) -> list[str]:
    parts, stale_here = read_store_contributions(path, exclude_tags)
    for part in parts:
        if isinstance(part, ModelEdges):
            fields.setdefault(part.model_name, part.projected_fields)
    _merge((qualify(p, name) for p in parts), nodes, edges, _source(path))
    return [f"{name}:{export_id}" if name else export_id for export_id in stale_here]


def _merge(parts: Iterable[EdgeContribution], nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], source: dict) -> None:
    for part in parts:
        edges += part.edges
        for node in part.nodes:
            nodes.setdefault(node.id, _stamped(node, source))


def _stamped(node: EdgeNodeRecord, source: dict) -> EdgeNodeRecord:
    return node.model_copy(update={"facets": {**node.facets, "source": source}})


def _source(store_path: Path) -> dict:
    return {"generated_from": "sldb.store.edge_index", "store_path": str(store_path), "hash_a": load_store_index(store_path).hash_a}

FILE:tests/api/test_views_linked.py
"""H9: a ViewDoc tracked by a linked store (DA4: deskops' views ship only in its package store).

Store A links to B; the view `board` lives only in B. `run_view(A, "board")` finds it, reads
its file from B's root (through the read guard) and evaluates it over A's documents."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.core.exceptions import SLDBDocumentTargetError

MODULE = "sldb_h9_linked_view_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


def board(key: str, title: str = "Board") -> dict:
    return {"id": "board", "name": "board", "title": title, "sections": [{"key": key, "select": {"model": "Note"}, "fields": ["title"]}]}


class Store:
    def __init__(self, base: Path, name: str, py: str) -> None:
        self.root, self.py = base / name, py
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for ref in (f"{MODULE}:Note", "sldb.models.notation_models:ViewDoc"):
            api.add_model(self.store, ref, py)

    def doc(self, model: str, name: str, payload: dict) -> Path:
        path = self.root / model.lower() / f"{name}.md"
        api.create_document(self.store, model, path, payload, name, self.py)
        return path

    def link(self, other: "Store", name: str) -> None:
        api.link_store(self.store, other.store, name=name)


@pytest.fixture
def stores(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        a, b = Store(tmp_path, "A", str(tmp_path)), Store(tmp_path, "B", str(tmp_path))
        a.doc("Note", "a1", {"title": "from A"})
        b.doc("Note", "b1", {"title": "from B"})
        b.doc("ViewDoc", "board", board("notes"))
        a.link(b, "B")
        yield a, b
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_view_only_in_the_linked_store_is_found_and_evaluated_over_the_calling_store(stores) -> None:
    a, _ = stores
    (a.root / "viewdoc").mkdir()
    (a.root / "viewdoc" / "board.md").write_text("# not the view: B's root is read, not A's\n", encoding="utf-8")
    result = api.run_view(a.store, "board")
    assert result["view"] == "board"
    assert [(r["export_id"], r["fields"]) for r in result["sections"]["notes"]["rows"]] == [("Note:a1", {"title": "from A"})]
    assert api.run_view(a.store, "B:board")["revision"] == result["revision"]


def test_list_views_lists_the_linked_view(stores) -> None:
    a, _ = stores
    assert api.list_views(a.store) == [{"name": "board", "title": "Board", "params": [], "sections": ["notes"]}]


def test_two_linked_views_with_one_name_are_ambiguous_and_listed_qualified(stores, tmp_path: Path) -> None:
    a, _ = stores
    c = Store(tmp_path, "C", str(tmp_path))
    c.doc("ViewDoc", "board", board("other"))
    a.link(c, "C")
    with pytest.raises(SLDBDocumentTargetError) as caught:
        api.run_view(a.store, "board")
    assert str(caught.value) == "Ambiguous view: board (linked in B, C)"
    assert [v["name"] for v in api.list_views(a.store)] == ["B:board", "C:board"]
    assert list(api.run_view(a.store, "C:board")["sections"]) == ["other"]


def test_a_local_view_wins_over_a_linked_one(stores) -> None:
    a, _ = stores
    a.doc("ViewDoc", "board", board("mine", "Mine"))
    assert list(api.run_view(a.store, "board")["sections"]) == ["mine"]
    assert list(api.run_view(a.store, "B:board")["sections"]) == ["notes"]
    assert [(v["name"], v["title"]) for v in api.list_views(a.store)] == [("B:board", "Board"), ("board", "Mine")]


def test_the_revision_moves_when_the_linked_view_changes(stores) -> None:
    a, b = stores
    before = api.run_view(a.store, "board")["revision"]
    api.save_document_payload(b.store, "ViewDoc", "board", board("notes", "Board v2"), b.py)
    assert api.run_view(a.store, "board")["revision"] != before


def test_a_linked_view_file_swapped_for_a_symlink_out_of_its_root_is_not_read(stores, tmp_path: Path) -> None:
    a, b = stores
    path = b.root / "viewdoc" / "board.md"
    outside = tmp_path / "outside.md"
    outside.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(outside)
    with pytest.raises(SLDBDocumentTargetError, match="outside-root"):
        api.run_view(a.store, "board")

FILE:tests/store/test_shard_cache_copies.py
"""A loaded shard is the caller's own copy: editing it and saving it back writes the edit.

The cache used to hand out its own instance, so a caller that edited what it loaded was
compared against its own edit and the save was skipped. `fields update` did exactly that: the
Markdown and the roster moved, the document's record did not, and `stores check` failed on the
write sldb itself had just made.
"""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as sldb_main
from sldb.store.io.shards import load_document_shard, save_document_shard
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.io.utils import yaml_load

MODEL_SRC = (
    "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
    "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
    "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
)


def test_an_edited_shard_is_written(tmp_path: Path):
    path = tmp_path / "note.yaml"
    save_document_shard(path, DocumentEntry(name="note", path="note.md", source_hash="old"))
    entry = load_document_shard(path)
    entry.source_hash = "new"
    save_document_shard(path, entry)
    assert yaml_load(path.read_text(encoding="utf-8"))["source_hash"] == "new"
    assert load_document_shard(path).source_hash == "new"


def test_editing_a_loaded_shard_does_not_touch_the_cache(tmp_path: Path):
    path = tmp_path / "note.yaml"
    save_document_shard(path, DocumentEntry(name="note", path="note.md", source_hash="old"))
    load_document_shard(path).source_hash = "edited, never saved"
    assert load_document_shard(path).source_hash == "old"


def test_fields_update_leaves_the_store_passing(tmp_path: Path):
    (tmp_path / "shardcopy_models.py").write_text(MODEL_SRC)
    (tmp_path / "note.md").write_text("# hello\n\nold body\n")
    sp, pp = str(tmp_path / ".sldb"), str(tmp_path)
    assert sldb_main(["stores", "init", "--path", pp]) == 0
    assert sldb_main(["models", "add", "shardcopy_models:NoteDoc", "--store", sp, "--pythonpath", pp]) == 0
    assert sldb_main(["docs", "track", str(tmp_path / "note.md"), "--model", "NoteDoc", "--store", sp, "--pythonpath", pp]) == 0
    assert sldb_main(["fields", "update", "docs/NoteDoc/note/body", '"new body"', "--store", sp, "--pythonpath", pp]) == 0
    assert "new body" in (tmp_path / "note.md").read_text()
    assert sldb_main(["stores", "check", "--store", sp, "--pythonpath", pp, "--quiet"]) == 0

FILE:instruccion
Cold-bundle de la tarea task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views_linked.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_shard_cache_copies.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_run_view_reads.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

