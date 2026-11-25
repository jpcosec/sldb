FILE:desk/tasks/task-clean-code-tras-carga-tolerante-edge-index-py-y-runtime-documents-py-con-una-clase-cada-uno-y-query.md
---
sldb:
  by: agent
  at: '2026-11-16T13:08:17Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-carga-tolerante-edge-index-py-y-runtime-documents-py-con-una-clase-cada-uno-y-query
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
- src/sldb/store/edge_index/edge_index.py
- src/sldb/api/documents/runtime_documents.py
- src/sldb/store/query.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
---

# Clean code tras carga-tolerante: edge_index.py y runtime_documents.py con una clase cada uno y query.py bajo 80 líneas

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: src/sldb/store/edge_index/edge_index.py y src/sldb/api/documents/runtime_documents.py tienen 2 clases (máximo 1) y src/sldb/store/query.py tiene 81 líneas efectivas (máximo 80). Lo introdujo task-carga-tolerante (163726f2); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-carga-tolerante, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Mover EdgeProblem (y edge_problem, ENDPOINT_NOT_A_NODE) a un módulo nuevo edge_problem.py del paquete sldb.store.edge_index; mover InvalidDocument a un módulo nuevo invalid_document.py del paquete sldb.api.documents, reexportando desde el módulo original; bajar query.py a 80 líneas extrayendo un helper de la carga con rechazados a un módulo vecino. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_doc_invalid_check.py
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

FILE:desk/atoms/atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los.md
---
sldb:
  by: agent
  at: '2026-11-16T10:38:59Z'
  authority: generated
  via: create_document
id: atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
title: 'Cargar un store por la API pública no aborta por un documento inválido: on_invalid=''skip''
  devuelve los sanos y nombra los inválidos'
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: src/sldb/api/documents/runtime_documents.py
---

# Cargar un store por la API pública no aborta por un documento inválido: on_invalid='skip' devuelve los sanos y nombra los inválidos

## Answer

sldb.api.load_runtime_documents(store_path, on_invalid='skip') devuelve RuntimeDocuments(documents, invalid), donde cada InvalidDocument tiene path, model y error. Con el modo por defecto ('raise') sigue devolviendo una lista y, si un documento no valida, lanza SLDBValidationError con su ruta. EdgeIndex.problem_details es una lista de EdgeProblem(kind, document, detail) paralela a problems, que se mantiene como lista de textos para no romper consumidores.

FILE:src/sldb/store/edge_index/edge_index.py
"""The composed edge index: every node and edge of a store (and its linked stores), in memory."""

from __future__ import annotations

import re

from pydantic import BaseModel, Field, PrivateAttr, model_validator

from sldb.store.edge_index.node_ids import RELATION_MODEL, as_node_id
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.store.models import EdgeNodeRecord, EdgeRecord


ENDPOINT_NOT_A_NODE = "endpoint-not-a-node"
# The one shape `resolve._authored` gives an entry of `EdgeIndex.problems`.
_ENDPOINT_PROBLEM = re.compile(r"^relation '(?P<doc>.*?)': (?:source|target) '.*' is not a tracked document$")


class EdgeProblem(BaseModel):
    """One entry of `EdgeIndex.problems`, structured: a consumer reads the fields instead of
    parsing the text."""

    kind: str = Field(description="What went wrong; `endpoint-not-a-node` for an authored edge whose end is not a node.")
    document: str = Field(description="Export id of the document that declared the edge (`RelationDoc:<name>`); empty if the text names none.")
    detail: str = Field(description="The same text as the matching entry of `problems`.")


def edge_problem(text: str) -> EdgeProblem:
    """The structured form of one `problems` entry."""
    match = _ENDPOINT_PROBLEM.match(text)
    return EdgeProblem(kind=ENDPOINT_NOT_A_NODE, document=f"{RELATION_MODEL}:{match['doc']}" if match else "", detail=text)


class EdgeIndex(BaseModel):
    """What the shards say, composed: the one door for reading edges. Ids are node ids
    (`sldb://document/Model:name`...); a bare export id `Model:name` is read as its document's."""

    nodes: dict[str, EdgeNodeRecord] = Field(default_factory=dict, description="Every node by id; the same id contributed twice is one node.")
    edges: list[EdgeRecord] = Field(default_factory=list, description="Every edge, cross-document rules applied (inherited conditions, reverse edges, edges to nothing dropped).")
    problems: list[str] = Field(default_factory=list, description="Authored edges left out because an endpoint is not a node; reported, never stored.")
    problem_details: list[EdgeProblem] = Field(default_factory=list, description="`problems`, one EdgeProblem per entry and in its order: {kind, document, detail}.")
    stale: list[str] = Field(default_factory=list, description="Export ids of tracked documents whose shard is missing, built from another hash_c or EDGE_INDEX_VERSION, from a file since edited outside sldb, or under another contract_signature of the model: run the rebuild.")
    payload_fields: dict[str, list[str]] = Field(default_factory=dict, description="Per model, the fields a `payload` facet filter may name (`ModelEdges.projected_fields`); a filter naming none of them is rejected.")
    unresolved_references: list[UnresolvedReference] = Field(default_factory=list, description="Declared reference and containment values that name no document; inspected, never stored as edges.")
    _out: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)
    _in: dict[str, list[EdgeRecord]] | None = PrivateAttr(default=None)

    @model_validator(mode="after")
    def _details_follow_problems(self) -> "EdgeIndex":
        """`problem_details` is derived from `problems` wherever the index is built (composed,
        or read back from a composed index saved before the field existed)."""
        if [d.detail for d in self.problem_details] != self.problems:
            self.problem_details = [edge_problem(p) for p in self.problems]
        return self

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

FILE:src/sldb/api/documents/runtime_documents.py
"""Bulk runtime load through sldb.api: every tracked document, payload and both hashes.

``sldb r…``/serve consumers used to import ``sldb.store.query.load_runtime_documents``
directly; this wrapper supplies the model resolver the store function takes as a parameter,
so a consumer names only a store path, an optional pythonpath and whether to follow links.

One document its model rejects used to abort the whole load with a ValidationError that named
no file. By default (``on_invalid="raise"``) it still aborts, as an SLDBValidationError whose
message starts with the document's path; ``on_invalid="skip"`` returns the sound documents and
names the rejected ones instead (``RuntimeDocuments``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, overload

from pydantic import ValidationError

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.core.exceptions import SLDBValidationError
from sldb.store.query import load_runtime_documents as _load_runtime_documents

__all__ = ["InvalidDocument", "RuntimeDocuments", "load_runtime_documents"]


@dataclass(frozen=True)
class InvalidDocument:
    """A tracked document its model rejects: path relative to its project root, the model's
    name and the text of the validation error."""

    path: str
    model: str
    error: str


@dataclass
class RuntimeDocuments:
    """What ``load_runtime_documents(..., on_invalid="skip")`` returns: the documents that
    load, and the ones left out because their model rejects them."""

    documents: list[Any] = field(default_factory=list)
    invalid: list[InvalidDocument] = field(default_factory=list)


@overload
def load_runtime_documents(store_path: Path, pythonpath: str | None = ..., include_linked: bool = ..., on_invalid: Literal["raise"] = ...) -> list[Any]: ...
@overload
def load_runtime_documents(store_path: Path, pythonpath: str | None = ..., include_linked: bool = ..., *, on_invalid: Literal["skip"]) -> RuntimeDocuments: ...
def load_runtime_documents(store_path: Path, pythonpath: str | None = None, include_linked: bool = False, on_invalid: Literal["raise", "skip"] = "raise") -> list[Any] | RuntimeDocuments:
    """Every runtime document of `store_path`, extracted, with its two index hashes.

    `on_invalid="raise"` (default): a list, as always; a document its model rejects raises
    SLDBValidationError("<path>: <original message>"). `on_invalid="skip"`: RuntimeDocuments
    with the sound documents and each rejected one as InvalidDocument, without raising."""
    if on_invalid == "skip":
        return _skipping(store_path, pythonpath, include_linked)
    if on_invalid != "raise":
        raise ValueError(f"on_invalid must be 'raise' or 'skip', not {on_invalid!r}")
    try:
        return _load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked)
    except ValidationError as exc:
        invalid = _skipping(store_path, pythonpath, include_linked).invalid
        if not invalid:
            raise
        raise SLDBValidationError(f"{invalid[0].path}: {exc}", {"path": invalid[0].path, "model": invalid[0].model}) from exc


def _skipping(store_path: Path, pythonpath: str | None, include_linked: bool) -> RuntimeDocuments:
    """The load with each rejected document left out and named (uncached, as `stores check`)."""
    rejected: list[tuple[str, str, str]] = []
    documents = _load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked, accepted_only=True, rejected=rejected)
    return RuntimeDocuments(documents=documents, invalid=[InvalidDocument(*r) for r in rejected])

FILE:src/sldb/store/query.py
from __future__ import annotations

from functools import partial
from pathlib import Path

from pydantic import ValidationError

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.layout import project_root, store_exists
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
)
from sldb.store.query_engine.models import RuntimeDocument
from sldb.store.source_read import guarded_text
from sldb.store.runtime_cache import cached_document, cached_store, invalidate_runtime_cache  # noqa: F401


def _resolve_path(base: Path, maybe_relative: str) -> Path:
    """Resolves a potentially relative path against a base path."""
    path = Path(maybe_relative)
    return path if path.is_absolute() else (base / path).resolve()


def _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec: StoreCodec) -> RuntimeDocument | None:
    if (text := guarded_text(root, root / doc.path)) is None:
        return None  # missing, or not read (source_read): `stores check` names it
    return RuntimeDocument(store_name=s_name, store_path=s_path, model_name=m_entry.name, model_type=model_type, name=doc.name, path=doc.path, payload=codec.extract(model_type, text), semantic_tags=list(doc.semantic_tags), source_hash=doc.source_hash, content_hash=doc.content_hash, field_hashes=dict(doc.field_hashes or {}), provenance=doc.provenance)


def _load_doc(doc, root, model_type, m_entry, s_name, s_path, codec: StoreCodec = default_codec) -> RuntimeDocument | None:
    """One document, from the per-document cache when the default codec is in use."""
    if codec is not default_codec:
        return _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec)
    return cached_document(doc, root, s_path, s_name, m_entry.name, model_type, lambda: _extract_doc(doc, root, model_type, m_entry, s_name, s_path, codec))


def _load_accepted(*args, rejected: list[tuple[str, str, str]] | None = None) -> RuntimeDocument | None:
    """`_load_doc`, None for a document its model rejects: `stores check` names it once, as
    `store/doc-invalid` (inbox 3895e9f7 H1), and its scans read the rest. A caller that wants
    them named passes `rejected`: each one is added as (path, model, message)."""
    try:
        return _load_doc(*args)
    except ValidationError as exc:
        if rejected is not None:
            doc, m_entry = args[0], args[3]
            rejected.append((str(doc.path), m_entry.name, str(exc)))
        return None


def _resolve_model_type(resolver, model_ref: str, p_path, store_root: Path):
    """Resolve a model, trying the store's own project root before giving up.

    Linked stores register model_refs (e.g. ``docs.models:X``) that resolve
    relative to that store's repo root, not the caller's pythonpath. We try the
    caller path first, then the store root, and return None if neither works so a
    single unresolvable model does not abort a federated query.
    """
    for candidate in (p_path, str(store_root)):
        try:
            return resolver(model_ref, candidate)
        except Exception:  # noqa: BLE001 - graceful degradation across repos
            continue
    return None


def _load_one(s_path: Path, s_name: str, resolver, p_path, codec: StoreCodec = default_codec, accepted_only: bool = False, rejected: list[tuple[str, str, str]] | None = None) -> list[RuntimeDocument]:
    root, docs = project_root(s_path), []
    load = partial(_load_accepted, rejected=rejected) if accepted_only else _load_doc
    for m in load_store_index(s_path).models:
        m_type = _resolve_model_type(resolver, m.model_ref, p_path, root)
        if m_type is None:
            continue
        d_idx = load_documents_index(root / load_models_index(root / m.models_index).documents_index)
        docs.extend([d for doc in d_idx.documents if (d := load(doc, root, m_type, m, s_name, s_path, codec))])
    return docs


def load_runtime_documents(store_path: Path, resolve_model_ref, pythonpath: str | None = None, include_linked: bool = False, codec: StoreCodec = default_codec, store_name: str = "local", accepted_only: bool = False, rejected: list[tuple[str, str, str]] | None = None) -> list[RuntimeDocument]:
    """The tracked documents of a store, extracted. With the default codec the load is cached
    by the state of the files it comes from (sldb.store.runtime_cache), so repeated queries
    do not read the store again. The list is fresh per call; the documents are shared.
    `store_name` is the name the documents carry: the alias when a linked store is read alone.
    `accepted_only` leaves out each document its model rejects instead of raising (uncached:
    `stores check` scans, inbox 3895e9f7 H1); with `rejected` it also adds each one left out
    as (path relative to its project root, model, message)."""
    def one(path: Path, name: str) -> list[RuntimeDocument]:
        loader = lambda: _load_one(path, name, resolve_model_ref, pythonpath, codec, accepted_only, rejected)  # noqa: E731
        return cached_store(path, name, pythonpath, loader) if codec is default_codec and not accepted_only else loader()

    return _load_federated_documents(store_path, one) if include_linked else list(one(store_path, store_name))


def _load_federated_documents(store_path: Path, load_one) -> list[RuntimeDocument]:
    """Traverse explicit links once per canonical store, safely across cycles."""
    documents: list[RuntimeDocument] = []
    pending: list[tuple[Path, str]] = [(store_path.resolve(), "local")]
    visited: set[Path] = set()
    while pending:
        _visit_federated_store(pending.pop(0), pending, visited, documents, load_one)
    return documents


def _visit_federated_store(item, pending, visited, documents, load_one) -> None:
    current, name = item
    if current in visited or not store_exists(current):
        return
    visited.add(current)
    documents.extend(load_one(current, name))
    pending.extend(_linked_stores(current))


def _linked_stores(store_path: Path) -> list[tuple[Path, str]]:
    root = project_root(store_path)
    return [
        (_resolve_path(root, entry.path).resolve(), entry.name)
        for entry in load_store_index(store_path).stores
        if store_exists(_resolve_path(root, entry.path))
    ]


from sldb.store.query_engine.structural import (  # noqa: E402
    list_structural as list_structural,
    get_structural as get_structural,
)
from sldb.store.query_engine.structural_queries import (  # noqa: E402
    glob_structural as glob_structural,
    find_structural as find_structural,
)
from sldb.store.query_engine.semantic import (  # noqa: E402
    list_semantic as list_semantic,
    get_semantic as get_semantic,
    glob_semantic as glob_semantic,
    find_semantic as find_semantic,
)
from sldb.store.query_engine.global_semantic import (  # noqa: E402
    get_global_semantic as get_global_semantic,
    list_global_semantic as list_global_semantic,
)

FILE:instruccion
Cold-bundle de la tarea task-clean-code-tras-carga-tolerante-edge-index-py-y-runtime-documents-py-con-una-clase-cada-uno-y-query: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_doc_invalid_check.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

