FILE:desk/tasks/task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de.md
---
sldb:
  by: agent
  at: '2026-11-16T05:42:48Z'
  authority: generated
  via: save_document_payload
id: task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-sldb-docs-update-valida-y-reescribe-documentos-ajenos-al-que-actualiza.md
depends_on: []
pills: []
files:
- tests/store/test_doc_invalid_writes.py
- src/sldb/api/documents/payload_save.py
- src/sldb/api/documents/payload_save_steps.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
---

# Reproducir si sldb docs update reescribe índices de documentos ajenos al que actualiza (ReviewDoc de un store enlazado con otro contrato)

## Rationale

_Explain why this task exists or the business driver behind it._

En el kit Chatbot_Infra (enlazado a un checkout viejo de deskops cuyo ReviewDoc no conocía kind evidence), `sldb docs update borrado-de-una-persona` falló con 2 validation errors de ReviewDoc sobre recibos que no eran el documento actualizado, y además dejó modificados 5 ReviewDoc .yaml ajenos sin el tag workspace:desk. La parte "una escritura cae por un vecino inválido" se arregló en 9668e881 (tests/store/test_doc_invalid_writes.py, test_a_transactional_write_of_a_valid_document_touches_only_it). No está verificado si update todavía reescribe shards de índice de otros documentos. Reportado por AntonIA el 2026-11-10. Origen: desk/inbox/inbox-note-sldb-docs-update-valida-y-reescribe-documentos-ajenos-al-que-actualiza.md.

## Goal

_Describe the concrete result this task must produce._

Saber, con un test que lo prueba, si `sldb docs update <doc>` sobre un store que enlaza a otro store cuyo modelo rechaza algunos de sus documentos modifica algún archivo fuera del documento actualizado, su shard y los índices derivados del store (store_index.yaml y models/<Modelo>.yaml del modelo del documento).

## Scope

_State what is in scope and what is out of scope._

Entra: (1) test de reproducción en tests/store/test_doc_invalid_writes.py: store A con un modelo y un documento; store B enlazado desde A con un modelo ReviewDoc-like cuyos documentos dejan de validar al cambiar el modelo (un Literal que pierde un valor); snapshot de bytes de todos los archivos de A y B; `docs update` del documento de A; comparar. (2) Si el test muestra archivos ajenos modificados, arreglar en src/sldb/api/documents/payload_save.py (save_document_payload, línea 15) o en el paso de reconstrucción de src/sldb/api/documents/payload_save_steps.py (línea 112) para que solo se escriban el documento, su shard y los índices derivados que dependen de él, y que los documentos inválidos de B se reporten como alerta. (3) Si no se reproduce con caché caliente ni con caché fría (sin .sldb_cache), el test queda como guarda de regresión y el informe lo dice; la tarea cierra igual. CHANGELOG.md solo si hubo arreglo. No entra: cambiar el modelo ReviewDoc de deskops, tocar el kit Chatbot_Infra.

Precisiones (preflight-1): el enlace se crea con la API pública de stores (la función que usa `sldb stores add`, en src/sldb/api/stores/link_store.py), como en los tests de tests/api/test_api_stores.py. El cambio de modelo se simula con dos módulos de modelo en tmp_path: B se construye con el modelo v1 (Literal["a","b"]) y documentos con "b"; después se reescribe el módulo a v2 (Literal["a"]) y se limpia sys.modules de ese módulo antes del update. Archivos legítimos de cambiar: el Markdown del documento de A, su shard bajo .sldb/core/documents/<Modelo de A>/, .sldb/core/store_index.yaml de A y .sldb/core/models/<Modelo de A>.yaml de A; cualquier otro archivo modificado (en A o en B) es la falla. "Sin caché" es borrar .sldb_cache de A y B antes del update. La "alerta" es un Finding de nivel alert enviado por sldb.core.finding_route.route, como las demás alertas de escritura.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/store/test_doc_invalid_writes.py (fixtures existentes), payload_save.py y payload_save_steps.py. 2) Escribir el test con snapshot de bytes (dict ruta -> sha256 antes y después). 3) Correrlo con y sin .sldb_cache. 4) Arreglo solo si falla. 5) Informe con resultado de ambas corridas.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_writes.py
- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_check.py

## Done When

_Name the observable condition that makes the task complete._

El test de reproducción existe y pasa; el informe dice si se reprodujo (con caché caliente y fría) y, si se reprodujo, qué se cambió; commit; respuesta a AntonIA con deskops message send --to AntonIA (si ese repo no está registrado para el envío, el aviso va como línea "Aviso a AntonIA" en el informe de cierre).

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

FILE:desk/atoms/atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada.md
---
id: atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
title: Una escritura de varios documentos en sldb es todo o nada
five_wh_one_plus: what
tags:
- system:sldb
- topic:transactions
- topic:write-api
provenance: docs/architecture/transactions.md
---

# Una escritura de varios documentos en sldb es todo o nada

## Answer

Toda escritura de sldb que toca más de un documento (sldb.api.transaction, apply_batch, move_document y POST /save de sldb serve) es atómica: si un cambio falla, se restauran los bytes de los archivos, las entradas del índice y los shards (documents, semantic, sections, edges) al estado previo, y el store vuelve a pasar stores check. Las transacciones se anidan y la más externa decide. Una guarda de concurrencia vieja (expected_sha256 o expected_source_hash) es un ConflictError que no escribe nada (409 en serve). Si el rollback mismo no puede restaurar algo, levanta RollbackError con la lista de rutas sin restaurar en vez de dejar el store a medias en silencio. Toda ruta de escritura (fields update, docs update, /save, apply_batch, transaction) valida contra el modelo, y un payload que el model_validator rechaza no llega al disco (G4); por /save eso es un 422. Decisión DA2 del dueño y G4 del plan generalizar-desde-deskops; implementado en GD24.

FILE:tests/store/test_doc_invalid_writes.py
"""H2 and H3 of inbox 3895e9f7: with two documents their model rejects, untracking one of the
model's documents and a transactional write of a valid one succeed and touch nothing else; a
transaction that fails leaves the tree as it was. Each write runs in a fresh process, as a CLI
does, with the caches kept (warm) or gone as in a clean clone (cold): only a cold cache rebuilds
every document's edges, which is where an invalid neighbour used to stop the write (H2) and
leave its shards rewritten (H3)."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from sldb.store.layout import documents_shard_path

from tests.store.invalid_memo_store import store_with_invalid  # noqa: F401 - the fixture

_SRC = Path(__file__).resolve().parents[2] / "src"
_TX = "with api.transaction(sp, py) as tx:\n    api.replace_text(sp, 'c', '# c', '# c2', transaction=tx, pythonpath=py)\n"


def _tree(root: Path, cache: bool = False) -> dict[str, bytes]:
    """Every file under the project, lock files aside; the regenerable cache only with `cache`."""
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file() and "locks" not in p.parts and (cache or ".sldb_cache" not in p.parts)}


def _changed(before: dict[str, bytes], after: dict[str, bytes]) -> set[str]:
    return {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}


def _run(store, cache: str, code: str) -> subprocess.CompletedProcess:
    """`code` in a new process over the store (`api`, `sp`, `py` bound); `cold` drops every cache first."""
    root, sp, py = store
    if cache == "cold":
        shutil.rmtree(root / ".sldb_cache", ignore_errors=True)
        shutil.rmtree(os.environ["XDG_CACHE_HOME"], ignore_errors=True)
    prelude = f"import sys\nsys.path[:0] = [{str(_SRC)!r}, {py!r}]\nfrom sldb import api\nsp, py = {str(sp)!r}, {py!r}\n"
    return subprocess.run([sys.executable, "-c", prelude + code], capture_output=True, text=True, cwd=root, timeout=300)


def _shards(root: Path, sp: Path, *names: str) -> set[str]:
    return {documents_shard_path(sp, "Memo", n).relative_to(root).as_posix() for n in names}


@pytest.mark.parametrize("cache", ["warm", "cold"])
@pytest.mark.parametrize("name", ["a", "c"])
def test_untracking_beside_invalid_documents_touches_only_that_one(store_with_invalid, cache, name):
    root, sp, _py = store_with_invalid
    before = _tree(root)
    done = _run(store_with_invalid, cache, f"api.untrack_document(sp, {name!r}, py)")
    assert done.returncode == 0, done.stderr
    changed = _changed(before, _tree(root))
    assert _shards(root, sp, name) <= changed
    assert not ({"a.md", "b.md", "c.md"} | _shards(root, sp, *({"a", "b", "c"} - {name}))) & changed


@pytest.mark.parametrize("cache", ["warm", "cold"])
def test_a_transactional_write_of_a_valid_document_touches_only_it(store_with_invalid, cache):
    root, sp, _py = store_with_invalid
    before = _tree(root)
    done = _run(store_with_invalid, cache, _TX)
    assert done.returncode == 0, done.stderr
    changed = _changed(before, _tree(root))
    assert "c.md" in changed
    assert not ({"a.md", "b.md"} | _shards(root, sp, "a", "b")) & changed


@pytest.mark.parametrize("cache", ["warm", "cold"])
def test_a_failed_transaction_leaves_the_tree_as_it_was(store_with_invalid, cache):
    """Derived shards included: what the rebuilds wrote in the cache is put back or removed."""
    root, _sp, _py = store_with_invalid
    if cache == "cold":
        _run(store_with_invalid, cache, "")  # drops the caches; the snapshot below is taken cold
    before = _tree(root, cache=True)
    done = _run(store_with_invalid, "warm", _TX.replace("pythonpath=py)\n", "pythonpath=py)\n    raise RuntimeError('on purpose')\n"))
    assert done.returncode != 0 and "RuntimeError: on purpose" in done.stderr
    assert "RollbackError" not in done.stderr
    assert _changed(before, _tree(root, cache=True)) == set()

FILE:src/sldb/api/documents/payload_save.py
"""Write a whole payload back to a tracked document: render, round-trip, rehash, reindex."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.doc_anchor_pinning import pin_payload
from sldb.api.documents.payload_save_steps import check_rules_on_write, load_document_entry, load_model_indexes, model_class, render_checked, save_document_indexes, write_rendered_document
from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.stores.open_store import open_store


def save_document_payload(store: str | Path | None, model_name: str, document_name: str, payload: dict[str, Any], pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Replace a tracked document's content with the Markdown rendered from `payload`.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        model_name: Registered model name of the document.
        document_name: Tracked document name.
        payload: The complete new payload; it has no fixed schema beyond the model's own.
        pythonpath: Directory to import the model module from; the store's project root
            is tried next, since a linked store's models import from where it lives.
        actor: Optional caller label, stamped into the document's provenance block.

    Returns:
        The document written.

    Raises:
        SLDBPayloadSaveError: When the model or document is not registered, or the rendered
            Markdown does not round-trip back to the payload.
        SLDBStoreError: When a RuleDoc's subject names a model the store does not register.
        SLDBRuleViolationError: When an `on_write` rule of severity error fails on the payload
            (after its anchors are pinned); nothing is written.
    """
    location = open_store(store)
    idx, m_entry, m_idx = load_model_indexes(location.store_path, location.project_root, model_name)
    doc_entry = load_document_entry(location.store_path, m_entry.name, document_name)
    model_type = model_class(m_entry.model_ref, pythonpath, location.project_root)
    _save(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor)
    return DocumentReference(model=m_entry.name, name=doc_entry.name, path=location.project_root / doc_entry.path)


def _save(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor) -> None:
    payload = pin_payload(location.store_path, model_type, payload)
    check_rules_on_write(location.store_path, model_type, f"{m_entry.name}:{doc_entry.name}", payload)
    rendered = render_checked(model_type, payload, location.project_root)
    refuse_unknown_family(location.store_path, model_type, payload, pythonpath)
    write_rendered_document(location.project_root, doc_entry, model_type, rendered, actor=actor, store_path=location.store_path)
    save_document_indexes(location.store_path, location.project_root, idx, m_idx, m_entry, doc_entry, pythonpath, model_type)

FILE:src/sldb/api/documents/payload_save_steps.py
"""The steps of `save_document_payload`, moved here from `sldb.cli.commands.fields_save`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.core.exceptions import SLDBModelError, SLDBPayloadSaveError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store import documents_hash
from sldb.store.hashing import hash_fields_with_map, hash_text
from sldb.store.io import load_models_index, load_store_index, save_models_index, store_lock
from sldb.store.io.shards import load_document_shard, save_document_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.models.store_index import StoreIndex
from sldb.store.model_node import stamp_model_node
from sldb.store.ops import cascade_store_hash
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes
from sldb.store.source_read import refuse_unreadable
from sldb.store.source_guard import write_source_text
from sldb.models.provenance_block import index_block


def model_class(model_ref: str, pythonpath: str | None, root: Path) -> type:
    """The model class, imported with the caller's pythonpath first, then the store's own root.

    A linked store's models import from where that store lives.
    """
    try:
        return resolve_model_ref(model_ref, pythonpath)
    except SLDBModelError:
        return resolve_model_ref(model_ref, str(root))


def load_model_indexes(sp: Path, root: Path, model_name: str) -> tuple[StoreIndex, ModelEntry, ModelsIndex]:
    """The store index, the model's entry and its models index."""
    idx = load_store_index(sp)
    m_entry = next((m for m in idx.models if m.name == model_name), None)
    if m_entry is None:
        raise SLDBPayloadSaveError(f"Model '{model_name}' not registered.")
    return idx, m_entry, load_models_index(root / m_entry.models_index)


def load_document_entry(sp: Path, model_name: str, doc_name: str) -> DocumentEntry:
    """The document's index entry, from its shard."""
    doc_entry = load_document_shard(documents_shard_path(sp, model_name, doc_name))
    if doc_entry is None:
        raise SLDBPayloadSaveError(f"Doc '{doc_name}' not registered.")
    return doc_entry


def render_checked(model_type: type, payload: dict[str, Any], ref_root: Path, store_path: Path | None = None) -> str:
    """The payload rendered to Markdown, refused unless it round-trips.

    `ref_root` is the project root, so a composed field resolves its refs against the project
    rather than against whatever directory the caller happens to run in. With `store_path`, the
    unpinned document anchors of the payload are pinned first (GO07, `doc_anchor_pinning`).
    """
    from sldb.api.documents.doc_anchor_pinning import pin_payload

    payload = pin_payload(store_path, model_type, payload) if store_path is not None else payload
    rendered = render_model_markdown(model_type, payload, ref_root)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBPayloadSaveError(f"Field mutation broke idempotency: {details}")
    return rendered


def check_rules_on_write(store_path: Path, model_type: type, node: str, payload: dict[str, Any]) -> None:
    """The `on_write` rules on the pinned payload of `node` (GO08), before anything is written:
    an error raises `SLDBRuleViolationError`; a store without RuleDoc is not read."""
    from sldb.api.rules.rules_on_write import check_on_write

    check_on_write(store_path, model_type, node, payload)


def write_rendered_document(root: Path, doc_entry: DocumentEntry, model_type: type, rendered: str, via: str = "save_document_payload", actor: str | None = None, store_path: Path | None = None) -> None:
    """Write the rendered Markdown, signed with its provenance block (plus final newline), and
    record its source and content hashes. With `store_path`, the block's unpinned `from:`
    document anchors are pinned (GO07)."""
    from sldb.api.documents.doc_anchor_pinning import pin_provenance
    from sldb.api.documents.provenance_stamp import stamped_file

    refuse_unreadable(root, root / doc_entry.path)  # a symlink, or a path out of the root, is not written through
    text = stamped_file(root / doc_entry.path, rendered + "\n", model_type, via, actor)
    text = pin_provenance(store_path, text) if store_path is not None else text
    write_source_text(root / doc_entry.path, text)  # O_NOFOLLOW: a symlink swapped in after the check is not written through
    doc_entry.source_hash = hash_text(text)
    doc_entry.content_hash, doc_entry.field_hashes = hash_fields_with_map(model_type, text)
    doc_entry.provenance = index_block(text)


def save_document_indexes(sp: Path, root: Path, idx: StoreIndex, m_idx: ModelsIndex, m_entry: ModelEntry, doc_entry: DocumentEntry, pythonpath: str | None, model_type: type | None = None) -> None:
    """Save the document shard and model hashes, then rebuild derived indexes, under the store lock.

    The model's roster hash covers its documents' hashes: a field write must move it, or
    `stores check` fails and consumers keyed on the model node never see the change.
    """
    with store_lock(sp):
        save_document_shard(documents_shard_path(sp, m_entry.name, doc_entry.name), doc_entry)
        documents_hash.note(sp, m_entry.name, doc_entry)
        stamp_model_node(m_idx, documents_hash.roster_hash_of(sp, m_entry.name), model_type)
        m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
        save_models_index(root / m_entry.models_index, m_idx)
        rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_sections_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_edges_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_store_hash(sp, root, idx)

FILE:instruccion
Cold-bundle de la tarea task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_writes.py
- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_check.py

