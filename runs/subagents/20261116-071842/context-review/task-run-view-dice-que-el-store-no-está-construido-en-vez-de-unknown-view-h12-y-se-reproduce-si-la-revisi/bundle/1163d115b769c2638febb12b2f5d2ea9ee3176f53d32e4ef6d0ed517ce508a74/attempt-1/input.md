FILE:desk/tasks/task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi.md
---
sldb:
  by: agent
  at: '2026-11-16T05:46:57Z'
  authority: generated
  via: save_document_payload
id: task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md
depends_on: []
pills: []
files:
- src/sldb/api/views/view_source.py
- src/sldb/api/views/view_revision.py
- tests/api/test_run_view_reads.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
---

# run_view dice que el store no está construido en vez de Unknown view (H12) y se reproduce si la revision depende de cachés del proceso (H13)

## Rationale

_Explain why this task exists or the business driver behind it._

CC34 de deskops dejó dos huecos de sldb.api.run_view: (H12) con .sldb_cache borrado, run_view responde "Unknown view: board" porque el índice sale vacío ("reading never rebuilds"), en vez de decir que hay que correr sldb stores build; el error sale de src/sldb/api/views/view_source.py:33. (H13) en el proceso que escribió el store, run_view da otra revision (src/sldb/api/views/view_revision.py:16, sha256 de source_hash, content_hash y shards_signature) para las mismas filas que un proceso nuevo o sldb serve; no está reproducido en sldb. H9 y H11 ya se resolvieron (04a0e94e, 47b75674) y H1-H8 van en una task.decision aparte. Origen: desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md.

## Goal

_Describe the concrete result this task must produce._

(H12) run_view sobre un store cuyo índice compuesto está vacío o sin construir lanza SLDBStoreError con "store index not built: run `sldb stores build`" en lugar de "Unknown view"; (H13) un test dice si la revision cambia entre el proceso que escribió y uno nuevo, y si cambia, la revision deja de depender de cachés en memoria.

## Scope

_State what is in scope and what is out of scope._

Entra: (H12) en view_source.py, antes de "Unknown view", distinguir índice vacío o sin shards (usar la misma señal que stores check usa para store/unbuilt, src/sldb/api/stores/store_surroundings.py) y lanzar el error de Goal; test en tests/api/test_run_view_reads.py que borra .sldb_cache y comprueba el mensaje. (H13) test en tests/api/test_run_view_reads.py que escribe un documento, corre run_view en el mismo proceso y en un subprocess nuevo (python -c con sldb.api.run_view) sobre el mismo store y compara revision; si difieren, encontrar qué entrada de view_revision.revision viene de una caché del proceso (source_hash del índice, content_hash o shards_signature) y leerla del disco; si no difieren, el test queda como guarda y el informe lo dice. CHANGELOG.md. No entra: H1-H8 (task.decision aparte), rendimiento de run_view (task-sldb-views-run-board-en-menos-de-1-s...).

Precisiones (preflight-1): la señal de "no construido" es la de store/unbuilt en src/sldb/api/stores/store_surroundings.py (líneas 18-28): reutilizar esa función o su condición, sin copiarla. Para H13, el diagnóstico es: calcular por separado las cuatro entradas del dict read de view_revision.revision en el proceso que escribió y en el subprocess, y la que difiera es la que viene de caché; se arregla leyéndola con la función de disco que ya existe para ese dato (load_document_shard para source_hash, el content_hash del índice en disco para los demás), sin cachés de módulo. El "informe" es result-summary.md del run del ejecutor.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer view_source.py, view_revision.py, store_surroundings.py y tests/api/test_run_view_reads.py. 2) Test H12 y arreglo. 3) Test H13 con subprocess; arreglo solo si falla. 4) Informe con el resultado de H13.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_run_view_reads.py
- TMPDIR=/dev/shm pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm pytest -q tests/api/test_view_doc.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los dos tests nuevos; el informe dice si H13 se reprodujo; CHANGELOG y commit; aviso a deskops con deskops message send --to deskops.

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

FILE:src/sldb/api/views/view_source.py
"""Which ViewDoc node a name means, and its file read from the store that tracks it (H9).

A ViewDoc may live in the calling store or in a store it links to (DA4: deskops' views ship
only in its package store). The composed index names a linked one `<link>:ViewDoc:<name>`
and stamps every node with `facets.source.store_path`, the `.sldb` that contributed it: the
file is read from that store's root, through the read guard (`sldb.store.source_read`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.models.notation.view_doc import ViewDoc
from sldb.runtime.validation import extract_model_data
from sldb.store.layout import project_root
from sldb.store.source_guard import aggregate_text, target_text

VIEW_MODEL = "ViewDoc"


def view_node(index: Any, name: str) -> Any:
    """The ViewDoc node `name` means: the local one first, else the only linked one with that
    name; `<link>:<name>` names a linked one directly. Several linked = ambiguous, an error."""
    local = index.node(f"{VIEW_MODEL}:{name}")
    if local is not None and local.node_type == VIEW_MODEL:
        return local
    found = [n for n in index.nodes_of_type(VIEW_MODEL) if n.semantics.get("store") and name in (bare_name(n), qualified_name(n))]
    if len(found) > 1:
        stores = ", ".join(sorted(n.semantics["store"] for n in found))
        raise SLDBDocumentTargetError(f"Ambiguous view: {name} (linked in {stores})")
    if not found:
        raise SLDBDocumentTargetError(f"Unknown view: {name}")
    return found[0]


def bare_name(node: Any) -> str:
    """The view's name, without the link it comes through."""
    return node.semantics["export_id"].split(":", 1)[1]


def qualified_name(node: Any) -> str:
    """`<link>:<name>` for a linked view, `<name>` for a local one."""
    store = node.semantics.get("store")
    return f"{store}:{bare_name(node)}" if store else bare_name(node)


def view_store(node: Any) -> Path:
    """The `.sldb` of the store that tracks the node (the linked one for a linked view)."""
    return Path(node.facets["source"]["store_path"])


def read_view_node(node: Any) -> ViewDoc:
    """The ViewDoc extracted from its file, under the root of the store that tracks it; a path
    that leaves that root or is a symlink is not read (`SLDBDocumentTargetError` naming its
    finding, `store/path-outside-root` or `store/symlink-not-read`)."""
    root = project_root(view_store(node))
    text = target_text(root, root / node.semantics["path"], f"{VIEW_MODEL}:{qualified_name(node)}")
    return ViewDoc.model_validate(extract_model_data(ViewDoc, text))


def readable_view_node(node: Any) -> ViewDoc | None:
    """`read_view_node` for a listing: a path the read guard refuses is warned and gives None."""
    root = project_root(view_store(node))
    text = aggregate_text(root, root / node.semantics["path"], f"{VIEW_MODEL}:{qualified_name(node)}")
    return ViewDoc.model_validate(extract_model_data(ViewDoc, text)) if text is not None else None

FILE:src/sldb/api/views/view_revision.py
"""The revision of a view's result (GD25, q16): what changes when anything it read changes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from sldb.api.views.view_source import view_store
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path


def revision(store_path: Path, index: Any, row_ids: set[str], view: Any, rule_ids: list[str]) -> str:
    """sha256 of the rows' documents' `source_hash` (sorted), the ViewDoc's and the used
    RuleDocs' `content_hash`, and the store's shards signature (an edge reaching a row from
    a new document moves the shards, not the row). `view` is the ViewDoc's index node: its
    hash is read from the store that tracks it, a linked one included (H9)."""
    read = {
        "documents": sorted(source_hash(index, export_id) for export_id in row_ids),
        "view": content_hash(view_store(view), view.semantics["export_id"]),
        "rules": [content_hash(store_path, rule_id) for rule_id in sorted(set(rule_ids))],
        "shards": shards_signature(store_path),
    }
    return hashlib.sha256(json.dumps(read, sort_keys=True, default=list).encode("utf-8")).hexdigest()


def source_hash(index: Any, export_id: str) -> str:
    node = index.node(export_id)
    return node.source_hash if node is not None else ""


def content_hash(store_path: Path, export_id: str) -> str:
    """A local document's `content_hash` from its shard; empty when the shard is missing."""
    model, name = export_id.split(":")[-2], export_id.split(":")[-1]
    entry = load_document_shard(documents_shard_path(store_path, model, name))
    return entry.content_hash if entry is not None else ""

FILE:tests/api/test_run_view_reads.py
"""H11: `run_view` composes the edge index of the calling store alone unless the view can name a
linked store, and a composed index survives the process in the store's `.sldb_cache`."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.store.edge_index import compose
from sldb.store.edge_index.compose import invalidate_composed_edge_indexes
from sldb.store.io.shards import invalidate_shard_cache

MODULE = "sldb_h11_run_view_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


def view(name: str, select: dict) -> dict:
    return {"id": name, "name": name, "title": name, "sections": [{"key": "notes", "select": select, "fields": ["title"]}]}


def make_store(base: Path, name: str, py: str) -> tuple[Path, Path]:
    root = base / name
    root.mkdir()
    store = api.init_store(root).store_path
    for ref in (f"{MODULE}:Note", "sldb.models.notation_models:ViewDoc"):
        api.add_model(store, ref, py)
    return root, store


def note(root: Path, store: Path, py: str, name: str, title: str) -> None:
    api.create_document(store, "Note", root / f"{name}.md", {"title": title}, name, py)


@pytest.fixture
def linked(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        py = str(tmp_path)
        (a_root, a), (b_root, b) = make_store(tmp_path, "A", py), make_store(tmp_path, "B", py)
        note(a_root, a, py, "a1", "from A")
        note(b_root, b, py, "b1", "from B")
        for name, select in (("local", {"model": "Note"}), ("wide", {"model": "Note", "include_linked": True}), ("byref", {"prefix": "B:b"})):
            api.create_document(a, "ViewDoc", a_root / f"{name}.md", view(name, select), name, py)
        api.link_store(a, b, name="B")
        yield a, lambda title: note(b_root, b, py, "b2", title)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def reads(monkeypatch, name: str, store: Path) -> tuple[list[bool], dict]:
    seen: list[bool] = []
    run = sys.modules["sldb.api.views.view_reading"]
    original = run.load_edge_index
    monkeypatch.setattr(run, "load_edge_index", lambda s, include_linked=True, **k: seen.append(include_linked) or original(s, include_linked=include_linked, **k))
    return seen, api.run_view(store, name)


def test_a_view_that_names_no_link_reads_only_the_calling_store(linked, monkeypatch) -> None:
    a, _ = linked
    seen, result = reads(monkeypatch, "local", a)
    assert seen == [False]
    assert [r["export_id"] for r in result["sections"]["notes"]["rows"]] == ["Note:a1"]


@pytest.mark.parametrize("name", ["wide", "byref"])
def test_a_view_that_can_name_a_link_reads_the_linked_stores(linked, monkeypatch, name: str) -> None:
    a, _ = linked
    seen, _ = reads(monkeypatch, name, a)
    assert seen == [False, True]


def test_the_revision_follows_a_linked_store_only_for_a_view_that_selects_it(linked) -> None:
    a, add_b_note = linked
    before = {n: api.run_view(a, n)["revision"] for n in ("local", "wide")}
    add_b_note("new in B")
    after = {n: api.run_view(a, n) for n in ("local", "wide")}
    assert after["local"]["revision"] == before["local"]
    assert after["wide"]["revision"] != before["wide"]
    assert "B:Note:b2" in [r["export_id"] for r in after["wide"]["sections"]["notes"]["rows"]]


def forget_process() -> None:
    invalidate_composed_edge_indexes()
    invalidate_shard_cache()


def test_a_new_process_reads_the_composed_index_from_disk_and_a_moved_store_recomposes(linked, monkeypatch) -> None:
    a, add_b_note = linked
    first = api.run_view(a, "local")
    composed = []
    original = compose._compose
    monkeypatch.setattr(compose, "_compose", lambda *args: composed.append(1) or original(*args))
    forget_process()
    assert api.run_view(a, "local") == first and composed == []
    add_b_note("moves B")
    forget_process()
    api.run_view(a, "wide")
    api.run_view(a, "wide")
    forget_process()
    assert api.run_view(a, "wide")["sections"] and len(composed) == 1


def test_a_view_read_inside_a_failed_transaction_leaves_no_composed_file_and_rolls_back(linked) -> None:
    from sldb.store.layout import cache_dir

    a, _ = linked
    forget_process()
    composed = cache_dir(a) / "composed"
    for stale in composed.glob("*.json"):
        stale.unlink()
    with pytest.raises(RuntimeError, match="boom"):
        with api.transaction(a) as tx:
            assert api.run_view(a, "local")["sections"]["notes"]["rows"]
            tx.write_file("scratch.txt", b"x")
            raise RuntimeError("boom")
    assert not list(composed.glob("*.json"))
    assert api.run_view(a, "local")["sections"]
    assert list(composed.glob("*.json"))  # outside a transaction it is kept as before

FILE:instruccion
Cold-bundle de la tarea task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_run_view_reads.py
- TMPDIR=/dev/shm pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm pytest -q tests/api/test_view_doc.py

