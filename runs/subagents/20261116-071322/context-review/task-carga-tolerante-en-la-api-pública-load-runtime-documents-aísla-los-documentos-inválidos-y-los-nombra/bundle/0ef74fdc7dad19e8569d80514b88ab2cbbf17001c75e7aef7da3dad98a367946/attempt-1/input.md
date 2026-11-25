FILE:desk/tasks/task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra.md
---
sldb:
  by: agent
  at: '2026-11-16T05:05:01Z'
  authority: generated
  via: save_document_payload
id: task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261031-033714-suggestion-resiliencia-en-carga-de-store-ante-documentos-invalidos-y-problems-estructurados.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/runtime_documents.py
- src/sldb/store/edge_index/edge_index.py
- tests/api/test_api_documents.py
- tests/api/test_api_edges.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos
---

# Carga tolerante en la API pública: load_runtime_documents aísla los documentos inválidos y los nombra, y EdgeIndex expone problemas estructurados

## Rationale

_Explain why this task exists or the business driver behind it._

En la integración del Workspace de graph_ui, load_runtime_documents abortó con ValidationError para todo el store porque un solo Markdown era inválido, sin nombrar el archivo culpable. El modo que salta documentos rechazados existe pero es interno (accepted_only en src/sldb/store/query.py:75-88, lo usa stores check); el envoltorio público src/sldb/api/documents/runtime_documents.py:17 no lo expone. EdgeIndex.problems es list[str] (src/sldb/store/edge_index/edge_index.py:18), así que un consumidor tiene que parsear texto. Origen: desk/inbox/20261031-033714-suggestion-resiliencia-en-carga-de-store-ante-documentos-invalidos-y-problems-estructurados.md.

## Goal

_Describe the concrete result this task must produce._

load_runtime_documents(..., on_invalid="skip") devuelve los documentos sanos y una lista de (ruta, modelo, error) de los inválidos sin lanzar; el comportamiento por defecto (on_invalid="raise") no cambia salvo que el mensaje nombra la ruta del documento; EdgeIndex gana un campo problem_details con objetos {kind, document, detail} junto a problems, que no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: parámetro on_invalid: Literal["raise", "skip"] = "raise" en la función pública de src/sldb/api/documents/runtime_documents.py, implementado con accepted_only de src/sldb/store/query.py; un tipo de retorno para el modo skip (dataclass RuntimeDocuments con documents e invalid) definido en el mismo módulo y exportado; en modo raise, la excepción incluye la ruta. En EdgeIndex (src/sldb/store/edge_index/edge_index.py) un campo nuevo problem_details: list[EdgeProblem] (modelo pydantic con kind, document, detail), poblado donde hoy se agregan strings a problems; problems sigue igual para no romper consumidores. Tests en tests/api/test_api_documents.py (store con un documento inválido: skip devuelve los sanos y nombra el inválido; raise nombra la ruta) y en tests/api/test_api_edges.py (problem_details tiene la misma cantidad que problems). CHANGELOG.md. No entra: resolve_runtime_doc focalizado sin barrido total (src/sldb/api/records/resolve.py:6) — se mide en esta tarea y se anota el tiempo en el informe, pero su cambio es otra tarea si hace falta; quitar problems; tocar graph_ui.

Precisiones (preflight-1): con on_invalid="raise" la función devuelve list como hoy; con on_invalid="skip" devuelve RuntimeDocuments(documents: list, invalid: list[InvalidDocument]), donde InvalidDocument es un dataclass (path: str relativo al proyecto, model: str, error: str con el texto de la excepción). Se implementa pasando accepted_only=True a sldb.store.query.load_runtime_documents (el parámetro ya existe) más la lista de rechazados, que hay que recoger en _load_accepted (src/sldb/store/query.py). En modo raise, la excepción que hoy sale se relanza como SLDBValidationError con el mensaje "<ruta>: <mensaje original>". EdgeProblem.kind es "endpoint-not-a-node" para los problemas que hoy se agregan como strings (son todos de ese tipo según la descripción del campo problems), document es el export id del documento que declaró la arista y detail es el mismo string de problems. La medición de resolve_runtime_doc va al informe del ejecutor: tiempo de resolve_runtime_doc sobre el store de sldb, en frío.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/documents/runtime_documents.py, src/sldb/store/query.py (75-88), src/sldb/store/edge_index/edge_index.py y grep "problems.append\|problems=" en src/sldb/store/edge_index. 2) Implementar on_invalid. 3) Agregar EdgeProblem y problem_details en cada punto donde se agrega un problema. 4) Tests. 5) stores build --check.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_check.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los tests nuevos; on_invalid="skip" sobre un store con un documento inválido devuelve los sanos y el inválido en invalid; problem_details existe y cuadra con problems; CHANGELOG y commit.

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

FILE:desk/atoms/atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos.md
---
id: atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos
title: Una vista de todo el store no puede depender de que importen todos sus modelos
five_wh_one_plus: why
tags:
- system:sldb
---

# Una vista de todo el store no puede depender de que importen todos sus modelos

## Answer

Un store registra modelos de varios paquetes (deskops, pron, el propio repo) y no todos están instalados en cada entorno. Una vista que recorre todos los modelos (el AST del store en src/sldb/api/records/build_ast.py) tiene que registrar el que no importa como no resuelto, con su error, y seguir: si aborta, cualquier consulta de otro modelo cae con él.

FILE:src/sldb/api/documents/runtime_documents.py
"""Bulk runtime load through sldb.api: every tracked document, payload and both hashes.

``sldb r…``/serve consumers used to import ``sldb.store.query.load_runtime_documents``
directly; this wrapper supplies the model resolver the store function takes as a parameter,
so a consumer names only a store path, an optional pythonpath and whether to follow links.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.query import load_runtime_documents as _load_runtime_documents


def load_runtime_documents(store_path: Path, pythonpath: str | None = None, include_linked: bool = False) -> list[Any]:
    """Every runtime document of `store_path`, extracted, with its two index hashes."""
    return _load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked)

FILE:src/sldb/store/edge_index/edge_index.py
"""The composed edge index: every node and edge of a store (and its linked stores), in memory."""

from __future__ import annotations

from pydantic import BaseModel, Field, PrivateAttr

from sldb.store.edge_index.node_ids import as_node_id
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.store.models import EdgeNodeRecord, EdgeRecord


class EdgeIndex(BaseModel):
    """What the shards say, composed: the one door for reading edges. Ids are node ids
    (`sldb://document/Model:name`...); a bare export id `Model:name` is read as its document's."""

    nodes: dict[str, EdgeNodeRecord] = Field(default_factory=dict, description="Every node by id; the same id contributed twice is one node.")
    edges: list[EdgeRecord] = Field(default_factory=list, description="Every edge, cross-document rules applied (inherited conditions, reverse edges, edges to nothing dropped).")
    problems: list[str] = Field(default_factory=list, description="Authored edges left out because an endpoint is not a node; reported, never stored.")
    stale: list[str] = Field(default_factory=list, description="Export ids of tracked documents whose shard is missing, built from another hash_c or EDGE_INDEX_VERSION, from a file since edited outside sldb, or under another contract_signature of the model: run the rebuild.")
    payload_fields: dict[str, list[str]] = Field(default_factory=dict, description="Per model, the fields a `payload` facet filter may name (`ModelEdges.projected_fields`); a filter naming none of them is rejected.")
    unresolved_references: list[UnresolvedReference] = Field(default_factory=list, description="Declared reference and containment values that name no document; inspected, never stored as edges.")
    _out: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)
    _in: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)

    def edges_from(self, node_id: str, relation: str | None = None) -> list[EdgeRecord]:
        """Edges leaving `node_id`, of one relation or of all."""
        self._ensure_maps()
        return [e for e in (self._out or {}).get(as_node_id(node_id), []) if relation in (None, e.relation)]

    def edges_to(self, node_id: str, relation: str | None = None) -> list[EdgeRecord]:
        """Edges pointing at `node_id`, of one relation or of all."""
        self._ensure_maps()
        return [e for e in (self._in or {}).get(as_node_id(node_id), []) if relation in (None, e.relation)]

    def node(self, node_id: str) -> EdgeNodeRecord | None:
        """The node with that id (or that export id), None when the index has none."""
        return self.nodes.get(as_node_id(node_id))

    def nodes_of_type(self, node_type: str) -> list[EdgeNodeRecord]:
        """Nodes of one class, sorted by id; a document's class is its model's name."""
        return sorted((n for n in self.nodes.values() if n.node_type == node_type), key=lambda n: n.id)

    def _ensure_maps(self) -> None:
        if self._out is not None:
            return
        self._out, self._in = {}, {}
        for e in self.edges:
            self._out.setdefault(e.source, []).append(e)
            self._in.setdefault(e.target, []).append(e)

FILE:tests/api/test_api_documents.py
"""`sldb.api` document operations and the `sldb.cli` bridges over them."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

import sldb.api as api
from sldb.cli import dict_utils
from sldb.cli.commands.fields_save import save_payload
from sldb.core.exceptions import SLDBError, SLDBPayloadSaveError, SLDBStoreError, SLDBValidationError
from sldb.store.query import load_runtime_documents

from .conftest import PAYLOAD


def _title(api_store, name: str) -> str:
    docs = load_runtime_documents(api_store.store, api.resolve_model_ref, api_store.pythonpath)
    return next(d.payload["title"] for d in docs if d.name == name)


def test_save_document_payload_rewrites_markdown_and_indexes(api_store):
    saved = api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Fixed login"}, api_store.pythonpath)
    assert saved.path.resolve() == (api_store.root / "login.md").resolve()
    assert "# Fixed login" in saved.path.read_text(encoding="utf-8")
    api.open_store(api_store.store)
    assert _title(api_store, "login") == "Fixed login"


def test_save_document_payload_refuses_unknown_documents_and_models(api_store):
    with pytest.raises(SLDBPayloadSaveError, match="Doc 'ghost' not registered."):
        api.save_document_payload(api_store.store, "TicketDoc", "ghost", PAYLOAD, api_store.pythonpath)
    with pytest.raises(SLDBPayloadSaveError, match="Model 'NopeDoc' not registered."):
        api.save_document_payload(api_store.store, "NopeDoc", "login", PAYLOAD, api_store.pythonpath)


def test_cli_save_payload_still_exits_with_the_message(api_store):
    doc = SimpleNamespace(model_name="TicketDoc", name="ghost")
    with pytest.raises(SystemExit, match="Doc 'ghost' not registered."):
        save_payload(doc, PAYLOAD, str(api_store.store), api_store.pythonpath)


def test_track_document_file_refuses_a_file_the_model_cannot_read(api_store):
    (api_store.root / "broken.md").write_text("not a ticket\n", encoding="utf-8")
    with pytest.raises((SLDBValidationError, ValidationError)):
        api.track_document_file(api_store.store, "TicketDoc", "broken.md", pythonpath=api_store.pythonpath)


def test_track_document_file_resolves_relative_paths_against_the_project_root(api_store):
    api_store.write_document("signup", PAYLOAD)
    tracked = api.track_document_file(api_store.store, "TicketDoc", "signup.md", pythonpath=api_store.pythonpath, force=True)
    assert (tracked.model, tracked.name, tracked.path) == ("TicketDoc", "signup", (api_store.root / "signup.md").resolve())


def test_untrack_document_drops_it_from_the_store(api_store):
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    untracked = api.untrack_document(api_store.store, "signup", api_store.pythonpath)
    assert (untracked.model, untracked.name) == ("TicketDoc", "signup")
    assert (api_store.root / "signup.md").exists()
    with pytest.raises(SLDBError, match="not found"):
        api.untrack_document(api_store.store, "signup", api_store.pythonpath)


def test_a_document_can_be_named_by_its_absolute_path(api_store):
    """The store records paths relative to the project root; an absolute one used to miss."""
    path = (api_store.root / "signup.md").resolve()
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    deleted = api.delete_document(api_store.store, str(path), api_store.pythonpath)
    assert (deleted.model, deleted.name) == ("TicketDoc", "signup")
    assert not path.exists()


def test_payload_paths_are_the_cli_helpers():
    assert dict_utils.deep_get is api.deep_get and dict_utils.deep_set is api.deep_set
    payload = {"items": [{"name": "a"}]}
    api.deep_set(payload, "items.0.name", "b")
    api.deep_set(payload, "meta.owner", "jp", create=True)
    assert api.deep_get(payload, "items.0.name") == "b"
    assert api.deep_delete(payload, "meta.owner") == {"items": [{"name": "b"}], "meta": {}}
    with pytest.raises(TypeError):
        api.ensure_list(payload, "meta")


def test_move_document_moves_the_file_and_keeps_the_name(api_store):
    moved = api.move_document(api_store.store, "login", "tickets/login.md", api_store.pythonpath)
    assert (moved.model, moved.name, moved.path) == ("TicketDoc", "login", (api_store.root / "tickets" / "login.md").resolve())
    assert not (api_store.root / "login.md").exists()
    assert api.doc_status(api_store.store, "login").exists
    assert _title(api_store, "login") == "Broken login"


def test_move_document_refuses_a_taken_destination_without_moving(api_store):
    (api_store.root / "taken.md").write_text("# Taken\n", encoding="utf-8")
    with pytest.raises(SLDBStoreError, match="already exists"):
        api.move_document(api_store.store, "login", "taken.md", api_store.pythonpath)
    assert (api_store.root / "login.md").exists()

FILE:tests/api/test_api_edges.py
"""`sldb.api` edge index: per-document shards on the hash chain, read through one door.

Covers: every write keeps its own shard current and touches no other document's; an untracked
document loses its shard; relation types, relations and anchors become nodes and edges, not
document nodes; cross-document rules (inherited condition and axis, reverse edges, orphans)
apply on read and are reported, not stored; `exclude_tags` is the reader's; a linked store's
documents come back qualified by the link's name; `init_relations` is idempotent.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.store.layout import edges_model_shard_path, edges_shard_path, edges_store_shard_path

MODULE = "sldb_edges_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Table(StructuredNLDoc):
    __semantics__ = {"type": ["restaurant", "table"]}
    __template__ = "# ⸢rev•title⸥\\n\\nCapacity: ⸢rev•capacity⸥\\n\\n## Notes\\n\\n⸢rev,markdown•notes⸥"
    title: str = Field(description="Title.")
    capacity: int = Field(description="Seats.")
    notes: str = Field(default="", description="Notes.")


class Booking(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nSize: ⸢rev•party_size⸥"
    title: str = Field(description="Title.")
    party_size: int = Field(description="People.")


class Move(StructuredNLDoc):
    __semantics__ = {"type": ["pron", "move"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Alias(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "anchor"]}
    __template__ = "# ⸢rev•symbol⸥\\n\\nRef: ⸢rev•ref⸥"
    symbol: str = Field(description="Word.")
    ref: str = Field(description="What it names.")
'''


class EdgeWorld:
    """A store prepared for relations, with the models above registered."""

    def __init__(self, base: Path, name: str = "world") -> None:
        self.root, self.py = base / name, str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Table", "Booking", "Move", "Alias"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str, source: list[str], target: list[str], **extra) -> None:
        payload = {"title": name, "name": name, "direction": "directed", "cardinality": "many_to_many", "axis": "WHERE", "source_types": source, "target_types": target, "condition": "", "description": f"{name}."}
        self.create("RelationTypeDoc", f"rt-{name}", {**payload, **extra})

    def relation(self, name: str, src: str, tgt: str, rtype: str, condition: str = "", **extra) -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": rtype, "condition": condition, "notes": "", **extra})


@pytest.fixture
def world(tmp_path: Path) -> EdgeWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    w = EdgeWorld(tmp_path)
    w.create("Table", "t12", {"title": "Table 12", "capacity": 6, "notes": "By the window."})
    w.create("Table", "t14", {"title": "Table 14", "capacity": 8, "notes": ""})
    w.create("Booking", "b1", {"title": "Ana", "party_size": 6})
    w.relation_type("assigned_to", ["Booking"], ["Table"], cardinality="many_to_one", condition="capacity >= {party_size}")
    w.relation("b1-t12", "Booking:b1", "Table:t12", "assigned_to")
    return w


def _pairs(edges) -> list[tuple[str, str]]:
    return [(e.target, e.relation) for e in edges]


def test_a_write_leaves_a_shard_per_document_model_and_store(world: EdgeWorld):
    assert edges_shard_path(world.store, "Table", "t12").exists()
    assert edges_model_shard_path(world.store, "Table").exists()
    assert edges_store_shard_path(world.store).exists()
    assert api.load_edge_index(world.store).stale == []


def test_structural_edges_and_typed_nodes(world: EdgeWorld):
    assert ("sldb://document/Table:t12", "has_document") in _pairs(api.edges_from(world.store, "sldb://model/Table"))
    assert ("sldb://section/Table:t12#table-12/notes", "has_section") in _pairs(api.edges_from(world.store, "Table:t12"))
    assert ("sldb://semantic_tag/type.restaurant.table", "tagged_as") in _pairs(api.edges_from(world.store, "Table:t12", "tagged_as"))
    assert api.edge_node(world.store, "Table:t12").node_type == "Table"
    assert [n.id for n in api.edge_nodes_of_type(world.store, "Booking")] == ["sldb://document/Booking:b1"]
    field = api.edge_node(world.store, "sldb://field/Table.capacity")
    assert field.node_type == "sldb_field" and field.semantics["kind"] == "integer"
    assert [e.source for e in api.edges_to(world.store, "sldb://model/Table", "has_model")] == ["sldb://store"]


def test_a_relation_doc_is_an_edge_that_inherits_from_its_type(world: EdgeWorld):
    [edge] = api.edges_from(world.store, "Booking:b1", "assigned_to")
    assert (edge.source, edge.target) == ("sldb://document/Booking:b1", "sldb://document/Table:t12")
    assert edge.metadata == {"origin": "relation_doc", "relation_doc": "b1-t12", "condition": "capacity >= {party_size}", "axis": "WHERE"}
    assert api.edges_to(world.store, "Table:t12", "assigned_to") == [edge]
    assert api.edge_node(world.store, "RelationDoc:b1-t12") is None
    applies = api.edges_from(world.store, "sldb://relation_type/assigned_to")
    assert _pairs(applies) == [("sldb://model/Booking", "applies_to_source"), ("sldb://model/Table", "applies_to_target")]
    assert api.check_edges(world.store).ok


def test_editing_one_document_rewrites_only_its_shard(world: EdgeWorld):
    shards = {name: edges_shard_path(world.store, model, name) for model, name in (("Table", "t12"), ("Table", "t14"), ("Booking", "b1"), ("RelationDoc", "b1-t12"))}
    before = {name: path.stat().st_mtime_ns for name, path in shards.items()}
    old_hash = api.edge_node(world.store, "Table:t14").semantics["hash_c"]
    api.save_document_payload(world.store, "Table", "t14", {"title": "Table 14", "capacity": 10, "notes": ""}, world.py)
    after = {name: path.stat().st_mtime_ns for name, path in shards.items()}
    assert [name for name in shards if before[name] != after[name]] == ["t14"]
    assert api.edge_node(world.store, "Table:t14").semantics["hash_c"] not in ("", old_hash)
    assert api.load_edge_index(world.store).stale == []
    assert api.rebuild_edges(world.store, world.py).docs_written == 0


def test_untracking_a_document_drops_its_shard_and_reports_the_orphan(world: EdgeWorld):
    api.untrack_document(world.store, "t12", world.py)
    assert not edges_shard_path(world.store, "Table", "t12").exists()
    assert api.edge_node(world.store, "Table:t12") is None
    assert api.edges_from(world.store, "Booking:b1", "assigned_to") == []
    assert api.check_edges(world.store).errors == ["relation 'b1-t12': target 'Table:t12' is not a tracked document"]


def test_undirected_types_read_both_ways_and_bad_classes_are_reported(world: EdgeWorld):
    world.relation_type("near", ["Table"], ["Table"], direction="undirected")
    world.relation("t12-t14", "Table:t12", "Table:t14", "near")
    [back] = api.edges_from(world.store, "Table:t14", "near")
    assert back.target == "sldb://document/Table:t12" and back.metadata["reverse"] is True
    world.relation("b1-near", "Booking:b1", "Table:t14", "near")
    errors = api.check_edges(world.store).errors
    assert any("source class 'Booking' not in source_types ['Table']" in e for e in errors)


def test_exclude_tags_is_the_readers_choice(world: EdgeWorld):
    world.create("Move", "m1", {"title": "a move"})
    assert api.edge_node(world.store, "Move:m1") is not None
    hidden = api.load_edge_index(world.store, exclude_tags=["type.pron.move"])
    assert hidden.node("Move:m1") is None
    assert hidden.edges_from("sldb://model/Move", "has_document") == []
    assert hidden.node("sldb://semantic_tag/type.pron.move") is not None


def test_anchors_name_what_their_ref_points_at(world: EdgeWorld):
    world.create("Alias", "mesa", {"symbol": "mesa", "ref": "model:Table"})
    world.create("Alias", "cupo", {"symbol": "cupo", "ref": "(field Table capacity)"})
    assert _pairs(api.edges_from(world.store, "sldb://anchor/mesa")) == [("sldb://model/Table", "names")]
    assert _pairs(api.edges_from(world.store, "sldb://anchor/cupo")) == [("sldb://field/Table.capacity", "names")]
    assert api.edge_node(world.store, "Alias:mesa") is None


def test_linked_store_documents_come_back_qualified(world: EdgeWorld, tmp_path: Path):
    other = EdgeWorld(tmp_path, "other")
    other.create("Table", "t99", {"title": "Table 99", "capacity": 2, "notes": ""})
    api.link_store(world.store, other.store, "annex")
    world.relation("b1-t99", "Booking:b1", "annex:Table:t99", "assigned_to")
    index = api.load_edge_index(world.store)
    assert index.node("annex:Table:t99").semantics["store"] == "annex"
    assert "sldb://document/annex:Table:t99" in [e.target for e in index.edges_from("sldb://model/Table", "has_document")]
    assert [e.target for e in index.edges_from("Booking:b1", "assigned_to")] == ["sldb://document/Table:t12", "sldb://document/annex:Table:t99"]
    assert api.load_edge_index(world.store, include_linked=False).node("annex:Table:t99") is None


def test_init_relations_is_idempotent(world: EdgeWorld):
    report = api.init_relations(world.store, world.py)
    assert (report.models_added, report.types_written, report.predicates_added) == ([], [], [])
    assert (world.root / "sldb" / "relation_types" / "tagged_as.md").exists()
    assert "sldb://relation_type/has_document" in [n.id for n in api.edge_nodes_of_type(world.store, "relation_type")]


def test_cli_edges_uses_the_api(world: EdgeWorld, capsys):
    from sldb.cli import main as cli_main

    assert cli_main(["edges", "show", "Booking:b1", "--relation", "assigned_to", "--store", str(world.store)]) == 0
    assert '"target": "sldb://document/Table:t12"' in capsys.readouterr().out
    assert cli_main(["edges", "check", "--store", str(world.store)]) == 0
    assert cli_main(["edges", "rebuild", "--store", str(world.store), "--pythonpath", world.py]) == 0
    assert "0 shard(s) written" in capsys.readouterr().out
    world.relation("orphan", "Booking:b1", "Table:nowhere", "assigned_to")
    assert cli_main(["edges", "check", "--store", str(world.store)]) == 1
    assert cli_main(["help", "edges"]) == 0


def test_a_hand_edit_reaches_the_index_through_stores_update(world: EdgeWorld):
    others = {name: edges_shard_path(world.store, "Table", name).stat().st_mtime_ns for name in ("t14",)}
    old_hash = api.edge_node(world.store, "Table:t12").semantics["hash_c"]
    path = world.root / "t12.md"
    path.write_text(path.read_text(encoding="utf-8").replace("By the window.", "By the door."), encoding="utf-8")
    assert api.update_store_indexes(world.store, world.py).complete
    assert api.edge_node(world.store, "Table:t12").semantics["hash_c"] != old_hash
    assert edges_shard_path(world.store, "Table", "t14").stat().st_mtime_ns == others["t14"]
    assert api.load_edge_index(world.store).stale == []


def test_a_wiped_index_reads_as_stale_and_rebuild_brings_it_back(world: EdgeWorld):
    import shutil

    before = api.load_edge_index(world.store)
    shutil.rmtree(world.store.parent / ".sldb_cache" / "edges")
    wiped = api.load_edge_index(world.store)
    assert "Table:t12" in wiped.stale and wiped.node("Table:t12") is None
    assert api.rebuild_edges(world.store, world.py).docs_written == len(wiped.stale)
    rebuilt = api.load_edge_index(world.store)
    assert rebuilt.stale == [] and rebuilt.nodes == before.nodes and rebuilt.edges == before.edges
    edges_shard_path(world.store, "Table", "t14").unlink()  # one shard lost, its model's cache key intact
    assert api.load_edge_index(world.store).stale == ["Table:t14"]
    assert api.rebuild_edges(world.store, world.py).docs_written == 1
    assert api.load_edge_index(world.store).nodes == before.nodes


def test_a_relation_carries_free_attributes_to_its_edge(world: EdgeWorld):
    """spec2viz loses a class relation's multiplicities and roles, a transition's action."""
    world.create("Booking", "b2", {"title": "Luis", "party_size": 2})
    world.relation("b2-t14", "Booking:b2", "Table:t14", "assigned_to", attributes={"multiplicity": "1..*", "role": "guest"})
    edge = next(e for e in api.load_edge_index(world.store).edges_from("sldb://document/Booking:b2", "assigned_to"))
    assert edge.metadata["attributes"] == {"multiplicity": "1..*", "role": "guest"}
    plain = next(e for e in api.load_edge_index(world.store).edges_from("sldb://document/Booking:b1", "assigned_to"))
    assert "attributes" not in plain.metadata, "an edge without attributes keeps its shard"


def test_query_snapshot_runs_a_query_without_a_store(world: EdgeWorld, tmp_path: Path):
    from sldb.api import graph as graph_api

    output = tmp_path / "snap.json"
    graph_api.snapshot_save(world.store, output, include_linked=False)
    query = graph_api.StructuredQuery(scope=graph_api.GraphScope(node_id_prefix="sldb://document/Table:"))
    assert sorted(n.id for n in graph_api.query_snapshot(graph_api.snapshot_load(output), query)) == sorted(n.id for n in graph_api.execute_query(world.store, query, include_linked=False))
    assert graph_api.Edge and graph_api.SystemIdentity

FILE:instruccion
Cold-bundle de la tarea task-carga-tolerante-en-la-api-pública-load-runtime-documents-aísla-los-documentos-inválidos-y-los-nombra: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/store/test_doc_invalid_check.py

