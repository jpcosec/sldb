FILE:desk/tasks/task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg.md
---
sldb:
  by: agent
  at: '2026-11-16T05:34:12Z'
  authority: generated
  via: save_document_payload
id: task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md
depends_on: []
pills: []
files:
- src/sldb/api/matching/store_reader.py
- src/sldb/api/matching/store_edges.py
- src/sldb/store/edge_index/composed_reading.py
- tests/matching/test_matching_refs.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector
---

# matching: attach_atom_edges deja de recomponer live-stale y los mapas del índice federado en cada edges_of (catalog build con átomos en minutos)

## Rationale

_Explain why this task exists or the business driver behind it._

IR13 midió que `specir catalog build --config <project.yml de ejemplo del catálogo en las fixtures visuales del repo IR>` (repo IR) no termina en 300 s; el tiempo es de sldb. cProfile: 146 de 149 s en sldb.api.matching.attach_atom_edges -> StoreReader.edges_of (31 llamadas) -> store_edges.edges_of -> edges_from + edges_to -> load_edge_index (62 llamadas, ~1,1 s cada una). compose_edge_index acierta la caché _COMPOSED, pero with_live_stale corre stale_of_facts en cada llamada y el model_copy resultante reconstruye los mapas (_ensure_maps). Origen: desk/inbox/20261115-224941-suggestion-matching-edges-catalog-build-con-tomos-tarda-minutos-porque-cada-edges-of-recompone-live-stale-y-mapas-del-ndice-federado.md.

## Goal

_Describe the concrete result this task must produce._

attach_atom_edges sobre N referencias carga el índice de aristas una sola vez por store y no recalcula live-stale ni los mapas por cada referencia; el catalog build de IR de la nota termina en menos de 60 s con el mismo resultado.

## Scope

_State what is in scope and what is out of scope._

Entra, en este orden: (1) reproducir con un test de rendimiento acotado en tests/matching/ que cuenta llamadas (monkeypatch de load_edge_index o de stale_of_facts con un contador) para 10 referencias sobre un store de prueba y falla si load_edge_index se llama más de 2 veces; (2) arreglar en src/sldb/api/matching/store_reader.py (StoreReader, líneas 45-57) para que cargue el índice una vez por store y resuelva edges_from y edges_to de cada referencia sobre ese índice ya cargado, en lugar de llamar store_edges.edges_of por referencia; (3) solo si (2) no basta para la meta, memoizar with_live_stale en src/sldb/store/edge_index/composed_reading.py (líneas 43-47) por firma de shards y stats de fuentes. Medición antes y después con el comando de IR de la nota (cd al repo IR, timeout 300) y guardada en el informe del ejecutor. CHANGELOG.md. No entra: cambiar la semántica de stale (sigue reportando las ediciones externas), tocar compose.py salvo que (3) lo exija, ni la configuración de federación del store de IR (la doble federación deskops/sldb de SLDB_1 y ~/herramientas es configuración de IR, no código de sldb).

Precisiones (preflight-1): la meta es una carga por store y por llamada a attach_atom_edges; el test admite 2 porque edges_from y edges_to pueden necesitar el índice con y sin enlaces. Si se llega al paso (3), la clave de la memoización es (store_path, shards_signature(store_path), tupla ordenada de (ruta, mtime_ns, tamaño) de los archivos trackeados) y la caché vive en el proceso. "Mismo resultado" es igualdad de las aristas devueltas por attach_atom_edges antes y después, comparadas como conjuntos en el test. El comando de la nota es `cd /mnt/ssd/proyectos/SLDB_1/IR && timeout 300 specir catalog build --config <ruta del project.yml de ejemplo que cita la nota>`; la ruta exacta se copia de la nota de origen (references). El store de prueba del test contador se arma como en tests/matching/test_matching_refs.py.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/matching/store_reader.py, src/sldb/api/matching/store_edges.py (línea 28), src/sldb/api/edges/edge_reading.py (edges_from línea 45, edges_to línea 61), src/sldb/store/edge_index/compose.py (línea 48), composed_reading.py (43-47) y edge_index.py (_ensure_maps, línea 43). 2) Test contador que falla hoy. 3) Cambio en StoreReader. 4) Medir; si no alcanza, memoización del paso (3). 5) Correr los tests de Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/store/test_live_stale_security.py

## Done When

_Name the observable condition that makes the task complete._

El test contador pasa (load_edge_index a lo sumo 2 veces para 10 referencias); los tres comandos de Validation pasan; la medición del catalog build de IR antes/después queda en el informe con el después bajo 60 s; commit.

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

FILE:desk/atoms/atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector.md
---
id: atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector
title: 'Un escaneo por documento se cachea por lo que lo determina: texto, contrato
  y lector'
five_wh_one_plus: how
tags:
- system:sldb
- topic:performance
provenance: src/sldb/api/stores/scan_cache.py
---

# Un escaneo por documento se cachea por lo que lo determina: texto, contrato y lector

## Answer

Lo que stores check deriva de cada documento (si una reescritura perdería contenido, si trae headings no declarados) depende solo de su texto, del contrato de su modelo y del código de sldb que lo lee. Con esos tres como clave, en el caché del usuario y nunca dentro del store, un store sin cambios no se re-renderiza (src/sldb/api/stores/scan_cache.py). La huella del lector incluye el código, no solo la versión: en un checkout de desarrollo la versión no cambia cuando se arregla el extractor.

FILE:src/sldb/api/matching/store_reader.py
"""`StoreReader`: lectura de los stores de las vistas con caché por store y avisos como findings.

Lo que queda de `spec2viz.deskops.SldbAtomResolver` sin el descubrimiento del store: documentos,
átomos y aristas por store, leídos una vez. Un store ilegible o sin índice de aristas deja un
finding una sola vez y sigue con vacío.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.matching.atom_payload import atoms_from_documents
from sldb.api.matching.matching_findings import finding
from sldb.api.matching.store_documents import resolve_ref, store_documents
from sldb.api.matching.store_edges import edges_of
from sldb.core.finding import Finding


class StoreReader:
    """Documentos, átomos y aristas de los stores de las vistas, con caché y findings."""

    def __init__(self, pythonpath: str | None = None):
        self.pythonpath = pythonpath
        self.findings: list[Finding] = []
        self._docs: dict[str, list[dict]] = {}
        self._edges: dict[tuple[str, str], list[dict]] = {}
        self._no_edges: set[str] = set()

    def documents(self, store_path: Path) -> list[dict]:
        key = str(Path(store_path).resolve())
        if key not in self._docs:
            try:
                self._docs[key] = store_documents(Path(key), self.pythonpath)
            except Exception as exc:
                self._docs[key] = []
                self.findings.append(finding("store-unreadable", key, f"Failed to load documents through SLDB: {exc}", "revisar el store con sldb stores check"))
        return self._docs[key]

    def atoms(self, store_path: Path) -> dict[str, dict]:
        return atoms_from_documents(self.documents(store_path))

    def resolve_ref(self, store_path: Path, ref: str) -> dict | None:
        return resolve_ref(self.documents(store_path), ref)

    def edges_of(self, store_path: Path, ref: str) -> list[dict]:
        key = str(Path(store_path).resolve())
        if (key, ref) not in self._edges:
            self._edges[(key, ref)] = [] if key in self._no_edges else self._read_edges(key, ref)
        return self._edges[(key, ref)]

    def _read_edges(self, key: str, ref: str) -> list[dict]:
        try:
            return edges_of(Path(key), ref, {doc["ref"]: doc["title"] for doc in self.documents(Path(key))})
        except Exception as exc:
            self._no_edges.add(key)
            self.findings.append(finding("edges-unavailable", key, f"Edge index unavailable through SLDB, relations left out: {exc}", "sldb edges rebuild"))
            return []

FILE:src/sldb/api/matching/store_edges.py
"""Las aristas declaradas de un documento, en ambos sentidos, sobre `edges_from`/`edges_to` de sldb.api.

Migrado de `spec2viz.deskops.SldbAtomResolver.edges_of`. Las relaciones que el índice de aristas
fabrica solo de la estructura (secciones, tags, campos, modelos) no las declaró nadie y se omiten.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.edge_reading import edges_from, edges_to

STRUCTURAL_RELATIONS = frozenset(
    {
        "has_section", "tagged_as", "has_document", "has_field", "has_model", "names",
        "semantic_parent", "semantic_equivalent", "applies_to_source", "applies_to_target",
    }
)
_DOC_NODE_PREFIX = "sldb://document/"


def _edge(record, direction: str, titles: dict[str, str]) -> dict:
    other = str(record.target if direction == "out" else record.source)
    other_ref = other[len(_DOC_NODE_PREFIX):] if other.startswith(_DOC_NODE_PREFIX) else ""
    return {"relation": str(record.relation), "direction": direction, "node": other, "ref": other_ref, "title": titles.get(other_ref, other_ref or other)}


def edges_of(store_path: Path, ref: str, titles: dict[str, str]) -> list[dict]:
    """`relation`, `direction` (`out`/`in`), `node`, `ref` (`Model:name` o vacío) y `title` de
    cada arista declarada que toca `ref`. Sin índice de aristas, lanza lo que lance sldb."""
    return [
        _edge(record, direction, titles)
        for direction, records in (("out", edges_from(store_path, ref)), ("in", edges_to(store_path, ref)))
        for record in records
        if record.relation not in STRUCTURAL_RELATIONS
    ]

FILE:src/sldb/store/edge_index/composed_reading.py
"""How `compose_edge_index` gets its index in a process that has none (H11): the one an earlier
process kept on disk (`composed_disk`), else composed from the shards and kept; and the
documents a file edited from outside left stale, checked on every read."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from sldb.store.edge_index.composed_disk import disk_key, load_composed, save_composed
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.live_stale import ModelTypeOf, live_facts, stale_of_facts

Stores = list[tuple[Path, str | None]]


def read_or_compose(stores: Stores, include_linked: bool, exclude_tags: frozenset[str], model_type_of: ModelTypeOf | None, compose: Callable) -> tuple[EdgeIndex, list]:
    """(index, each store's `live_facts`): as an earlier process composed it from these very
    shards, else composed now by `compose(stores, exclude_tags, model_type_of)` and kept."""
    key = disk_key(stores, include_linked, exclude_tags, model_type_of)
    found = load_composed(stores[0][0], key)
    if found is not None:
        mark_stale_dirty(found[0].stale, stores)
        return found
    found = (compose(stores, exclude_tags, model_type_of), [live_facts(path) for path, _ in stores])
    save_composed(stores[0][0], key, *found)
    return found


def mark_stale_dirty(stale: list[str], stores: Stores) -> None:
    """What reading the shards does for a stale document, done again for an index read from disk:
    the document enters the dirty set, so the next rebuild compares it."""
    from sldb.store import documents_dirty

    by_name = {name: path for path, name in stores}
    for export_id in stale:
        parts = export_id.split(":")
        link = parts[0] if len(parts) == 3 else None
        if link in by_name:
            documents_dirty.mark(by_name[link], parts[-2], parts[-1])


def with_live_stale(index: EdgeIndex, stores: Stores, facts: list, model_type_of: ModelTypeOf | None) -> EdgeIndex:
    moved = [f"{name}:{e}" if name else e for (path, name), f in zip(stores, facts) for e in stale_of_facts(path, f, model_type_of)]
    known = set(index.stale)
    extra = [e for e in dict.fromkeys(moved) if e not in known]
    return index.model_copy(update={"stale": index.stale + extra}) if extra else index

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
Cold-bundle de la tarea task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/matching/
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/store/test_live_stale_security.py

