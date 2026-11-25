FILE:desk/tasks/task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio.md
---
sldb:
  by: agent
  at: '2026-11-16T07:41:24Z'
  authority: generated
  via: save_document_payload
id: task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-cada-escritura-en-el-desk-de-sldb-imprime-miles-de-líneas-sections-rebuild-missing-de-knowledge-symb.md
depends_on: []
pills:
- desk/contexts/pill-pill-dónde-se-agrupan-los-ausentes-de-sections-rebuild.md
files:
- src/sldb/store/section_sync.py
- tests/store/test_semantic_rebuild.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Una escritura en un store con documentos generados ausentes no imprime una línea por cada uno (Sections rebuild missing)

## Rationale

_Explain why this task exists or the business driver behind it._

Cada comando que escribe en el desk de sldb (add atom, edit task, docs update) imprime unas 2500 líneas "Sections rebuild: doc '<id>' missing at <root>/knowledge/symbols/<id>.md". Son PythonSymbolDoc indexados en el store pero generados (knowledge/symbols/ está en .gitignore), así que no existen en un checkout limpio. El comando termina bien, pero el ruido tapa el resultado. La fuente es src/sldb/store/section_sync.py: _missing_doc (línea 72) emite un logger.warning por documento, llamado desde _sync_one_section (línea 56). Origen: desk/inbox/inbox-note-cada-escritura-en-el-desk-de-sldb-imprime-miles-de-líneas-sections-rebuild-missing-de-knowledge-symb.md.

## Goal

_Describe the concrete result this task must produce._

Una reconstrucción de secciones con N documentos ausentes emite a lo sumo una línea de aviso con el número de ausentes, el modelo y hasta 3 ejemplos, en lugar de N líneas.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/store/section_sync.py acumular los ausentes durante la reconstrucción y emitir un solo logger.warning al final con el formato "Sections rebuild: <n> documents missing on disk (<modelo>: <n>, ...); e.g. <ruta1>, <ruta2>, <ruta3>". Las rutas que llaman (src/sldb/api/documents/payload_save_steps.py:112, src/sldb/api/documents/untrack_document.py:68, src/sldb/api/edges/rebuild_edges.py:37) no cambian. Test en tests/store/test_semantic_rebuild.py con caplog: un store de prueba con 5 documentos trackeados cuyo archivo se borró produce exactamente un registro de warning que dice 5. CHANGELOG.md. No entra: limitar la reconstrucción a los documentos que tocó la transacción (otro cambio, más invasivo), ni cambiar cómo stores check reporta los PythonSymbolDoc ausentes (tarea de stores check sobre un clon sin build).

Precisiones (preflight-1): la acumulación usa el report que ya recorre la reconstrucción (report.docs_skipped_missing y report.verbose en section_sync.py): _missing_doc deja de llamar a logger.warning y agrega la ruta relativa al proyecto a una lista nueva report.missing_paths; la función de nivel superior que arma el report emite al terminar un solo logger.warning si la lista no está vacía. Formato exacto: "Sections rebuild: <n> documents missing on disk (<Modelo>: <n>[, <Modelo>: <n>...]); e.g. <ruta1>, <ruta2>, <ruta3>" con modelos en orden alfabético y las tres primeras rutas en orden alfabético. La comprobación manual en el desk es opcional y se hace con una copia del repo en /dev/shm, no en el checkout.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/section_sync.py entero. 2) Cambiar _missing_doc para que agregue a una lista que vive durante la llamada de nivel superior de la reconstrucción y emitir el resumen al final. 3) Test con caplog. 4) Comprobación manual en el desk: `deskops edit task <una tarea> summary "x" --root sldb` en un worktree limpio imprime una línea de Sections en lugar de miles (anotarlo en el informe; no commitear ese cambio de desk).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_semantic_rebuild.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (5 ausentes -> 1 warning que dice 5); test_semantic_rebuild.py completo pasa; CHANGELOG y commit.

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

FILE:desk/contexts/pill-pill-dónde-se-agrupan-los-ausentes-de-sections-rebuild.md
---
sldb:
  by: agent
  at: '2026-11-16T07:41:04Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-dónde-se-agrupan-los-ausentes-de-sections-rebuild
status: active
summary: dónde se agrupan los ausentes de Sections rebuild
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: dónde se agrupan los ausentes de Sections rebuild

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

src/sldb/store/section_sync.py, src/sldb/store/semantic.py

## How

_Describe the correct way to apply this guidance._

RebuildReport vive en src/sldb/store/semantic.py y se puede editar para agregar missing_paths: list[str]. El modelo es m_entry.name. El aviso se emite una vez por llamada a la función de section_sync que recorre los modelos; si esa función se llama por modelo, sale una línea por modelo con ausentes, y eso es válido. report.verbose sigue acumulando una entrada por ausente (no es log). Los documentos se trackean con sldb.api.create_document y después se borran sus archivos.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.

FILE:src/sldb/store/section_sync.py
"""Bringing one model's sections shards current (PLAN 15 capa 5): skipped whole when the
model's model_hash has not moved; otherwise every document's shard synced (`section_doc_
contribution.sync_doc_shard`) and shards of documents no longer tracked pruned. The
markdown parsing itself stays in section_rebuild.py; this is the per-model plumbing around
it, split out to keep both files under this project's own line-count rule."""

from __future__ import annotations

import logging
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
    current = _sync_model_sections(store_path, m_entry, m_idx, root, report, process_doc_sections)
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
        _missing_doc(doc, d_path, report)
        return False
    if do_sync:
        sync_doc_shard(store_path, doc, d_path, m_entry, report, process_doc_sections)
    return True


def _missing_doc(doc, d_path, report) -> None:
    report.docs_skipped_missing += 1
    report.verbose.append(f"sections: {doc.name} — missing file {d_path}")
    logger.warning(f"Sections rebuild: doc '{doc.name}' missing at {d_path}")


def _shards_kept(shards_dir: Path, m_idx) -> bool:
    """The user cache says the shards are current; they are only if they are still there. A
    deleted `.sldb_cache/` (then `.sldb/runtime/`) left the cache trusting shards that no longer existed, so no
    rebuild (nor `stores update`) brought sections back."""
    return not m_idx.documents_count or shards_dir.is_dir()

FILE:tests/store/test_semantic_rebuild.py
from __future__ import annotations

from pathlib import Path

import pytest

from sldb.store.semantic import RebuildReport
from sldb.store.section_rebuild import _extract_sections


class TestExtractSectionsEdgeCases:
    def test_plain_paragraph_no_headings(self):
        md = "This is a plain paragraph with no headings.\n\nJust text."
        sections = _extract_sections(md)
        assert sections == []

    def test_empty_string(self):
        sections = _extract_sections("")
        assert sections == []

    def test_only_thematic_breaks_and_code_blocks(self):
        md = "---\n\n```python\nprint('hello')\n```\n\n***"
        sections = _extract_sections(md)
        assert sections == []

    def test_heading_with_no_map_attribute(self):
        md = "# Title\n\nSome content."
        sections = _extract_sections(md)
        assert len(sections) == 1
        assert sections[0]["title"] == "Title"
        assert sections[0]["line_start"] is not None

    def test_single_heading(self):
        md = "# Hello\n\nWorld"
        sections = _extract_sections(md)
        assert len(sections) == 1
        assert sections[0]["title"] == "Hello"
        assert sections[0]["level"] == 1
        assert sections[0]["slug"] == "hello"
        assert sections[0]["path"] == "hello"

    def test_multiple_headings_with_hierarchy(self):
        md = "# A\n\n## B\n\n### C\n\n# D"
        sections = _extract_sections(md)
        assert len(sections) == 4
        assert sections[0]["path"] == "a"
        assert sections[1]["path"] == "a/b"
        assert sections[2]["path"] == "a/b/c"
        assert sections[3]["path"] == "d"

    def test_malformed_heading_no_title(self):
        md = "# \n\nContent after empty heading."
        sections = _extract_sections(md)
        assert sections == []


class TestRebuildReportDataclass:
    def test_default_values(self):
        r = RebuildReport()
        assert r.docs_processed == 0
        assert r.docs_skipped_missing == 0
        assert r.docs_empty_sections == 0
        assert r.headings_no_map == 0
        assert r.verbose == []

    def test_increment_fields(self):
        r = RebuildReport()
        r.docs_processed += 1
        r.docs_skipped_missing += 2
        r.docs_empty_sections += 1
        r.headings_no_map += 1
        r.verbose.append("test message")
        assert r.docs_processed == 1
        assert r.docs_skipped_missing == 2
        assert r.docs_empty_sections == 1
        assert r.headings_no_map == 1
        assert r.verbose == ["test message"]

FILE:instruccion
Cold-bundle de la tarea task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/store/test_semantic_rebuild.py

