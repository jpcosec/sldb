FILE:desk/tasks/task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto.md
---
sldb:
  by: agent
  at: '2026-11-16T06:19:51Z'
  authority: generated
  via: create_document
id: task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-004642-suggestion-sldb-notations-atoms-dir-no-manda-el-resolver-trae-tomos-de-un-store-ajeno-heredado-de-spec2viz-que-se-retira.md
depends_on: []
pills: []
files:
- src/sldb/api/matching/atoms_by_view.py
- tests/matching/test_matching_refs.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# raw_atoms_by_view: si se pasa atoms_dir, ese directorio manda para todas las vistas y nunca entran átomos de un store ajeno

## Rationale

_Explain why this task exists or the business driver behind it._

raw_atoms_by_view (src/sldb/api/matching/atoms_by_view.py) toma primero reader.atoms(view.store) de cada vista y solo usa atoms_dir como respaldo para las vistas vacías. Corrido desde labchile_chatbots/docs/spec2viz con --atoms-dir ../../desk/atoms, el store que se descubre era el de deskops y entraron 146 átomos ajenos en vez de los 3 del repo. specir catalog build la llama (repo IR). Heredado de spec2viz, que se retira. Origen: desk/inbox/20261116-004642-suggestion-sldb-notations-atoms-dir-no-manda-el-resolver-trae-tomos-de-un-store-ajeno-heredado-de-spec2viz-que-se-retira.md.

## Goal

_Describe the concrete result this task must produce._

raw_atoms_by_view(views, atoms_dir=d) devuelve para todas las vistas los átomos de d y no consulta ningún store; sin atoms_dir, el comportamiento es el de hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: en raw_atoms_by_view, si atoms_dir es truthy, armar atoms_by_view solo desde parse_atoms(atoms_dir, findings) para todas las vistas, sin llamar reader.atoms; docstring actualizada. Test nuevo en tests/matching/test_matching_refs.py: dos vistas, una con store que tiene átomos y otra sin store, más un atoms_dir con un átomo distinto; con atoms_dir las dos vistas traen solo el átomo del directorio; sin atoms_dir, la vista con store trae los del store. CHANGELOG.md. No entra: cambiar cómo se descubre el store de una vista sin atoms_dir.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer atoms_by_view.py y los tests de tests/matching/ que la usan (grep -rn raw_atoms_by_view tests). 2) Cambiar la rama de atoms_dir. 3) Test. 4) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/

## Done When

_Name the observable condition that makes the task complete._

tests/matching/ pasa con el test nuevo; CHANGELOG y commit; aviso a IR con deskops message send --to IR (si no está registrado, línea "Aviso a IR" en result-summary.md).

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

FILE:src/sldb/api/matching/atoms_by_view.py
"""Los átomos de cada vista: los `AtomDoc` del store de la vista, o los de una carpeta de respaldo.

Migrado de `spec2viz.deskops` (`build_atoms_by_view`, `_raw_atoms_by_view`), sobre `SpecView`
y `StoreReader`.
"""

from __future__ import annotations

import json
from pathlib import Path

from sldb.api.matching.atom_payload import parse_atoms
from sldb.api.matching.atom_tags import filter_atoms_payload
from sldb.api.matching.spec_view import SpecView
from sldb.api.matching.store_reader import StoreReader
from sldb.core.finding import Finding


def raw_atoms_by_view(
    views: list[SpecView], atoms_dir: Path | None = None, reader: StoreReader | None = None
) -> tuple[dict[str, dict[str, dict]], list[Finding]]:
    """`vista -> payload` del store de cada vista; las vistas sin átomos toman los de `atoms_dir`."""
    reader = reader or StoreReader()
    atoms_by_view = {view.key: reader.atoms(view.store) if view.store is not None else {} for view in views}
    findings: list[Finding] = []
    if atoms_dir:
        fallback = json.loads(parse_atoms(atoms_dir, findings))
        atoms_by_view.update({view.key: fallback for view in views if not atoms_by_view.get(view.key)})
    return atoms_by_view, [*reader.findings, *findings]


def build_atoms_by_view(
    views: list[SpecView], atoms_dir: Path | None = None, atoms_tags: list[str] | None = None, reader: StoreReader | None = None
) -> tuple[dict[str, dict[str, dict]], list[Finding]]:
    """`raw_atoms_by_view` filtrado por `atoms_tags` (sin tags no filtra)."""
    atoms_by_view, findings = raw_atoms_by_view(views, atoms_dir, reader)
    if atoms_tags:
        atoms_by_view = {k: filter_atoms_payload(v, atoms_tags) for k, v in atoms_by_view.items()}
    return atoms_by_view, findings

FILE:tests/matching/test_matching_refs.py
"""`refs: [Model:name]` por elemento del spec -> referencias a documentos sldb, y aristas de átomos.

Portado de spec2viz (`tests/test_refs.py`, y `test_build_atoms_by_view_uses_store_scoped_payload`
de `tests/test_deskops.py`) contra `sldb.api.matching`. Donde spec2viz falseaba el store con
monkeypatch, aquí hay un store sldb real en el tmp de la prueba (conftest); por eso las aristas
de `TaskDoc:task-x` ya no son vacías: su campo `about` apunta a `AtomDoc:atom-y`.
No se portan los de modelos y schema (tarea de modelos de spec), los de la CLI del catálogo
(HTML, se quedan en spec2viz) ni el descubrimiento del store (la vista trae su `store`).
"""
from pathlib import Path

import pytest

import sldb.api
from sldb.api.matching import (
    STRUCTURAL_RELATIONS, SpecView, StoreReader, UnknownAtomError, attach_atom_edges, build_atoms_by_view, build_explicit_atoms,
    build_explicit_refs, collect_explicit_refs, store_documents,
)


def _view(store, refs=None, atoms=None):
    nodes = {"cli": {"label": "CLI", **({"refs": refs} if refs else {}), **({"atoms": atoms} if atoms else {})}, "core": {"label": "Core"}}
    spec = {"id": "arq", "title": "Arq", "type": "component", "version": "1.0", "data": {"nodes": nodes, "edges": []}}
    return SpecView(key="v1", id="v1", specs=[spec], store=store)


IN_FROM_TASK = {"relation": "references", "direction": "in", "node": "sldb://document/TaskDoc:task-x", "ref": "TaskDoc:task-x", "title": "Tarea X"}
OUT_TO_ATOM = {"relation": "references", "direction": "out", "node": "sldb://document/AtomDoc:atom-y", "ref": "AtomDoc:atom-y", "title": "Atomo Y"}


def test_collect_explicit_refs_indexes_by_label_and_id():
    assert collect_explicit_refs(_view(None, ["TaskDoc:task-x"])) == {"cli": ["TaskDoc:task-x"]}


def test_build_resolves_refs_with_title_path_and_summary(matching_store):
    payload, findings = build_explicit_refs([_view(matching_store, ["TaskDoc:task-x", "AtomDoc:atom-y"])])
    assert findings == []
    refs = payload["v1"]["cli"]
    assert [r["ref"] for r in refs] == ["TaskDoc:task-x", "AtomDoc:atom-y"]
    assert refs[0] == {
        "ref": "TaskDoc:task-x", "model": "TaskDoc", "name": "task-x", "title": "Tarea X",
        "path": str(matching_store.parent / "desk/tasks/task-x.md"), "store": str(matching_store), "summary": "Resumen de X",
        "edges": [OUT_TO_ATOM],
    }
    assert refs[1]["summary"] == "Respuesta Y"
    assert refs[1]["edges"] == [IN_FROM_TASK]


def test_unknown_ref_is_warning_unless_strict(matching_store):
    payload, findings = build_explicit_refs([_view(matching_store, ["TaskDoc:no-existe"])])
    assert payload == {}
    assert [(f.level, f.code) for f in findings] == [("warning", "matching/unknown-ref")]
    assert "no-existe" in findings[0].what
    with pytest.raises(UnknownAtomError) as raised:
        build_explicit_refs([_view(matching_store, ["TaskDoc:no-existe"])], strict=True)
    assert "no-existe" in str(raised.value)


def test_view_without_store_warns_per_ref():
    result, findings = build_explicit_refs([_view(None, ["TaskDoc:task-x"])])
    assert result == {}
    assert len(findings) == 1 and findings[0].code == "matching/no-store" and "sin store" in findings[0].what


def test_edges_of_keeps_declared_edges_both_ways_and_drops_structural(matching_store):
    raw = {e.relation for e in [*sldb.api.edges_from(matching_store, "AtomDoc:atom-y"), *sldb.api.edges_to(matching_store, "AtomDoc:atom-y")]}
    assert raw & STRUCTURAL_RELATIONS  # el indice si las tiene
    reader = StoreReader()
    edges = reader.edges_of(matching_store, "AtomDoc:atom-y")
    assert edges == [IN_FROM_TASK]
    assert reader.edges_of(matching_store, "AtomDoc:atom-y") is edges  # cache
    assert reader.findings == []


def test_edges_of_without_edge_index_warns_once_and_is_empty(tmp_path):
    reader = StoreReader()
    assert reader.edges_of(tmp_path / ".sldb", "AtomDoc:a") == []
    assert reader.edges_of(tmp_path / ".sldb", "AtomDoc:b") == []
    assert [f.code for f in reader.findings].count("matching/edges-unavailable") == 1


def test_edges_of_against_a_real_store(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    sldb.api.init_store(project)
    sldb.api.init_relations(project / ".sldb")
    sldb.api.rebuild_edges(project / ".sldb")
    reader = StoreReader()
    # la relacion builtin `references` existe como documento, sin aristas declaradas: lista vacia, sin findings
    assert reader.edges_of(project / ".sldb", "RelationTypeDoc:references") == []
    assert reader.findings == []


def test_build_attaches_edges_to_explicit_atoms(matching_store):
    views = [_view(matching_store, atoms=["atom-y"])]
    reader = StoreReader()
    raw, _ = build_atoms_by_view(views, reader=reader)
    explicit, _complete, _findings, linked = build_explicit_atoms(views, raw)
    attach_atom_edges(views, explicit, linked, reader, raw)
    atom = explicit["v1"]["cli"]["list"][0]
    assert atom["id"] == "atom-y" and atom["edges"] == [IN_FROM_TASK]


def test_store_documents_come_from_sldb_api(tmp_path, store_factory):
    atom = {"name": "atom-a", "id": "atom-a", "title": "Alpha", "five_wh_one_plus": "what", "tags": ["x:y"], "answer": "Cuerpo"}
    store = store_factory(tmp_path / "proj", [atom], [])
    other = store_factory(tmp_path / "other", [], [{"name": "task-b", "title": "Beta"}])
    sldb.api.link_store(store, other, "desk")

    docs = {d["ref"]: d for d in store_documents(store)}
    assert {"AtomDoc:atom-a", "desk:TaskDoc:task-b"} <= set(docs)
    assert docs["AtomDoc:atom-a"]["path"] == str(tmp_path / "proj/desk/atoms/atom-a.md")
    assert docs["desk:TaskDoc:task-b"]["path"] == str(tmp_path / "other/desk/tasks/task-b.md")

    reader = StoreReader()
    payload = reader.atoms(store)
    assert list(payload) == ["alpha"]
    assert payload["alpha"]["atoms"]["what"]["id"] == "atom-a"
    assert payload["alpha"]["atoms"]["what"]["tags"] == ["x:y"]
    assert reader.resolve_ref(store, "desk:TaskDoc:task-b")["title"] == "Beta"
    assert reader.resolve_ref(store, "TaskDoc:nope") is None


def test_build_atoms_by_view_uses_store_scoped_payload(matching_store):
    atoms_by_view, findings = build_atoms_by_view([SpecView(key="view-1", id="view-1", store=matching_store)])
    assert findings == []
    assert list(atoms_by_view) == ["view-1"]
    entry = atoms_by_view["view-1"]["atomo y"]
    assert entry["title"] == "Atomo Y" and "atomo" in entry["aliases"] and "oc" in entry["aliases"]
    assert entry["atoms"]["what"]["id"] == "atom-y" and entry["atoms"]["what"]["body"] == "Respuesta Y"

FILE:instruccion
Cold-bundle de la tarea task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/matching/

