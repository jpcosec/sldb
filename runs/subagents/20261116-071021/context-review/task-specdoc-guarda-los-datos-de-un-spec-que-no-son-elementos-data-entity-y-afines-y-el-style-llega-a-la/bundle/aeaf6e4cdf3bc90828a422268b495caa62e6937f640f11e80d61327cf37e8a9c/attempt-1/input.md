FILE:desk/tasks/task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos-data-entity-y-afines-y-el-style-llega-a-la.md
---
sldb:
  by: agent
  at: '2026-11-16T06:08:08Z'
  authority: generated
  via: save_document_payload
id: task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos-data-entity-y-afines-y-el-style-llega-a-la
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-193320-suggestion-ir-pide-exportar-desde-sldb-api-notations-los-modelos-de-spec-de-d3-y-guardar-style-y-entity-en-specdoc.md
depends_on: []
pills: []
files:
- src/sldb/models/notation/spec_doc.py
- src/sldb/api/notations/spec_sync_docs.py
- tests/notations/test_spec_sync.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill
---

# SpecDoc guarda los datos de un spec que no son elementos (data.entity y afines) y el style llega a la vista resuelta

## Rationale

_Explain why this task exists or the business driver behind it._

IR11 (specIR, compiladores y proyecciones migrados de spec2viz) necesita que el SpecDoc sincronizado conserve lo que el spec YAML declara además de elementos y aristas. SpecDoc ya guarda style (src/sldb/models/notation/spec_doc.py, campo style) y la sincronización lo escribe (src/sldb/api/notations/spec_sync_docs.py), pero no hay campo para data.entity ni otros datos del spec, así que se pierden al pasar por el store. Origen (pedido 2): desk/inbox/20261115-193320-suggestion-ir-pide-exportar-desde-sldb-api-notations-los-modelos-de-spec-de-d3-y-guardar-style-y-entity-en-specdoc.md.

## Goal

_Describe the concrete result this task must produce._

Sincronizar un spec con data.entity (y cualquier otra clave de data que no sea elementos) y leerlo de vuelta con el SpecDoc devuelve esos datos sin pérdida, y la vista resuelta de ese SpecDoc incluye su style.

## Scope

_State what is in scope and what is out of scope._

Entra: leer primero la nota de origen completa para fijar qué claves de data pide IR11; agregar a SpecDoc un campo opcional data: dict[str, Any] = {} (vacío por defecto) que guarda las claves de data que no son elementos, con render y extract reversibles en la plantilla del modelo; escribirlo en spec_sync_docs.py; comprobar con un test que resolve_view (sldb.api.notations) pasa style a la vista resuelta y, si no lo hace, pasarlo. Tests en tests/notations/test_spec_sync.py (round trip de data.entity) y tests/notations/test_spec_loader.py si hace falta. Los SpecDoc existentes siguen validando (el campo nuevo es opcional); correr sldb stores build --check. CHANGELOG.md. No entra: reexportar clases (tarea de exports de sldb.api.notations), cambiar el formato YAML de los specs, ni migrar SpecDoc del modelo local docs.models:SpecDoc (tarea de decisión aparte).

Precisiones (preflight-1): lo que pide IR11 (pedido 2 de la nota): que SpecDoc guarde, además de style, el data.entity del spec. "Elementos" son las claves de data que ya se sincronizan hoy como nodos y aristas (nodes, edges y las que spec_sync_docs.py ya mapea); toda otra clave de data se guarda en el campo nuevo. El campo es data: dict[str, Any] = Field(default_factory=dict), con un marcador de bloque YAML en la plantilla del modelo igual al que use style en spec_doc.py (copiar su forma). Para style en la vista resuelta, el test comprueba que la vista que devuelve resolve_view para ese SpecDoc tiene una clave style igual al style del SpecDoc. tests/notations/test_spec_loader.py no se toca salvo que un test existente falle por el cambio.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer la nota de origen, src/sldb/models/notation/spec_doc.py (campo style cerca de la línea 58 y la plantilla), src/sldb/api/notations/spec_sync_docs.py (línea 67) y el resolvedor de vistas en sldb.api.notations. 2) Agregar el campo y su marcador en la plantilla. 3) Escribirlo en la sincronización. 4) Test de round trip y test de style en la vista resuelta. 5) sldb stores build --check sobre el store del repo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_spec_sync.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_spec_catalog_sync.py
- TMPDIR=/dev/shm sldb stores build --check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

Un spec con data.entity sincronizado y releído conserva entity; la vista resuelta trae style; los tests y stores build --check pasan; CHANGELOG y commit.

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

FILE:desk/atoms/atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill.md
---
id: atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill
title: El contrato completo de un modelo se declara y edita por drafts con validacion
  y backfill
five_wh_one_plus: how
tags:
- system:sldb
- topic:models
- topic:drafts
provenance: docs/architecture/model-authoring.md
---

# El contrato completo de un modelo se declara y edita por drafts con validacion y backfill

## Answer

create_model acepta containment, references, compositions, semantics y authority y genera las asignaciones de clase; describe_model los devuelve junto con template y has_draft; edit_model_metadata inserta o reemplaza esas asignaciones en el .draft.py por AST y sincroniza las secciones render del template; validate_model_draft rechaza campos inexistentes en containment o references y composiciones sin source_field con SLDBModelEditError; promote_model_draft(backfill=True) reescribe los documentos afectados y actualiza indice semantico y de aristas. Expuesto en sldb models create | metadata | validate --backfill y en POST /models/create, /models/metadata-edit y /models/promote. Decidido en SV04 (SV-D5), integrado en 6b80df36 y 6ba8bb20.

FILE:src/sldb/models/notation/spec_doc.py
"""`SpecDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field, field_validator
from sldb.models.structured_doc import StructuredNLDoc


class SpecDoc(StructuredNLDoc):
    """Un spec de diagrama, como documento del store que contiene a sus nodos."""

    __semantics__ = {
        "type": ["architecture", "spec"],
        "layer": ["topology"],
        "system": ["spec2viz"],
    }
    # `references`, no `contains`: la relacion builtin `contains` es one_to_many y un nodo
    # anidado en otro ya tiene a ese otro como contenedor.
    __references__ = ["nodes", "notation"]
    __template__ = """---
id: ⸢rev•id⸥
diagram_type: ⸢rev•diagram_type⸥
version: ⸢rev•version⸥
spec_path: ⸢rev•spec_path⸥
sha256: ⸢rev•sha256⸥
notation: ⸢optrev•notation⸥
category: ⸢optrev•category⸥
nav: ⸢optrev•nav⸥
summary: ⸢optrev•summary⸥
style: ⸢optrev•style⸥
nodes: ⸢rev,list•nodes⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="Id del spec (`id:` del YAML); nombre del documento.")
    title: str = Field(description="Titulo del spec, mostrado como H1.")
    diagram_type: str = Field(description="Tipo de diagrama del spec (component, sequence, state...).")
    version: str = Field(description="Version declarada en el spec.")
    spec_path: str = Field(description="Ruta del YAML relativa a la raiz del proyecto del store.")
    sha256: str = Field(description="SHA-256 del YAML en el momento de la sincronizacion.")
    nodes: list[str] = Field(
        default_factory=list,
        description="Ids `SpecNodeDoc:<spec>.<elemento>` de los nodos del spec; el indice los convierte en aristas `references`.",
    )
    notation: str = Field(
        default="",
        description="Id `NotationDoc:<name>` de la notacion con la que se dibuja el spec; vacio si no se asigno ninguna.",
    )
    category: str = Field(default="", description="Categoria del catalogo (`category` de vistas.yml); graph_ui agrupa los specs por ella.")
    nav: str = Field(default="", description="Rotulo corto de navegacion del catalogo (`nav` de vistas.yml).")
    summary: str = Field(default="", description="Resumen del catalogo (`desc` de vistas.yml).")
    style: dict | None = Field(
        default=None,
        description="`style.kinds` neutral del spec (kind -> fill, stroke, icon): segundo nivel de la precedencia de estilo (glifo > spec > paleta); ausente si el spec no lo declara.",
    )
    description: str = Field(default="", description="Descripcion del spec (`metadata.description` del YAML).")

    @field_validator("notation", "category", "nav", "summary", mode="before")
    @classmethod
    def _absent_text(cls, value):
        # un documento escrito antes de que el campo existiera se extrae como None
        return "" if value is None else value

FILE:src/sldb/api/notations/spec_sync_docs.py
"""Los `SpecNodeDoc` y el `SpecDoc` de un spec sincronizado.

Migrado del cuerpo de `spec2viz.sldb_sync.SpecSync.sync` (nodos y el spec).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from sldb.api.notations.spec_refs import node_ref, spec_style_kinds
from sldb.api.notations.sync_report import SyncReport

_CATALOG_KEYS = ("category", "nav", "summary")


def node_payload(spec_id: str, el: dict) -> dict[str, Any]:
    """El payload del `SpecNodeDoc` de un elemento."""
    return {
        "id": f"{spec_id}.{el['id']}", "title": el["label"], "spec": f"SpecDoc:{spec_id}", "element": el["id"], "kind": el["kind"],
        "collection": el["collection"], "refs": el["refs"], "atom_refs": [f"AtomDoc:{a}" for a in el["atoms"]],
        "contains": [node_ref(spec_id, c) for c in el["contains"]], "data": el["data"], "description": el["description"],
    }


def upsert_nodes(writer: Any, existing: dict, report: SyncReport, spec_id: str, elements: list[dict], out: Path) -> set[tuple[str, str]]:
    """Upsert de un `SpecNodeDoc` por elemento; devuelve sus claves `(modelo, nombre)`."""
    for el in elements:
        payload = node_payload(spec_id, el)
        writer.upsert(existing, report, "SpecNodeDoc", payload["id"], out / "nodes" / f"{payload['id']}.md", payload)
    return {("SpecNodeDoc", f"{spec_id}.{el['id']}") for el in elements}


def kept_catalog(existing: dict, spec_id: str, catalog: dict[str, str] | None) -> dict[str, str] | None:
    """Sin catalogo (sync de un spec), el SpecDoc conserva la categoria, la nav y el resumen que le
    dio el sync del catalogo en vez de borrarlos."""
    if catalog is None and ("SpecDoc", spec_id) in existing:
        previous = existing[("SpecDoc", spec_id)].payload
        return {k: previous.get(k) or "" for k in _CATALOG_KEYS}
    return catalog


def _relative(spec_path: Path, root: Path) -> str:
    try:
        return str(spec_path.relative_to(root))
    except ValueError:
        return str(spec_path)


def _spec_head(spec: dict, spec_id: str, spec_path: Path, root: Path, text: str) -> dict[str, Any]:
    """Identidad del `SpecDoc`: id, titulo, tipo, version, ruta y hash del YAML."""
    return {
        "id": spec_id, "title": str(spec.get("title") or spec_id), "diagram_type": str(spec.get("type") or ""),
        "version": str(spec.get("version") or ""), "spec_path": _relative(spec_path, root),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def upsert_spec_doc(writer: Any, existing: dict, report: SyncReport, source: tuple, catalog: dict | None, elements: list[dict]) -> None:
    """Upsert del `SpecDoc`; `source` es `(spec_path, text, spec, out)`."""
    spec_path, text, spec, out = source
    spec_id = report.spec_id
    catalog = kept_catalog(existing, spec_id, catalog) or {}
    payload = {
        **_spec_head(spec, spec_id, spec_path, writer.root, text), "notation": report.notation,
        **{k: str(catalog.get(k) or "") for k in _CATALOG_KEYS}, "style": spec_style_kinds(spec) or None,
        "nodes": [node_ref(spec_id, el["id"]) for el in elements], "description": str((spec.get("metadata") or {}).get("description") or ""),
    }
    writer.upsert(existing, report, "SpecDoc", spec_id, out / f"{spec_id}.md", payload)

FILE:tests/notations/test_spec_sync.py
"""`SpecSync`: el spec como namespace sobre el store sldb (SpecDoc, SpecNodeDoc, RelationDoc).

Portado de spec2viz `tests/test_sldb_sync.py` con el minimo cambio: imports de
`sldb.api.notations`, la CLI click `spec2viz diagram sync` pasa a `sldb notations sync --spec`,
el spec invalido se valida con `validate=load_spec` (el cargador de sldb, D3), el desajuste de
notacion es `NotationMismatchError` de sldb y la parte de `SldbAtomResolver.edges_of` (superficie
de spec2viz, no migrada) se comprueba con `edges_to` de sldb.
"""
from pathlib import Path

import pytest
import yaml

import sldb.api as sldb_api
from sldb.api.notations import SpecSync, catalog_entries, edge_name, find_store, load_spec, relation_token, spec_edges, spec_elements, to_slash_ref
from sldb.cli import main
from sldb.notations.exceptions import NotationMismatchError

ARQ = {
    "id": "arq", "title": "Arq", "type": "component", "version": "1.0", "metadata": {"description": "demo"},
    "data": {
        "nodes": {
            "cli": {"label": "CLI", "kind": "entry", "contains": ["core"]},
            "core": {"label": "Core"},
            "renderers": {"label": "Renderer Dispatch", "atoms": ["atom-nope"]},
        },
        "edges": [
            {"from": "cli", "to": "core", "relation": "uses"},
            {"from": "core", "to": "renderers", "relation": "loads(path)", "label": "x"},
        ],
    },
}
FLOW = {
    "id": "flow", "title": "Flow", "type": "state", "version": "1.0",
    "data": {
        "entity": "Job", "initial": "a",
        "states": [{"id": "a", "label": "A", "refs": ["SpecNodeDoc:arq.core"]}, {"id": "b", "label": "B"}],
        "transitions": [{"from": "a", "to": "b", "on": "go"}],
    },
}


@pytest.fixture
def project(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "arq.yml").write_text(yaml.safe_dump(ARQ), encoding="utf-8")
    (tmp_path / "docs" / "flow.yml").write_text(yaml.safe_dump(FLOW), encoding="utf-8")
    return tmp_path


def _rels(records, attr):
    return sorted((r.relation, getattr(r, attr).removeprefix("sldb://document/")) for r in records
                  if r.relation in ("uses", "loads_path", "transitions_to", "references", "contains"))


# --- puro ---------------------------------------------------------------------------

def test_pure_extraction_and_tokens():
    assert [e["id"] for e in spec_elements(ARQ)] == ["cli", "core", "renderers"]
    assert spec_elements(ARQ)[0]["contains"] == ["core"] and spec_elements(ARQ)[2]["atoms"] == ["atom-nope"]
    assert spec_edges(ARQ) == [
        {"from": "cli", "to": "core", "relation": "uses", "label": "", "condition": "", "attributes": {}},
        {"from": "core", "to": "renderers", "relation": "loads_path", "label": "x", "condition": "", "attributes": {}},
    ]
    assert spec_edges(FLOW) == [{"from": "a", "to": "b", "relation": "transitions_to", "label": "go", "condition": "", "attributes": {"on": "go"}}]
    assert edge_name("arq", 1, 2, spec_edges(ARQ)[0]) == "arq.01-cli__uses__core" and edge_name("x", 7, 123, {"from": "a", "relation": "r", "to": "b"}) == "x.007-a__r__b"
    assert relation_token(" Depends-On ", "x") == "depends_on" and relation_token("", "uses") == "uses"
    assert to_slash_ref("AtomDoc:atom-a") == "AtomDoc/atom-a" and to_slash_ref("desk:TaskDoc:t") == "desk:TaskDoc/t"


# --- contra un store real -----------------------------------------------------------

def test_sync_writes_spec_nodes_and_edges(project):
    store = project / ".sldb"
    report = SpecSync(store).sync(project / "docs" / "arq.yml")

    assert sorted(report.created) == sorted([
        "SpecDoc:arq", "SpecNodeDoc:arq.cli", "SpecNodeDoc:arq.core", "SpecNodeDoc:arq.renderers",
        "RelationDoc:arq.01-cli__uses__core", "RelationDoc:arq.02-core__loads_path__renderers",
        "NotationDoc:component", "GlyphDoc:component.boundary", "GlyphDoc:component.entry", "GlyphDoc:component.component",
        "LinkDoc:component.contains", "LinkDoc:component.relation",
    ])
    assert report.relation_types_added == ["loads_path", "uses"]
    assert report.unresolved == ["arq.renderers: 'AtomDoc:atom-nope' no existe en el store"]
    assert report.edge_errors == []

    out = project / "docs" / "sldb" / "arq"
    assert (out / "arq.md").exists() and (out / "nodes" / "arq.cli.md").exists() and (out / "edges" / "arq.01-cli__uses__core.md").exists()
    assert (project / "sldb" / "relation_types" / "loads_path.md").exists()
    assert sldb_api.doc_exists(store, "SpecNodeDoc/arq.renderers") and sldb_api.doc_exists(store, "RelationTypeDoc/reltype-uses")

    node = yaml.safe_load((out / "nodes" / "arq.cli.md").read_text(encoding="utf-8").split("---")[1])
    node.pop("sldb", None)  # sldb_api stamps generated provenance metadata on create_document
    assert node == {"id": "arq.cli", "spec": "SpecDoc:arq", "element": "cli", "kind": "entry", "collection": "nodes", "refs": [], "atom_refs": [], "contains": ["SpecNodeDoc:arq.core"], "data": {}}
    spec_doc = yaml.safe_load((out / "arq.md").read_text(encoding="utf-8").split("---")[1])
    assert spec_doc["spec_path"] == "docs/arq.yml" and len(spec_doc["sha256"]) == 64
    assert spec_doc["notation"] == "NotationDoc:component" and spec_doc["category"] == ""
    assert spec_doc["nodes"] == ["SpecNodeDoc:arq.cli", "SpecNodeDoc:arq.core", "SpecNodeDoc:arq.renderers"]

    assert _rels(sldb_api.edges_from(store, "SpecNodeDoc:arq.cli"), "target") == [
        ("contains", "SpecNodeDoc:arq.core"), ("references", "SpecDoc:arq"), ("uses", "SpecNodeDoc:arq.core"),
    ]
    assert ("loads_path", "SpecNodeDoc:arq.renderers") in _rels(sldb_api.edges_from(store, "SpecNodeDoc:arq.core"), "target")


def test_refs_across_specs_show_up_as_edges_the_catalog_reads(project):
    store = project / ".sldb"
    sync = SpecSync(store)
    sync.sync(project / "docs" / "arq.yml")
    report = sync.sync(project / "docs" / "flow.yml")
    assert report.unresolved == [] and report.edge_errors == []
    assert report.notation == "NotationDoc:statechart" and "NotationDoc:statechart" in report.created
    assert "GlyphDoc:statechart.state" in report.created and "LinkDoc:statechart.transition" in report.created
    flow_doc = yaml.safe_load((project / "docs" / "sldb" / "flow" / "flow.md").read_text(encoding="utf-8").split("---")[1])
    assert flow_doc["notation"] == "NotationDoc:statechart"
    assert ("references", "NotationDoc:statechart") in _rels(sldb_api.edges_from(store, "SpecDoc:flow"), "target")
    state_a = yaml.safe_load((project / "docs" / "sldb" / "flow" / "nodes" / "flow.a.md").read_text(encoding="utf-8").split("---")[1])
    assert state_a["data"] == {"initial": True}
    transition = (project / "docs" / "sldb" / "flow" / "edges" / "flow.01-a__transitions_to__b.md").read_text(encoding="utf-8")
    assert "go" in transition  # el evento viaja en `notes` del RelationDoc

    assert ("references", "SpecNodeDoc:flow.a") in _rels(sldb_api.edges_to(store, "SpecNodeDoc:arq.core"), "source")
    incoming = [(str(r.relation), str(r.source)) for r in sldb_api.edges_to(store, "SpecNodeDoc:arq.core")]
    assert ("references", "sldb://document/SpecNodeDoc:flow.a") in incoming


def test_resync_is_idempotent_and_deletes_what_left_the_spec(project):
    store = project / ".sldb"
    sync = SpecSync(store)
    sync.sync(project / "docs" / "arq.yml")
    again = sync.sync(project / "docs" / "arq.yml")
    assert again.created == [] and len(again.updated) == 12 and again.deleted == [] and again.relation_types_added == []

    smaller = yaml.safe_load(yaml.safe_dump(ARQ))
    smaller["data"]["nodes"].pop("renderers")
    smaller["data"]["edges"].pop()
    (project / "docs" / "arq.yml").write_text(yaml.safe_dump(smaller), encoding="utf-8")
    report = SpecSync(store).sync(project / "docs" / "arq.yml")
    assert sorted(report.deleted) == ["RelationDoc:arq.02-core__loads_path__renderers", "SpecNodeDoc:arq.renderers"]
    assert not sldb_api.doc_exists(store, "SpecNodeDoc/arq.renderers")
    assert not (project / "docs" / "sldb" / "arq" / "nodes" / "arq.renderers.md").exists()
    assert report.edge_errors == [] and report.unresolved == []


def test_invalid_spec_touches_nothing(project):
    (project / "docs" / "bad.yml").write_text("id: bad\ntitle: Bad\ntype: component\nversion: '1'\n", encoding="utf-8")
    with pytest.raises(Exception):
        SpecSync(project / ".sldb", validate=load_spec).sync(project / "docs" / "bad.yml")
    assert not (project / "docs" / "sldb").exists()


def test_find_store_walks_up(project):
    assert find_store(project / "docs") == (project / ".sldb").resolve()


def test_notation_override_and_mismatch(project):
    store = project / ".sldb"
    sync = SpecSync(store)
    report = sync.sync(project / "docs" / "flow.yml", notation="none")
    assert report.notation == "" and not any(d.startswith("NotationDoc") for d in report.created)
    with pytest.raises(NotationMismatchError, match="draws `class` specs"):
        sync.sync(project / "docs" / "flow.yml", notation="uml-class")


def test_other_diagram_types_extract_their_own_edges():
    activity = {"type": "activity", "data": {"start": "a", "end": "z", "steps": {
        "a": {"label": "A", "next": "d"}, "d": {"label": "D?", "kind": "decision", "branches": {"yes": "z", "no": "a"}}, "z": {"label": "Z"}}}}
    els = {e["id"]: e for e in spec_elements(activity)}
    # los pasos de start y end conservan su forma; los pseudonodos inicial y final son propios
    assert els["a"]["data"] == {"next": "d"} and els["z"]["data"] == {} and els["d"]["collection"] == "steps" and "branches" in els["d"]["data"]
    assert els["__initial"]["data"] == {"initial": True} and els["__final"]["data"] == {"final": True}
    assert [(e["from"], e["to"], e["relation"], e["label"]) for e in spec_edges(activity)] == [
        ("__initial", "a", "next", ""), ("a", "d", "next", ""), ("d", "z", "branch", "yes"), ("d", "a", "branch", "no"), ("z", "__final", "next", "")]

    sequence = {"type": "sequence", "data": {"participants": [{"id": "u", "kind": "actor"}, {"id": "s"}], "messages": [
        {"from": "u", "to": "s", "message": "hi"}, {"from": "s", "to": "u", "message": "ok", "kind": "return", "condition": "if alive"}, {"from": "u", "to": "s", "message": "bye", "kind": "async"}]}}
    assert [(e["relation"], e["label"], e["condition"]) for e in spec_edges(sequence)] == [("sends", "hi", ""), ("returns", "ok", "if alive"), ("sends_async", "bye", "")]
    assert spec_edges(sequence)[1]["attributes"] == {"kind": "return", "message": "ok"}

    matrix = {"type": "component_view_matrix", "data": {
        "views": [{"id": "v", "label": "View", "stages": [{"id": "s1", "label": "One"}, {"id": "s2", "label": "Two"}]}],
        "components": [{"name": "Root", "kind": "core", "stages": {"v": ["s1", "s2"]}, "children": [{"name": "Kid", "kind": "boundary", "stages": {"v": ["s2"]}}]}]}}
    els = {e["id"]: e for e in spec_elements(matrix)}
    assert els["v__s1"]["collection"] == "stages" and els["v__s1"]["data"] == {"view": "v", "view_label": "View", "order": 1}
    assert els["Root"]["contains"] == ["Kid"] and els["Kid"]["kind"] == "boundary" and els["Root"]["data"]["stages"] == {"v": ["s1", "s2"]}
    assert [(e["from"], e["to"], e["relation"]) for e in spec_edges(matrix)] == [("Root", "v__s1", "occupies"), ("Root", "v__s2", "occupies"), ("Kid", "v__s2", "occupies")]

    reflection = {"type": "reflection", "data": {"nodes": {"a": {"label": "A", "kind": "internal"}}, "edges": [{"from": "a", "to": "a", "relation": "uses"}]}}
    assert spec_elements(reflection)[0]["collection"] == "nodes" and spec_edges(reflection)[0]["relation"] == "uses"


def test_catalog_entries_read_vistas(tmp_path):
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "a.yml").write_text("id: a\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text(yaml.safe_dump({"vistas": [
        {"id": "va", "category": "Cat", "nav": "A", "desc": "About a", "specs": ["specs/a.yml"]},
        {"id": "vb", "category": "Cat", "title": "B", "specs": []},
    ]}), encoding="utf-8")
    entries = catalog_entries(tmp_path / "vistas.yml")
    assert entries == [{"spec": (tmp_path / "specs" / "a.yml").resolve(), "vista": "va", "notation": None, "src": None, "src_error": None, "errors": [], "catalog": {"category": "Cat", "nav": "A", "summary": "About a"}}]


def test_spec_elements_keep_the_rest_of_the_element_in_data():
    spec = {"type": "class", "data": {"classes": {"a": {"label": "A", "kind": "interface", "attributes": [{"name": "x", "type": "int"}], "methods": []}}}}
    (el,) = spec_elements(spec)
    assert el["kind"] == "interface" and el["data"] == {"attributes": [{"name": "x", "type": "int"}], "methods": []}
    guarded = {"type": "state", "data": {"initial": "a", "states": [{"id": "a", "label": "A"}], "transitions": [{"from": "a", "to": "a", "on": "tick", "guard": "x > 1"}]}}
    assert spec_elements(guarded)[0]["data"] == {"initial": True}
    assert spec_edges(guarded)[0]["label"] == "tick [x > 1]"
    acted = {"type": "state", "data": {"initial": "a", "states": [{"id": "a", "label": "A"}], "transitions": [{"from": "a", "to": "a", "on": "tick", "action": "log()"}]}}
    assert spec_edges(acted)[0]["label"] == "tick / log()" and spec_edges(acted)[0]["attributes"] == {"on": "tick", "action": "log()"}
    classes = {"type": "class", "data": {"classes": {"A": {}, "B": {}}, "relations": [{"from": "A", "to": "B", "relation": "composition", "from_multiplicity": "1", "to_multiplicity": "0..*", "label": "parts"}]}}
    assert spec_edges(classes)[0]["attributes"] == {"from_multiplicity": "1", "to_multiplicity": "0..*", "label": "parts"}


# --- CLI ----------------------------------------------------------------------------

def test_cli_sync_discovers_store_and_strict_fails_on_unresolved(project, capsys):
    rc = main(["notations", "sync", "--spec", str(project / "docs" / "arq.yml")])
    output = capsys.readouterr().out
    assert rc == 0, output
    assert "Synced arq: 3 nodes, 2 edges (12 created" in output and "atom-nope" in output

    rc = main(["notations", "sync", "--spec", str(project / "docs" / "arq.yml"), "--strict"])
    assert rc == 1

    rc = main(["notations", "sync", "--spec", str(project / "docs" / "flow.yml"), "--store", str(project / ".sldb"), "--strict"])
    assert rc == 0, capsys.readouterr()


def test_cli_sync_without_store(tmp_path, capsys):
    (tmp_path / "arq.yml").write_text(yaml.safe_dump(ARQ), encoding="utf-8")
    rc = main(["notations", "sync", "--spec", str(tmp_path / "arq.yml")])
    assert rc == 1 and "no `.sldb` store" in capsys.readouterr().err


def test_activity_terminal_end_that_is_not_a_step_is_materialized():
    """`end: end` (como en examples/activity) nombra un nodo terminal: las aristas `next: end` tienen destino."""
    spec = {"id": "activity.t", "type": "activity", "data": {"start": "a", "end": "end", "steps": {
        "a": {"label": "A", "next": "b"}, "b": {"label": "B", "next": "end"}}}}
    elements = {e["id"]: e for e in spec_elements(spec)}
    assert elements["end"]["kind"] == "end" and elements["end"]["data"]["final"] is True and elements["end"]["collection"] == "steps"
    assert "initial" not in elements["a"]["data"] and elements["__initial"]["data"]["initial"] is True and "__final" not in elements
    assert {e["to"] for e in spec_edges(spec)} <= set(elements) and {e["from"] for e in spec_edges(spec)} <= set(elements)


def test_activity_start_on_a_decision_keeps_its_diamond():
    """El paso de `start` no se vuelve el nodo inicial: el inicial es propio y fluye a el."""
    spec = {"id": "activity.t", "type": "activity", "data": {"start": "d", "end": "end", "steps": {
        "d": {"label": "Go?", "kind": "decision", "branches": {"yes": "end", "no": "d"}}}}}
    elements = {e["id"]: e for e in spec_elements(spec)}
    assert elements["d"]["kind"] == "decision" and "initial" not in elements["d"]["data"]
    assert ("__initial", "d", "next") in [(e["from"], e["to"], e["relation"]) for e in spec_edges(spec)]


def test_activity_end_that_is_a_step_is_not_duplicated():
    spec = {"id": "activity.t", "type": "activity", "data": {"start": "a", "end": "done", "steps": {"a": {"next": "done"}, "done": {"label": "Done"}}}}
    elements = spec_elements(spec)
    ids = [e["id"] for e in elements]
    assert ids.count("done") == 1 and "__final" in ids
    assert next(e for e in elements if e["id"] == "done")["data"] == {}


def test_deployment_protocol_is_an_attribute_not_a_relation_type():
    """`:5432` y `Postgres :5432` son la misma relacion `connects`; el protocolo va en attributes y rotulo."""
    spec = {"id": "deployment.t", "type": "deployment", "data": {"connections": [
        {"from": "api", "to": "db", "protocol": ":5432"}, {"from": "ui", "to": "db", "protocol": "Postgres :5432"}, {"from": "ui", "to": "api"}]}}
    edges = spec_edges(spec)
    assert {e["relation"] for e in edges} == {"connects"}
    assert [e["attributes"].get("protocol") for e in edges] == [":5432", "Postgres :5432", None]
    assert [e["label"] for e in edges] == [":5432", "Postgres :5432", ""]

FILE:instruccion
Cold-bundle de la tarea task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos-data-entity-y-afines-y-el-style-llega-a-la: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/notations/test_spec_sync.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_spec_catalog_sync.py
- TMPDIR=/dev/shm sldb stores build --check --store .sldb

