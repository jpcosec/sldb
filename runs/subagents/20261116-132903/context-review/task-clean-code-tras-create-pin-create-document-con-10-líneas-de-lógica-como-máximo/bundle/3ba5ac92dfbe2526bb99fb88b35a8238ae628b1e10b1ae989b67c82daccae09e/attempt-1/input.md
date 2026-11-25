FILE:desk/tasks/task-clean-code-tras-create-pin-create-document-con-10-líneas-de-lógica-como-máximo.md
---
sldb:
  by: agent
  at: '2026-11-16T13:09:20Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-create-pin-create-document-con-10-líneas-de-lógica-como-máximo
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
- src/sldb/api/documents/create_document.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
---

# Clean code tras create-pin: create_document con 10 líneas de lógica como máximo

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: la función create_document de src/sldb/api/documents/create_document.py tiene 12 líneas de lógica (máximo 10). Lo introdujo task-create-document-pinnea (e82d62ba); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-create-document-pinnea, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Extraer a una función privada con nombre el paso de pinneo y render (pin_payload, _rendered, pin_provenance) o el de escritura, en el mismo archivo si este sigue bajo 80 líneas, si no en un módulo vecino. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py
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

FILE:desk/atoms/atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa.md
---
sldb:
  by: agent
  at: '2026-11-16T11:09:58Z'
  authority: generated
  via: create_document
id: atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
title: 'Crear un documento ya fija sus anclas a documentos: create_document pinnea
  igual que save_document_payload'
five_wh_one_plus: what
tags:
- system:sldb
- topic:anchors
provenance: src/sldb/api/documents/create_document.py
---

# Crear un documento ya fija sus anclas a documentos: create_document pinnea igual que save_document_payload

## Answer

create_document (y Transaction.create, que pasa por él) llama pin_payload sobre el payload antes de renderizar y validar, y pin_provenance sobre el texto antes de escribirlo, en el mismo orden que save_document_payload. Un campo de __doc_anchors__ que nombra un destino trackeado sin @sha256 queda escrito con el hash de contrato del destino (anchor_state intact) sin necesidad de un save posterior. Un destino no trackeado queda como estaba (lost).

FILE:src/sldb/api/documents/create_document.py
"""Render a payload to a new Markdown file and track it as a document of a registered model."""

from __future__ import annotations
from sldb.api.stores.declaration_sync import declare_tracked, project_relative

from pathlib import Path
from typing import Any

from sldb.api.documents.doc_anchor_pinning import pin_payload, pin_provenance
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.documents.on_write_gate import check_entering
from sldb.api.documents.refuse_structural_noise import refuse_structural_noise
from sldb.api.documents.frontmatter_keys import refuse_undeclared_frontmatter
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from sldb.api.documents.provenance_stamp import stamped
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.ops import track_document
from sldb.store.source_guard import READ_CODES, write_source_text
from sldb.store.source_read import SYMLINK


def create_document(store: str | Path | None, model_name: str, path: str | Path, payload: dict[str, Any], name: str | None = None, pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Write the Markdown a model renders from `payload` and start tracking it.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file to write (parents are created, an existing file is
            overwritten); a relative path is relative to the project root, not the cwd.
        payload: The document's field values; it has no fixed schema beyond the model's own.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        actor: Optional caller label, stamped into the document's provenance block.

    Returns:
        The created document.

    Raises:
        SLDBStoreError: When the model is not registered, or a RuleDoc's subject names a model
            the store does not register.
        SLDBValidationError: When the rendered Markdown does not round-trip under the model,
            or when it carries headings the model does not declare; nothing is written then.

    Unpinned `doc:Model:name` anchors in `__doc_anchors__` fields and in the provenance `from:`
    are pinned with the target's contract hash before writing, as `save_document_payload` does
    (GO07); an untracked target leaves the value as it is.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    payload = pin_payload(location.store_path, registered.model_type, payload)
    rendered = _rendered(location, registered.model_type, payload, pythonpath)
    doc_path = _resolve_path(path, location.project_root)
    doc_name = name or doc_path.stem
    _admit(location.store_path, registered, rendered, doc_name, payload)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    text = pin_provenance(location.store_path, stamped(rendered + "\n", registered.model_type, "create_document", actor))
    write_source_text(doc_path, text)
    _track(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def refuse_noise(model_type: type, markdown: str, name: str, store_path: Path | None = None) -> None:
    """Refuse a document whose headings (unless the store's policy allows them) or frontmatter
    keys the model never declares."""
    from sldb.api.stores.policy import Policy

    refuse_structural_noise(model_type, markdown, name, Policy.of_store(store_path) if store_path else None)
    refuse_undeclared_frontmatter(model_type, markdown, name)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    """The new document's path, resolved; a symlink there is refused BEFORE resolving (the write
    would go where it points). A plain path outside the project is still created (spec2viz)."""
    raw_path = Path(raw) if Path(raw).is_absolute() else root / raw
    if raw_path.is_symlink():
        raise SLDBDocumentTargetError(f"[{READ_CODES[SYMLINK]}] {raw}: the path is a symlink; sldb does not write it")
    return raw_path.resolve()


def _track(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, pythonpath: str | None) -> None:
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    declare_tracked(sp, root, registered.entry.name, project_relative(root, doc_path), doc_name)


def _rendered(location, model_type: type, payload: dict[str, Any], pythonpath: str | None) -> str:
    """The round-tripped Markdown, once a RuleDoc's subject names only registered models."""
    rendered = _render_roundtrip(model_type, payload, location.project_root)
    refuse_unknown_family(location.store_path, model_type, payload, pythonpath)
    return rendered


def _render_roundtrip(model_type: type, payload: dict[str, Any], ref_root: Path) -> str:
    """The payload rendered to Markdown, refused unless it extracts back identically.

    `ref_root` is the project root, so a composed field resolves its refs the way the project
    names them; without it they would resolve against whatever directory the caller runs in.
    """
    rendered = render_model_markdown(model_type, payload, ref_root)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
    return rendered


def _admit(sp: Path, registered, rendered: str, doc_name: str, payload: dict[str, Any]) -> None:
    """Refuse a document the model's structure or an `on_write` rule (H4) does not admit."""
    refuse_noise(registered.model_type, rendered, doc_name, sp)
    check_entering(sp, registered.model_type, registered.entry.name, doc_name, payload)

FILE:instruccion
Cold-bundle de la tarea task-clean-code-tras-create-pin-create-document-con-10-líneas-de-lógica-como-máximo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

