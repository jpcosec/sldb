FILE:desk/tasks/task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co.md
---
sldb:
  by: agent
  at: '2026-11-16T06:09:50Z'
  authority: generated
  via: save_document_payload
id: task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co
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
- src/sldb/store/diagnostics.py
- src/sldb/api/stores/store_check.py
- tests/store/test_diagnostics.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista
from_drawer: desk/drawer/tasks/task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales.md
---

# stores check sobre un clon sin build reporta los documentos generados ausentes como una alerta, no como miles de errores

## Rationale

_Explain why this task exists or the business driver behind it._

En un checkout limpio de sldb sin correr stores build, `sldb stores check --store .sldb` da FAIL con 2453 errores, todos PythonSymbolDoc "missing: tracked at knowledge/symbols/<id>.md, not on disk" (mensaje de src/sldb/store/diagnostics_models/document_diagnosis.py:85). knowledge/symbols/ está en .gitignore y esos documentos los genera selfdoc python-sync durante stores build, pero sus shards sí están versionados. Los errores reales quedan tapados. La declaración del store ya dice qué rutas son derivadas (StoreDeclaration.derived en src/sldb/api/stores/store_declaration.py; en este repo `derived: [knowledge/symbols/]` en .sldb/store.yaml), pero stores check no la lee. Se elige reportarlos como alerta resumida (opción reversible y local a stores check); dejar de trackear documentos generados es la decisión de la tarea de python-sync. Origen: drawer desk/drawer/tasks/task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales.md.

## Goal

_Describe the concrete result this task must produce._

En un store cuyo store.yaml declara rutas derived, un documento trackeado ausente cuya ruta cae bajo una de ellas no es error: stores check emite una sola alerta store/generated-missing con el número y el modelo ("2453 PythonSymbolDoc documents are generated and not on disk: run `sldb stores build`"), sigue reportando como error cualquier otro ausente, y su exit code depende solo de los errores.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/store/diagnostics.py (_diagnose_doc línea 36, diagnose_store línea 112) recibir la lista de prefijos derived (leída de la declaración del store) y, para un missing cuya ruta empieza por uno de ellos, contar en lugar de emitir error; al final emitir la alerta resumida por modelo. src/sldb/api/stores/store_check.py (línea 18) pasa la declaración. Tests en tests/store/test_diagnostics.py: store de prueba con derived: [gen/], 3 documentos trackeados ausentes bajo gen/ y 1 ausente fuera de gen/ -> 1 alerta que dice 3 y 1 error. Al cerrar, correr en un clon limpio en /dev/shm `sldb stores check --store .sldb` y `sldb stores build && sldb selfdoc check`, y anotar en el informe el rc y las alertas changed de selfdoc check que queden (resto de la nota de "main de sldb en verde", punto 2). CHANGELOG.md. No entra: destrackear PythonSymbolDoc (decisión de python-sync) ni cambiar selfdoc check.

Precisiones (preflight-1): store_check.py pasa a diagnose_store solo la lista de prefijos (list[str]) de StoreDeclaration.derived; el prefijo se compara por componentes de ruta (Path(ruta).parts empieza por Path(prefijo).parts), no por texto. La alerta es un Finding de nivel alert con code "store/generated-missing", subject "<Modelo>" y el texto de Goal, creado con la función alert() de sldb.core.finding como las demás alertas de stores check. Lo que se anota en result-summary.md es el rc de los dos comandos del clon y las líneas de selfdoc check con estado changed tal como salen.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer diagnostics.py, store_check.py, store_declaration.py y tests/store/test_diagnostics.py (test_missing_document, línea 78). 2) Pasar los prefijos derived. 3) Contar y resumir. 4) Tests. 5) Prueba en clon limpio e informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_diagnostics.py
- TMPDIR=/dev/shm pytest -q tests/test_serve_stores_check.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos pasan con el test nuevo; en un clon limpio sin build stores check sale con 0 errores de PythonSymbolDoc y una alerta store/generated-missing; el informe lista las alertas de selfdoc check; CHANGELOG y commit.

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

FILE:desk/atoms/atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista.md
---
id: atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista
title: Lo que el código dice de sí mismo se publica con lo que no se pudo probar a
  la vista
five_wh_one_plus: how
tags:
- system:sldb
---

# Lo que el código dice de sí mismo se publica con lo que no se pudo probar a la vista

## Answer

El adaptador de fuente de sldb publica con lo que encontró también lo que no pudo establecer: declaraciones sin metadata (undeclared), declaradas sin explicación (unexplained), referencias sin resolver (unresolved_references), imports bajo condición (context) o sombreados (shadowed_at) y purposes escritos a mano que difieren del docstring (purpose_conflicts). Nada de eso se adivina ni se descarta en silencio, y un escaneo fallido no reemplaza lo publicado. Spec: docs/architecture/code-docstring-indexing.spec.md.

FILE:src/sldb/store/diagnostics.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional

from sldb.store.field_set_drift import document_drifted
from sldb.store.diagnostics_models.text_history import with_history
from sldb.store.layout import project_root as store_project_root
from sldb.store.hashing import hash_documents_index, hash_models_layer, hash_text
from sldb.store.diagnostics_models.invalid_verdict import fields_state
from sldb.store.source_read import read_source_text
from sldb.store.diagnostics_models.unread_verdict import unread_diagnosis
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.legacy_contract import legacy_contract
from sldb.store.model_node import contract_moved
from sldb.store.model_origin import add_owner_import_roots
from sldb.store.models import ModelsIndex
from sldb.store.diagnostics_models import (
    DiagnosisNote,
    DocumentDiagnosis,
    ModelDiagnosis,
    StoreDiagnosis,
)


def _try_resolve_model(
    model_ref: str, pythonpath: Optional[str], resolve_model_ref: Callable
) -> Any:
    try:
        return resolve_model_ref(model_ref, pythonpath)
    except Exception:
        # Layer 4: Don't swallow everything, but for diagnostics we want best-effort
        return None


def _diagnose_doc(doc, root: Path, model_type: Any, contract_ok: bool = True) -> DocumentDiagnosis:
    """Compare the document on disk against what the store recorded for it.

    `content` is the markdown text; `fields` is the payload extracted under the
    model's contract. Text moving while fields hold still is an expected mutation,
    so the two are reported separately rather than as one "mismatch".

    A model that cannot be imported here (`model_type` None) cannot re-extract the fields; an
    intact text then stands for intact fields, instead of reading as a data mutation that sends
    the operator to restore a file nobody touched. The model is named as unresolved.
    """
    doc_path = root / doc.path
    if (unread := unread_diagnosis(doc, root, doc_path)) is not None:
        return unread
    text = read_source_text(doc_path)
    content_on_disk = hash_text(text)
    state = fields_state(model_type, text, doc, content_on_disk)
    if isinstance(state, DocumentDiagnosis):
        return state  # the model rejects the text: nothing else of it is compared (inbox 3895e9f7 H1)
    return _compared(doc, state, content_on_disk, contract_ok)


def _compared(doc, state: tuple[str, dict[str, str], bool], content_on_disk: str, contract_ok: bool) -> DocumentDiagnosis:
    fields_on_disk, map_on_disk, fields_ok = state
    content_ok = content_on_disk == doc.source_hash
    changed = [] if fields_ok else _changed_fields(getattr(doc, "field_hashes", {}) or {}, map_on_disk)
    return DocumentDiagnosis(name=doc.name, path=doc.path, content_ok=content_ok, fields_ok=fields_ok, path_exists=True, note=_note(content_ok, fields_ok, contract_ok), content_on_disk=content_on_disk, content_in_index=doc.source_hash, fields_on_disk=fields_on_disk, fields_in_index=doc.content_hash, changed_fields=changed)


def _changed_fields(in_index: dict[str, str], on_disk: dict[str, str]) -> list[str]:
    """The field names whose hashes disagree, plus those present on only one side.

    Empty when either side has no map: a store written before `field_hashes` cannot be asked
    which field moved, and saying "none" there would read as "nothing changed" when
    `content_hash` already said otherwise.
    """
    if not in_index or not on_disk:
        return []
    return sorted(name for name in set(in_index) | set(on_disk) if in_index.get(name) != on_disk.get(name))


def _note(content_ok: bool, fields_ok: bool, contract_ok: bool) -> DiagnosisNote:
    """Which verdict the two hashes earn — and who to blame when the fields disagree.

    Fields differing while the text stands still is not the document's doing when the model's
    contract moved: the same text extracts to something else now. Blaming the document there
    sent the reader to inspect a file nobody had edited.

    The contract only excuses the document while its TEXT is intact (`content_ok`). A moved
    contract on a file that was also edited is still a data mutation and still needs a human:
    letting the contract absolve it would hide a hand edit behind a safe-to-run verdict.
    """
    if content_ok and fields_ok:
        return DiagnosisNote.OK
    if fields_ok:
        return DiagnosisNote.BENIGN_MUTATION
    return DiagnosisNote.CONTRACT_MUTATION if not contract_ok and content_ok else DiagnosisNote.DATA_MUTATION

def _diagnose_model(model_entry, root, pythonpath, resolve_model_ref: Callable) -> tuple[ModelDiagnosis, ModelsIndex]:
    """The model node, split into the two children that can move it: its document roster and
    its contract. Attributing the node to one of them is the whole point of storing both."""
    models_idx = load_models_index(root / model_entry.models_index)
    docs_idx = load_documents_index(root / models_idx.documents_index)
    model_type = _try_resolve_model(model_entry.model_ref, pythonpath, resolve_model_ref)
    legacy = legacy_contract(models_idx, model_type)
    drifted = any(document_drifted(d, root, model_type) for d in docs_idx.documents)  # see sldb.store.field_set_drift
    contract_ok = (legacy or not contract_moved(models_idx, model_type)) and not drifted
    doc_diagnoses = [_with_history(_diagnose_doc(d, root, model_type, contract_ok), root) for d in docs_idx.documents]
    roster_ok = hash_documents_index(docs_idx) == models_idx.roster_hash
    return ModelDiagnosis(name=models_idx.name, roster_ok=roster_ok, contract_ok=contract_ok, legacy_contract=legacy, resolved=model_type is not None, source_path=models_idx.path, documents=doc_diagnoses), models_idx

def _with_history(doc: DocumentDiagnosis, root: Path) -> DocumentDiagnosis:
    """The text's git history, except for a path sldb would not read (nothing to compare)."""
    return doc if doc.note in (DiagnosisNote.PATH_OUTSIDE_ROOT, DiagnosisNote.SYMLINK_NOT_READ) else with_history(doc, root)


def diagnose_store(store_path: Path, resolve_model_ref: Callable, project_root: Optional[Path] = None, pythonpath: Optional[str] = None) -> StoreDiagnosis:
    """Diagnoses the integrity of the entire store."""
    root = project_root or store_project_root(store_path)
    add_owner_import_roots(store_path)  # inherited models import from their owner
    store_index = load_store_index(store_path)
    diagnoses = [_diagnose_model(m, root, pythonpath, resolve_model_ref) for m in store_index.models]
    model_diagnoses = [d[0] for d in diagnoses]
    loaded_models_indices = [d[1] for d in diagnoses]
    return StoreDiagnosis(root_ok=hash_models_layer(loaded_models_indices) == store_index.hash_a, models=model_diagnoses)

FILE:src/sldb/api/stores/store_check.py
"""Store integrity check: the CLI's `sldb stores check` reached through sldb.api.

The verification itself is ``sldb.store.diagnostics.diagnose_store`` (the exact
function the CLI calls); this module only projects its per-document verdicts into
a compact ``{ok, checked, mismatched}`` summary with the expected/actual hashes
the diagnosis now carries. Nothing here re-checks the store.

``ok`` and ``valid`` are the same verdict, "no error" (anchoring.md §4): what moved is in
``alerts`` and ``mismatched``, what broke in ``errors``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def check_store(store_path: Path, project_root: Path, pythonpath: str | None = None) -> dict[str, Any]:
    """Run the CLI's store integrity check and summarize it."""
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.diagnostics import diagnose_store

    from sldb.api.model_registry.model_reference import same_model_class
    from sldb.store.model_origin import shadowed_models

    diagnosis = diagnose_store(store_path, resolve_model_ref, project_root, pythonpath=pythonpath)
    return {**check_report(diagnosis, structural_noise(store_path, project_root, pythonpath), all_findings(diagnosis, store_path, project_root, pythonpath)), "shadowed_models": shadowed_models(store_path, lambda a, b: same_model_class(a, b, pythonpath)), "broken_links": _broken_links(store_path), "gitignore_policy": _gitignore(store_path), "rewrite_loss": _rewrite_loss(store_path, project_root, pythonpath)}


def all_findings(diagnosis: Any, store_path: Path, project_root: Path, pythonpath: str | None) -> list:
    """The diagnosis' findings and its surroundings', each read through the store's policy
    (`judge_findings`), as `stores check` reports them; then, at their own level, the `on_check`
    rules' and the document anchors' (GO08, `on_check_findings`). A document its model rejects
    is named once, as `store/doc-invalid` (`once_per_invalid`)."""
    from sldb.api.rules.rules_on_check import on_check_findings
    from sldb.api.stores.judge_findings import judged
    from sldb.api.stores.store_findings import diagnosis_findings, once_per_invalid
    from sldb.api.stores.store_surroundings import surroundings_findings

    found = judged(diagnosis_findings(diagnosis) + surroundings_findings(store_path, project_root, pythonpath), store_path, pythonpath)
    return once_per_invalid(found + on_check_findings(store_path, pythonpath), diagnosis)


def _broken_links(store_path: Path) -> list[dict[str, str]]:
    """Links whose target is gone or holds no store (an error, in `errors`)."""
    from sldb.api.stores.store_links import store_links

    return [link for link in store_links(store_path) if link["status"] != "ok"]


def _gitignore(store_path: Path) -> dict[str, bool] | None:
    from sldb.api.stores.gitignore_policy import gitignore_policy

    return gitignore_policy(store_path)


def _rewrite_loss(store_path: Path, project_root: Path, pythonpath: str | None) -> list[dict[str, Any]]:
    from sldb.api.stores.scan_rewrite_loss import scan_rewrite_loss

    return scan_rewrite_loss(store_path, project_root, pythonpath)


def check_report(diagnosis: Any, noise: list[dict[str, Any]], findings: list) -> dict[str, Any]:
    """The compact `{ok, valid, errors, alerts, damaged, ..., checked, mismatched, structural_noise}` view of one diagnosis.

    Args:
        diagnosis: The store diagnosis to project.
        noise: The tracked documents with undeclared headings (see ``structural_noise``).
        findings: Every finding (``all_findings``); ``ok`` and ``valid`` are "none is an error".
    """
    from sldb.core.finding import split

    errors, alerts = split(findings)
    listed = {"valid": not errors, "errors": [f.as_dict() for f in errors], "alerts": [f.as_dict() for f in alerts]}
    return {"ok": not errors, **_classified(diagnosis), **listed, **_summarize(diagnosis), "structural_noise": noise}


def structural_noise(store_path: Path, project_root: Path, pythonpath: str | None) -> list[dict[str, Any]]:
    """Tracked documents with undeclared headings: reported here, refused at write time."""
    from sldb.api.stores.scan_structural_noise import scan_structural_noise

    return [report.details() for report in scan_structural_noise(store_path, project_root, pythonpath)]


def _classified(diagnosis: Any) -> dict[str, Any]:
    """The verdict split by category.

    `mismatched` lists every hash that moved, including the expected ones (text moved,
    fields held still). `damaged` is the documents changed or gone.
    """
    return {
        "damaged": [{"doc": d.name, "model": m, "note": d.note.value, "explain": d.explain()} for m, d in diagnosis.damaged_documents],
        "reformatted": [d.name for _m, d in diagnosis.reformatted_documents],
        "roster_only": [m.name for m in diagnosis.roster_only_models],
        "moved_contracts": [m.name for m in diagnosis.moved_contracts],
    }


def _summarize(diagnosis: Any) -> dict[str, Any]:
    checked = 0
    mismatched: list[dict[str, Any]] = []
    for model in diagnosis.models:
        for doc in model.documents:
            checked += 1
            _collect_mismatches(doc, mismatched)
    return {"checked": checked, "mismatched": mismatched}


# (reported kind, ok flag, value on disk now, value the index recorded)
_KINDS = (
    ("hash_c", "content_ok", "content_on_disk", "content_in_index"),
    ("hash_d", "fields_ok", "fields_on_disk", "fields_in_index"),
)


def _collect_mismatches(doc: Any, mismatched: list[dict[str, Any]]) -> None:
    for kind, ok, expected, actual in _KINDS:
        if not getattr(doc, ok):
            mismatched.append({"doc": doc.name, "expected": getattr(doc, expected), "actual": getattr(doc, actual), "kind": kind})

FILE:tests/store/test_diagnostics.py
from pathlib import Path
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.cli import main as cli_main
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.diagnostics import diagnose_store, DiagnosisNote
from sldb.store.io import load_store_index, load_models_index, save_models_index


class CheckDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Document title.")


_PYTHONPATH = str(Path(__file__).parent.parent.parent / "src")
_MODULE_REF = f"{CheckDoc.__module__}:{CheckDoc.__name__}"


def _make_store(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text("# Hello\n", encoding="utf-8")
    cli_main(["stores", "init", "--path", str(tmp_path)])
    cli_main(
        [
            "models",
            "add",
            _MODULE_REF,
            "--store",
            str(tmp_path / ".sldb"),
            "--pythonpath",
            _PYTHONPATH,
        ]
    )
    cli_main(
        [
            "docs",
            "track",
            str(doc),
            "--model",
            CheckDoc.__name__,
            "--store",
            str(tmp_path / ".sldb"),
            "--pythonpath",
            _PYTHONPATH,
        ]
    )
    return tmp_path


def test_clean_store_is_valid(tmp_path):
    _make_store(tmp_path)
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.is_valid
    assert result.hash_a_ok
    assert result.models[0].documents[0].note == DiagnosisNote.OK


def test_benign_text_mutation(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra paragraph\n", encoding="utf-8")
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.BENIGN_MUTATION
    assert result.is_valid


def test_data_mutation_is_an_alert_not_an_invalid_store(tmp_path):
    """The source moved against the index: valid, to be looked at (anchoring.md §4)."""
    from sldb.api.stores.store_findings import diagnosis_findings

    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.DATA_MUTATION
    assert result.is_valid
    assert [(f.level, f.code) for f in diagnosis_findings(result)] == [("alert", "store/data-mutation")]


def test_missing_document(tmp_path):
    from sldb.api.stores.store_findings import diagnosis_findings

    _make_store(tmp_path)
    (tmp_path / "doc.md").unlink()
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.MISSING
    assert not result.is_valid
    assert ("error", "store/missing") in [(f.level, f.code) for f in diagnosis_findings(result)]


def test_tampered_hash_b(tmp_path):
    _make_store(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    entry = store_index.models[0]
    models_idx = load_models_index(tmp_path / entry.models_index)
    models_idx.roster_hash = "tampered"
    save_models_index(tmp_path / entry.models_index, models_idx)
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert not result.models[0].hash_b_ok
    assert result.is_valid, "a stale roster is an alert, not an invalid store"


# ── semantic names: what each hash signs ─────────────────────────────────────
#
# The letters say where a hash sits in the chain; the names say what it signs.
# `content` is the markdown TEXT (hash_c), `fields` is the EXTRACTED PAYLOAD under
# the model's contract (hash_d). That distinction is the whole basis of the
# verdict, so the names are asserted against observable behaviour, not just
# aliased: a reformat must move content and hold fields still, and a field edit
# must move both.


def test_reformatting_moves_content_and_holds_fields_still(tmp_path):
    """The defining property of an expected mutation, stated in semantic terms."""
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra paragraph\n", encoding="utf-8")
    doc = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH).models[0].documents[0]

    assert not doc.content_ok, "the markdown text changed, so content must not match"
    assert doc.fields_ok, "no field's value changed, so fields must still match"
    assert doc.note == DiagnosisNote.BENIGN_MUTATION
    # the two sides are named for where they were read, not for which is right
    assert doc.content_on_disk != doc.content_in_index
    assert doc.fields_on_disk == doc.fields_in_index


def test_a_field_edit_moves_both_content_and_fields(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    doc = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH).models[0].documents[0]

    assert not doc.content_ok and not doc.fields_ok
    assert doc.note == DiagnosisNote.DATA_MUTATION
    assert doc.fields_on_disk != doc.fields_in_index


def test_letter_names_still_read_the_same_values(tmp_path):
    """hash_c/hash_d are the store's persisted keys; renaming them would invalidate
    every store on disk, so the letter names stay as aliases."""
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra\n", encoding="utf-8")
    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    doc = res.models[0].documents[0]

    assert doc.hash_c_ok is doc.content_ok
    assert doc.hash_d_ok is doc.fields_ok
    assert doc.hash_c_expected == doc.content_on_disk
    assert doc.hash_c_actual == doc.content_in_index
    assert doc.hash_d_expected == doc.fields_on_disk
    assert doc.hash_d_actual == doc.fields_in_index
    assert res.hash_a_ok is res.root_ok
    assert res.models[0].hash_b_ok is res.models[0].roster_ok


# ── the roster verdict: a failure no document can explain ────────────────────


def test_roster_failure_over_absent_documents_names_no_damaged_document(tmp_path):
    """The case that used to be indistinguishable from corruption.

    A model whose documents are absent (deliberately unversioned: a ledger that is
    gitignored, so a clean clone has none of them) fails the roster hash while every
    document present — none — is clean. Reproduces AgentsKBs MoveDoc: `docs=0,
    notes={}`, yet FAIL.

    The roster entry is removed while `hash_b` keeps signing it: that is exactly a
    clone's state, where the index was written by a tree that had the documents.
    """
    _make_store(tmp_path)
    (tmp_path / "doc.md").unlink()
    # The roster is composed from per-document shards, so a clone missing the
    # documents is missing the shards themselves — emptying the list would not
    # reproduce it. `hash_b` keeps signing the document that is no longer there.
    shard = tmp_path / ".sldb" / "core" / "documents" / "CheckDoc" / "doc.yaml"
    assert shard.exists(), "precondition: the document has a shard to remove"
    shard.unlink()
    # `documents_hash.entries_of` caches the composed roster across operations,
    # keyed on hash_b (which we are deliberately leaving stale), so drop it.
    from sldb.store import documents_hash

    documents_hash.invalidate(tmp_path / ".sldb", "CheckDoc")

    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    model = next(m for m in res.models if m.name == "CheckDoc")

    assert model.documents == [], "no document is present to carry a verdict"
    assert not model.roster_ok, "the roster hash still signs the document that left"
    assert model.documents_are_clean, "nothing present is damaged"
    assert model.roster_only_failure, "so the failure is roster-only"
    assert res.damaged_documents == [], "and it must not be reported as damage"
    assert model in res.roster_only_models
    assert res.is_valid, "a stale roster is an alert: classified, reported, and not an error"
    assert "0 documents" in model.explain()


def test_damaged_document_is_not_reported_as_roster_only(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)

    assert len(res.damaged_documents) == 1
    assert res.roster_only_models == [], "a damaged document is damage, not a roster artifact"


def test_reformatted_documents_are_listed_but_keep_the_store_valid(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra\n", encoding="utf-8")
    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)

    assert [d.name for _m, d in res.reformatted_documents] == ["doc"]
    assert res.damaged_documents == []
    assert res.is_valid, "an expected mutation must not fail the store"


# ── the report: every finding says which document and what to do ─────────────


def _check_output(tmp_path, capsys, *extra):
    """Run `stores check`, returning (rc, stdout) with the setup chatter drained."""
    from sldb.cli import main as _main

    capsys.readouterr()  # drop the init/register/track output of _make_store
    args = ["stores", "check", "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH, *extra]
    try:
        rc = _main(args)
    except SystemExit as exc:  # --format json/yaml exits instead of returning
        rc = exc.code
    return rc, capsys.readouterr().out


def test_report_names_the_damaged_document_and_its_fix(tmp_path, capsys):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    rc, out = _check_output(tmp_path, capsys)

    assert rc == 0, "a changed field is an alert"
    assert "PASS: store integrity" in out
    assert "1 damaged" in out
    assert "alert: [store/data-mutation] CheckDoc:doc" in out
    assert "data_mutation: doc" in out, "the document is named, not just counted"
    assert "doc.md" in out, "and so is its path"
    assert "stores update" in out, "the fix is stated in the message"
    assert "content_hash" in out and "on disk" in out and "in index" in out
    # an edited field value is a decision, not something a command should paper over
    assert "decide first" in out
    assert "need a decision" in out


def test_report_distinguishes_reformatting_from_damage(tmp_path, capsys):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra\n", encoding="utf-8")
    rc, out = _check_output(tmp_path, capsys)

    assert rc == 0, "an expected mutation passes"
    assert "PASS: store integrity" in out
    assert "reformatted (ok)" in out
    assert "damaged" not in out


def test_report_explains_a_roster_only_failure_without_blaming_a_document(tmp_path, capsys):
    _make_store(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    models_idx = load_models_index(tmp_path / store_index.models[0].models_index)
    models_idx.roster_hash = "tampered"
    save_models_index(tmp_path / store_index.models[0].models_index, models_idx)
    rc, out = _check_output(tmp_path, capsys)

    assert rc == 0
    assert "roster" in out
    assert "roster-only" in out
    assert "alert: [store/roster-stale] CheckDoc" in out
    # the legend at the bottom defines every category; the findings above it must
    # not accuse any document
    findings = out.split("what the categories mean:")[0]
    assert "data_mutation" not in findings, "no document is damaged, so none is accused"
    assert "all 1 documents present are clean" in findings


def test_quiet_keeps_the_verdict_line_and_never_hides_an_alert(tmp_path, capsys):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    rc, out = _check_output(tmp_path, capsys, "--quiet")

    assert rc == 0
    lines = out.strip().splitlines()
    assert lines[0] == "PASS: store integrity", "scripts pinned to the first line keep working"
    assert any(line.startswith("alert: [store/data-mutation]") for line in lines[1:])


def test_json_carries_both_letter_and_semantic_keys(tmp_path, capsys):
    import json

    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    _rc, out = _check_output(tmp_path, capsys, "--format", "json")
    payload = json.loads(out)
    doc = payload["models"][0]["documents"][0]

    # deskops reads `note`, `path` and the hash_*_ok keys: that shape must survive
    assert doc["note"] == "data_mutation"
    assert doc["hash_c_ok"] is False and doc["hash_d_ok"] is False
    assert doc["content_ok"] is False and doc["fields_ok"] is False
    assert payload["hash_a_ok"] == payload["root_ok"]
    assert payload["damaged"] == 1
    assert "explain" in doc and "stores update" in doc["explain"]

FILE:instruccion
Cold-bundle de la tarea task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/store/test_diagnostics.py
- TMPDIR=/dev/shm pytest -q tests/test_serve_stores_check.py

