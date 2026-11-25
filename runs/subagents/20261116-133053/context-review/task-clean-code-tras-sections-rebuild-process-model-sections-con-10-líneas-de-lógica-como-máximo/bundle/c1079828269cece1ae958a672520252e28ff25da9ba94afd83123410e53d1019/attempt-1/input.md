FILE:desk/tasks/task-clean-code-tras-sections-rebuild-process-model-sections-con-10-líneas-de-lógica-como-máximo.md
---
sldb:
  by: agent
  at: '2026-11-16T13:09:52Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-sections-rebuild-process-model-sections-con-10-líneas-de-lógica-como-máximo
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
- src/sldb/store/section_sync.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
---

# Clean code tras sections-rebuild: process_model_sections con 10 líneas de lógica como máximo

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: la función process_model_sections de src/sldb/store/section_sync.py tiene 13 líneas de lógica (máximo 10). Lo introdujo task-una-escritura-sections-rebuild (e55d872f); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-una-escritura-sections-rebuild, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Extraer el cálculo y la emisión del aviso resumido (missing_paths nuevos desde la marca, missing_summary y logger.warning) a una función privada _warn_missing(report, start, model_name); si section_sync.py pasa de 80 líneas, mover missing_summary a un módulo vecino reexportándola. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_semantic_rebuild.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Todos los comandos de Validation pasan (incluidos test_clean_code_rules y check.sh --fast); git diff no toca archivos de tests de comportamiento; CHANGELOG y commit.

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

FILE:desk/atoms/atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n.md
---
sldb:
  by: agent
  at: '2026-11-16T10:14:16Z'
  authority: generated
  via: create_document
id: atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n
title: Una reconstrucción de secciones con documentos trackeados ausentes avisa una
  vez por modelo, con el número y hasta tres ejemplos
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: src/sldb/store/section_sync.py
---

# Una reconstrucción de secciones con documentos trackeados ausentes avisa una vez por modelo, con el número y hasta tres ejemplos

## Answer

src/sldb/store/section_sync.py acumula en RebuildReport.missing_paths (src/sldb/store/semantic.py) las rutas de los documentos trackeados que no están en disco, por ejemplo los PythonSymbolDoc generados en un checkout limpio. process_model_sections emite un solo logger.warning por modelo con el formato 'Sections rebuild: <n> documents missing on disk (<Modelo>: <n>); e.g. <r1>, <r2>, <r3>' (missing_summary), en lugar de una línea por documento. report.verbose sigue con una entrada por ausente.

FILE:src/sldb/store/section_sync.py
"""Bringing one model's sections shards current (PLAN 15 capa 5): skipped whole when the
model's model_hash has not moved; otherwise every document's shard synced (`section_doc_
contribution.sync_doc_shard`) and shards of documents no longer tracked pruned. The
markdown parsing itself stays in section_rebuild.py; this is the per-model plumbing around
it, split out to keep both files under this project's own line-count rule."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from sldb.store import documents_hash
from sldb.store.io import load_models_index, save_models_index
from sldb.store.io.shards import prune_shards
from sldb.store.layout import sections_index_relpath, sections_shards_dir
from sldb.store.section_doc_contribution import sync_doc_shard
from sldb.store.section_paths import section_cache_key
from sldb.store.source_read import unreadable_reason

logger = logging.getLogger(__name__)


def process_model_sections(m_entry, root, report, store_path: Path | None, process_doc_sections) -> None:
    from sldb.store import built_cache

    m_idx = load_models_index(root / m_entry.models_index)
    key = section_cache_key(m_idx)
    if store_path and built_cache.get(store_path, "sections_shards", m_entry.name, key) is not None and _shards_kept(sections_shards_dir(store_path, m_entry.name), m_idx):
        return
    start = len(report.missing_paths)
    current = _sync_model_sections(store_path, m_entry, m_idx, root, report, process_doc_sections)
    if missing := report.missing_paths[start:]:
        logger.warning(missing_summary({m_entry.name: len(missing)}, missing))
    _mark_has_sections(store_path, m_entry, m_idx, root, current)
    if store_path:
        built_cache.put(store_path, "sections_shards", m_entry.name, key, True)


def _mark_has_sections(store_path: Path, m_entry, m_idx, root, current: set[str]) -> None:
    if current and not m_idx.sections_index:
        m_idx.sections_index = sections_index_relpath(store_path, m_entry.name)
        save_models_index(root / m_entry.models_index, m_idx)


def _sync_model_sections(store_path, m_entry, m_idx, root, report, process_doc_sections) -> set[str]:
    """PLAN 15 capa 8: `entries` is this operation's own cache (composed from shards at most
    once); every document's file is still cheaply checked to exist (as before, for pruning
    correctness), but only one in the dirty set (or every one, with no trustworthy baseline)
    is actually opened and re-synced — an untouched document's sections shard is never read
    just to confirm it agrees with a source_hash that has not moved."""
    entries = {e.name: e for e in documents_hash.entries_of(store_path, m_entry.name)}
    dirty = documents_hash.dirty_names(store_path, m_entry.name, "sections") if sections_shards_dir(store_path, m_entry.name).is_dir() else None  # no shards: no baseline
    current = {doc.name for doc in entries.values() if _sync_one_section(store_path, doc, m_entry, root, report, process_doc_sections, dirty is None or doc.name in dirty)}
    if store_path:
        prune_shards(sections_shards_dir(store_path, m_entry.name), current)
    documents_hash.clear_dirty(store_path, m_entry.name, "sections")
    return current


def _sync_one_section(store_path, doc, m_entry, root, report, process_doc_sections, do_sync: bool) -> bool:
    d_path = root / doc.path
    if unreadable_reason(root, d_path) is not None:
        return False  # not read (source_read): `stores check` and `stores update` name it
    if not d_path.exists():
        _missing_doc(doc, d_path, root, report)
        return False
    if do_sync:
        sync_doc_shard(store_path, doc, d_path, m_entry, report, process_doc_sections)
    return True


def _missing_doc(doc, d_path, root, report) -> None:
    """Counted and listed, not logged: a store whose generated documents (say
    `knowledge/symbols/`, ignored by git) are absent printed one line per document on every
    write; `process_model_sections` logs one summary line instead."""
    report.docs_skipped_missing += 1
    report.verbose.append(f"sections: {doc.name} — missing file {d_path}")
    report.missing_paths.append(Path(os.path.relpath(d_path, root)).as_posix())


def missing_summary(per_model: dict[str, int], paths: list[str]) -> str:
    models = ", ".join(f"{name}: {n}" for name, n in sorted(per_model.items()))
    return f"Sections rebuild: {len(paths)} documents missing on disk ({models}); e.g. {', '.join(sorted(paths)[:3])}"


def _shards_kept(shards_dir: Path, m_idx) -> bool:
    """The user cache says the shards are current; they are only if they are still there. A
    deleted `.sldb_cache/` (then `.sldb/runtime/`) left the cache trusting shards that no longer existed, so no
    rebuild (nor `stores update`) brought sections back."""
    return not m_idx.documents_count or shards_dir.is_dir()

FILE:instruccion
Cold-bundle de la tarea task-clean-code-tras-sections-rebuild-process-model-sections-con-10-líneas-de-lógica-como-máximo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_semantic_rebuild.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

