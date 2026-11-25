FILE:desk/tasks/task-referrers-y-rewrite-references-aceptan-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-duplican-men.md
---
sldb:
  by: agent
  at: '2026-11-16T05:40:56Z'
  authority: generated
  via: save_document_payload
id: task-referrers-y-rewrite-references-aceptan-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-duplican-men
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-referrers-y-rewrite-references-para-un-grafo-armado-en-proceso-excluir-fuentes-y-menciones-duplicada.md
depends_on: []
pills: []
files:
- src/sldb/api/edges/referrers.py
- src/sldb/api/edges/rewrite_references.py
- tests/api/test_referrers.py
- tests/api/test_rewrite_references.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
---

# referrers y rewrite_references aceptan un grafo armado en proceso, excluyen fuentes y no duplican menciones del frontmatter

## Rationale

_Explain why this task exists or the business driver behind it._

deskops (CC35c) recompone en el módulo references de deskops.services (repo deskops) lo que la API pública no cubre: (H-a) referrers y rewrite_references (src/sldb/api/edges/referrers.py:50, src/sldb/api/edges/rewrite_references.py:37) leen el grafo de store.yaml con optional_graph (referrers.py:86) y deskops arma el suyo en proceso, así que no ven menciones; (H-b) rewrite_references no admite excluir fuentes; (H-c) find_hits (referrers.py:100) devuelve dos veces un campo declarado del frontmatter, como schema y como mention. Origen: desk/inbox/inbox-note-referrers-y-rewrite-references-para-un-grafo-armado-en-proceso-excluir-fuentes-y-menciones-duplicada.md.

## Goal

_Describe the concrete result this task must produce._

referrers(store, target, graph=g) y rewrite_references(..., graph=g, excluded_sources=[...]) usan g en lugar de optional_graph cuando se pasa, no tocan las fuentes excluidas, y find_hits no devuelve como mention una línea del frontmatter que ya es un hit schema del mismo documento.

## Scope

_State what is in scope and what is out of scope._

Entra: parámetro keyword-only graph: ProjectGraph | None = None en referrers y rewrite_references (si es None se usa optional_graph como hoy); parámetro keyword-only excluded_sources: Iterable[str] = () en rewrite_references, con fuentes nombradas por ruta trackeada o export id Model:name, que se saltan tanto en campos como en menciones; en find_hits, descartar las mentions cuya ruta es la de un documento con un hit schema y cuya línea cae dentro del frontmatter de ese documento. Tests en tests/api/test_referrers.py (H-a con el desk mínimo de la nota armado en tmp_path: sin graph devuelve [], con graph devuelve la mención; H-c: un campo declarado aparece una sola vez como schema) y tests/api/test_rewrite_references.py (H-b: una fuente excluida queda byte a byte igual). CHANGELOG.md. No entra: declarar project_graph en el store.yaml de deskops (es de deskops), cambiar el formato de Referrer, ni tocar deskops (al cerrar se le avisa con deskops message send --to deskops).

Precisiones (preflight-1): ProjectGraph se importa de sldb.api.edges.project_graph.project_graph. Cada excluded_source se resuelve con resolve_target (el mismo que usa referrers para el target) a un documento trackeado; se compara por ruta trackeada relativa al proyecto, así que "Model:name" y la ruta del mismo documento excluyen lo mismo; una fuente que no resuelve lanza SLDBDocumentTargetError. El frontmatter de un documento es el bloque entre la primera línea "---" (línea 1) y la siguiente línea "---", ambas incluidas, numerando líneas desde 1 como ya hace LineMentions.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer referrers.py completo (referrers, optional_graph, find_hits) y rewrite_references.py (rewrite_references, _write, _planned_text). 2) Agregar graph y pasarlo a find_hits. 3) Agregar excluded_sources y filtrar en la planificación de campos y de menciones. 4) Dedupe de H-c en find_hits. 5) Tests y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos pasan con los tres casos nuevos; sin graph ni excluded_sources el comportamiento es el de hoy (los tests existentes siguen verdes); CHANGELOG, commit y aviso a deskops.

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

FILE:desk/atoms/atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada.md
---
id: atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada
title: Las referencias entrantes de un documento se consultan y se reescriben en sldb,
  todo o nada
five_wh_one_plus: what
tags:
- system:sldb
- topic:references
provenance: docs/architecture/references.md
---

# Las referencias entrantes de un documento se consultan y se reescriben en sldb, todo o nada

## Answer

sldb responde quién apunta a un documento: sldb.api.referrers(store, target) devuelve cada Referrer con source, field, index y location, y origin schema (campos de referencia del índice de aristas) o mention (menciones del grafo de proyecto de GD21). target acepta export_id, Model:name, ruta trackeada o id de nodo del grafo. sldb.api.rewrite_references(store, target, replacement | None) reemplaza o quita esas referencias conservando la forma del valor original, sin dejar huecos ni duplicados en las listas y sin borrar prosa (una mención sin reemplazo se informa en skipped), dentro de una transacción de GD24: todo o nada. Un campo __doc_anchors__ se reescribe a doc:Model:name sin hash para que sldb lo vuelva a anclar al guardar. CLI: sldb edges referrers y sldb edges rewrite --to|--remove [--dry-run]; serve: GET /edges/referrers y POST /edges/rewrite. Implementado en GD22 (plan generalizar-desde-deskops).

FILE:src/sldb/api/edges/referrers.py
"""`sldb.api.referrers(store, target)` (GD22): the incoming references of a document or of a
project graph node (docs/architecture/references.md).

The declared fields of tracked documents (a scalar value or an element of a list, `origin:
schema`) come from the store's composed edge index, the one every sldb write keeps current;
the mentions a `MentionPattern` captures in prose (`origin: mention`, located `path:line`) come
from `ProjectGraph.edges_to` of GD21, memoized per process. Neither reads walk the project.

`target` is resolved first as a tracked document, with the rule of `doc_status` plus the
export id form (`name`, `Model/name`, `Model:name` or a tracked path; several candidates are an
error naming them), then as a project graph node id (`kind:identity`); anything else is
`SLDBDocumentTargetError`. A document that is also a project node (its path is on a surface)
has both kinds of referrers.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.project_graph.store_project_graph import project_graph
from sldb.api.edges.referrer import Referrer
from sldb.api.edges.rewrite_mentions import mention_hits
from sldb.api.edges.rewrite_values import schema_hits
from sldb.api.stores.doc_ref import matches_doc_ref
from sldb.api.stores.indexed_documents import indexed_documents
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBStoreError

Hit = tuple[Referrer, str | None]


class Target(NamedTuple):
    """What a target (or a replacement) resolved to: a tracked document, a project node, or neither."""

    given: str
    model: str | None
    name: str | None
    path: str | None
    node_id: str | None

    @property
    def export_id(self) -> str | None:
        """`Model:name` when the target is a tracked document."""
        return f"{self.model}:{self.name}" if self.model else None


def referrers(store: str | Path | None, target: str, pythonpath: str | None = None) -> list[Referrer]:
    """Every reference to `target`, fields first (by source, field and position), then mentions (by path and line).

    Args:
        store: The store (path, alias, or None to discover it).
        target: A tracked document (`name`, `Model/name`, `Model:name`, tracked path) or a project node id.
        pythonpath: Unused by the read; accepted so callers pass what they pass `rewrite_references`.

    Raises:
        SLDBDocumentTargetError: `target` names no document and no project node, or several documents.
    """
    location = open_store(store, mode="readonly")
    graph = optional_graph(location.store_path)
    return [referrer for referrer, _ in find_hits(location, resolve_target(location, graph, target), graph)]


def resolve_target(location: StoreLocation, graph: ProjectGraph | None, given: str) -> Target:
    """A tracked document first, then a project node id; else `SLDBDocumentTargetError`."""
    found = matching_documents(location.store_path, given)
    if len(found) > 1:
        candidates = ", ".join(f"{d['model']}:{d['name']}" for d in found)
        raise SLDBDocumentTargetError(f"Ambiguous document target: {given} (candidates: {candidates})")
    if found:
        document = found[0]
        return Target(given, document["model"], document["name"], document["path"], node_id_of_path(graph, document["path"]))
    if graph is not None and given in graph.nodes.lookup.by_id:
        return Target(given, None, None, None, given)
    raise SLDBDocumentTargetError(f"Unknown document target: {given}")


def matching_documents(store_path: Path, ref: str) -> list[dict[str, str]]:
    """The tracked documents `ref` names by name, `Model/name`, `Model:name` or tracked path."""
    ref = ref.strip().strip("/")
    return [d for d in indexed_documents(store_path) if matches_doc_ref(ref, d["name"], d["path"], d["model"]) or ref == f"{d['model']}:{d['name']}"]


def optional_graph(store_path: Path) -> ProjectGraph | None:
    """The declared project graph, or None when the store declares none (then there are no mentions)."""
    try:
        return project_graph(store_path)
    except (SLDBStoreError, FileNotFoundError):
        return None


def node_id_of_path(graph: ProjectGraph | None, path: str) -> str | None:
    """The project node whose file is `path`, when the graph has one."""
    node = graph.nodes.lookup.by_path.get(path) if graph is not None else None
    return node.id if node is not None else None


def find_hits(location: StoreLocation, target: Target, graph: ProjectGraph | None) -> list[Hit]:
    """Field hits (with the value as written) then mention hits (value found when rewriting)."""
    hits = schema_hits(location.store_path, target.export_id) if target.export_id else []
    if graph is not None and target.node_id:
        hits += mention_hits(graph, target.node_id)
    return hits

FILE:src/sldb/api/edges/rewrite_references.py
"""`sldb.api.rewrite_references(store, target, replacement, *, transaction=None, dry_run=False,
pythonpath=None)` (GD22): every incoming reference of `target` (what `referrers` finds) rewritten to
name `replacement`, or removed when it is None, inside one `sldb.api.transaction` of GD24 (the one
given or its own): a write that fails puts every document back (docs/architecture/references.md).
A scalar field takes the new value (None removes it: the model decides whether it may be null); a
list field has the element replaced in place, or dropped, never duplicated; a mention has the
captured text replaced on its line (`rewrite_mentions`) through `replace_text`. Every new payload
and text is validated in memory first; with `dry_run` that is all: nothing is opened for writing
and the `on_write` rules do not run.
"""

from __future__ import annotations

from contextlib import nullcontext
from pathlib import Path
from typing import Any

from sldb.api.documents.document_payload import runtime_document
from sldb.api.documents.replace_text import replace_text
from sldb.api.documents.transaction import Transaction, transaction as open_transaction
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.referrers import Hit, Target, find_hits, matching_documents, optional_graph, resolve_target
from sldb.api.edges.rewrite_mentions import rewritten_text
from sldb.api.edges.rewrite_report import RewriteReport
from sldb.api.edges.rewrite_values import rewritten_payload
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from sldb.runtime.validation import validate_model_data_roundtrip, validate_model_input_roundtrip
from sldb.store.source_guard import aggregate_text

Plan = tuple[str, dict[str, Any], list[dict[str, Any]]]
TextPlan = tuple[str, str, str, list[dict[str, Any]], list[dict[str, Any]]]


def rewrite_references(store: str | Path | None, target: str, replacement: str | None, *, transaction: Transaction | None = None, dry_run: bool = False, pythonpath: str | None = None) -> RewriteReport:
    """Rewrite (or remove) every reference to `target` (what `referrers` accepts); see the module.

    `replacement` is resolved like `target` (a document keeps each value's form), written as given
    when it names nothing, None to remove. `transaction` is an open one over `store` to join.
    Raises `SLDBDocumentTargetError` (unknown or ambiguous target, ambiguous replacement) and
    `SLDBValidationError` (a rewritten payload or text the model refuses); nothing is written then.
    """
    location = open_store(store, mode="readonly" if dry_run else "default")
    graph = optional_graph(location.store_path)
    found = resolve_target(location, graph, target)
    new = None if replacement is None else replacement_target(location, graph, replacement)
    fields, mentions = _grouped(find_hits(location, found, graph))
    plans = [_planned_payload(location, pythonpath, export_id, hits, found, new) for export_id, hits in fields.items()]
    texts = [_planned_text(location, graph, pythonpath, path, hits, found, new) for path, hits in mentions.items()]
    if not dry_run:
        _write(location, pythonpath, transaction, plans, [(path, hits) for path, hits in mentions.items() if new is not None], graph, found, new)
    return RewriteReport(changed=[c for plan in plans for c in plan[2]] + [c for text in texts for c in text[3]], skipped=[s for text in texts for s in text[4]])


def replacement_target(location: StoreLocation, graph: ProjectGraph | None, given: str) -> Target:
    """`given` resolved like a target; when it names nothing it is kept literal (an ambiguous one is still an error)."""
    try:
        return resolve_target(location, graph, given)
    except SLDBDocumentTargetError as exc:
        if "Ambiguous" in str(exc):
            raise
        return Target(given, None, None, None, None)


def _grouped(hits: list[Hit]) -> tuple[dict[str, list[Hit]], dict[str, list[Hit]]]:
    fields: dict[str, list[Hit]] = {}
    mentions: dict[str, list[Hit]] = {}
    for hit in hits:
        (fields if hit[0].origin == "schema" else mentions).setdefault(hit[0].source, []).append(hit)
    return fields, mentions


def _planned_payload(location: StoreLocation, pythonpath: str | None, export_id: str, hits: list[Hit], target: Target, replacement: Target | None) -> Plan:
    """(path, new payload, changes) of one referring document, its payload validated under its model."""
    doc = runtime_document(location.store_path, pythonpath, export_id.replace(":", "/", 1))
    payload, changes = rewritten_payload(dict(doc.payload), [(r, v) for r, v in hits if v is not None], target, replacement)
    _check(export_id, _model_type(location, pythonpath, doc.model_name), payload, None)
    return doc.path, payload, changes


def _planned_text(location: StoreLocation, graph: ProjectGraph | None, pythonpath: str | None, path: str, hits: list[Hit], target: Target, replacement: Target | None) -> TextPlan:
    """(path, text, new text, changes, skips) of one mentioning file, a tracked document's new text validated."""
    if (text := aggregate_text(location.project_root, location.project_root / path, path)) is None:
        return path, "", "", [], [{"source": path, "location": None, "reason": "not read: the path resolves outside the project root or is a symlink"}]
    new_text, changes, skips = rewritten_text(text, graph, path, hits, target, replacement)
    for document in matching_documents(location.store_path, path) if new_text != text else []:
        _check(f"{document['model']}:{document['name']}", _model_type(location, pythonpath, document["model"]), None, new_text)
    return path, text, new_text, changes, skips


def _model_type(location: StoreLocation, pythonpath: str | None, model: str) -> type:
    return load_registered_model(location.store_path, model, pythonpath).model_type


def _check(node: str, model_type: type, payload: dict[str, Any] | None, text: str | None) -> None:
    """The new payload (or text) must validate and round-trip under the model, else `SLDBValidationError` and nothing is written."""
    try:
        valid, details = validate_model_data_roundtrip(model_type, payload) if payload is not None else validate_model_input_roundtrip(model_type, text or "")
    except (ValueError, TypeError) as exc:
        raise SLDBValidationError(f"{node}: the rewritten document does not validate under {model_type.__name__}: {exc}") from exc
    if not valid:
        raise SLDBValidationError(f"{node}: the rewritten document does not round-trip under {model_type.__name__}; nothing written", details)


def _write(location: StoreLocation, pythonpath: str | None, transaction: Transaction | None, plans: list[Plan], mentions: list[tuple[str, list[Hit]]], graph: ProjectGraph | None, target: Target, replacement: Target | None) -> None:
    """Payloads first, then each mentioning file re-read (a document may be both) and rewritten through `replace_text`."""
    with nullcontext(transaction) if transaction is not None else open_transaction(location.store_path, pythonpath) as tx:
        for path, payload, _ in plans:
            tx.update(path, payload)
        for path, hits in mentions:
            _, text, new_text, _, _ = _planned_text(location, graph, pythonpath, path, hits, target, replacement)
            if new_text != text:
                replace_text(location.store_path, path, text, new_text, count=1, transaction=tx, pythonpath=pythonpath)

FILE:tests/api/test_referrers.py
"""GD22: `sldb.api.referrers` and `sldb edges referrers` (docs/architecture/references.md).

A card A is referenced by B (scalar field `about`), by C (list field `related`, among two other
values, and a mention in its body), by a review R (a `__doc_anchors__` field) and by an
untracked note D (a mention in prose the project graph's `MentionPattern` captures). The
references come from the edge index (fields) and from the project graph (mentions); nothing
walks the project once both are warm.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.edges.project_graph import DocumentSurface, LineMentions, MentionPattern, ProjectGraphConfig
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import save_declaration
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError

MODULE = "sldb_gd22_reference_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Card(StructuredNLDoc):
    __references__ = ["about", "related"]
    __reference_models__ = {"about": ["Card"], "related": ["Card"]}
    __template__ = "---\\nid: ⸢rev•id⸥\\nabout: ⸢optrev•about⸥\\nrelated: ⸢rev,list•related⸥\\n---\\n\\n# ⸢rev•title⸥\\n\\n⸢rev•body⸥"
    id: str = Field(description="Card id.")
    title: str = Field(description="Title.")
    about: str | None = Field(default=None, description="The card this one is about.")
    related: list[str] = Field(default_factory=list, description="Related cards.")
    body: str = Field(default="", description="Body.")


class Review(StructuredNLDoc):
    __doc_anchors__ = ["subject"]
    __template__ = "---\\nsubject: ⸢optrev•subject⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subject: str | None = Field(default=None, description="The reviewed card.")


class Strict(StructuredNLDoc):
    __references__ = ["about"]
    __reference_models__ = {"about": ["Card"]}
    __template__ = "---\\nabout: ⸢rev•about⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    about: str = Field(description="A card; never null.")
'''

CONFIG = ProjectGraphConfig(
    document_extractor="docs_v1", file_extractor="files_v1", edge_extractor="edges_v1",
    surfaces=(DocumentSurface(kind="card", directory="cards", pattern="*.md", identity="document_id"), DocumentSurface(kind="note", directory="notes", pattern="*.md")),
    fields_by_model={"Card": ("about", "related")},
    kind_by_model={"Card": "card"},
    line_mentions=(LineMentions(kinds=("card", "note"), patterns=(MentionPattern(regex=r"card:[a-z0-9-]+", target="{0}"),), role="mentions", locator="prose"),),
)
D_TEXT = "# D\n\nSee card:card-a and card:card-ab, not card:card-a2.\n"


class World:
    """The store of the module docstring, with `project_graph` declared in its `store.yaml`."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Card", "Review", "Strict"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        self.card("card-a", "Card A")
        self.card("card-a2", "Card A2")
        self.card("card-b", "Card B", about="card-a")
        self.card("card-c", "Card C", related=["card-x", "card-a", "card-z"], body="Also card:card-a.")
        api.create_document(self.store, "Review", self.root / "reviews" / "r1.md", {"title": "R1", "subject": "doc:Card:card-a"}, "r1", self.py)
        (self.root / "notes").mkdir()
        (self.root / "notes" / "d.md").write_text(D_TEXT, encoding="utf-8")
        save_declaration(self.store, declare_store(self.store, self.root).model_copy(update={"project_graph": CONFIG.to_mapping()}))

    def card(self, name: str, title: str, **fields) -> None:
        api.create_document(self.store, "Card", self.root / "cards" / f"{name}.md", {"id": name, "title": title, **fields}, name, self.py)

    def payload(self, export_id: str) -> dict:
        return api.edge_node(self.store, export_id).payload

    def text(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def digests(self) -> dict[str, str]:
        files = sorted(p for p in self.root.rglob("*") if p.is_file() and ".sldb" in p.parts or p.suffix == ".md")
        return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

    def cli(self, capsys, *argv: str) -> tuple[int, object]:
        code = main(["--envelope", "edges", *argv, "--store", str(self.store), "--pythonpath", self.py, "--format", "json"])
        return code, json.loads(capsys.readouterr().out)


@pytest.fixture
def reference_world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


EXPECTED = [
    {"source": "Card:card-b", "field": "about", "index": None, "location": None, "origin": "schema"},
    {"source": "Card:card-c", "field": "related", "index": 1, "location": None, "origin": "schema"},
    {"source": "Review:r1", "field": "subject", "index": None, "location": None, "origin": "schema"},
    {"source": "cards/card-c.md", "field": None, "index": None, "location": "cards/card-c.md:16", "origin": "mention"},
    {"source": "notes/d.md", "field": None, "index": None, "location": "notes/d.md:3", "origin": "mention"},
]


def test_referrers_gives_the_fields_with_their_positions_and_the_mentions_with_their_lines(reference_world: World) -> None:
    found = [referrer.to_dict() for referrer in api.referrers(reference_world.store, "card-a")]
    assert found == EXPECTED
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a2")] == [{**EXPECTED[4]}]  # D also says `card:card-a2`


@pytest.mark.parametrize("target", ["Card/card-a", "Card:card-a", "cards/card-a.md"])
def test_a_tracked_document_is_named_by_name_export_id_model_name_or_path(reference_world: World, target: str) -> None:
    assert [r.to_dict() for r in api.referrers(reference_world.store, target)] == EXPECTED


def test_a_project_node_id_resolves_after_the_documents_and_has_only_mentions(reference_world: World) -> None:
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card:card-a")] == EXPECTED[3:]
    with pytest.raises(SLDBDocumentTargetError, match="Unknown document target: nope"):
        api.referrers(reference_world.store, "nope")


def test_an_ambiguous_target_names_its_candidates(reference_world: World) -> None:
    api.create_document(reference_world.store, "Review", reference_world.root / "reviews" / "card-a.md", {"title": "Same name"}, "card-a", reference_world.py)
    with pytest.raises(SLDBDocumentTargetError, match=r"Ambiguous document target: card-a \(candidates: Card:card-a, Review:card-a\)"):
        api.referrers(reference_world.store, "card-a")
    assert [r.source for r in api.referrers(reference_world.store, "Card:card-a")] == [r["source"] for r in EXPECTED]


def test_a_store_without_a_project_graph_has_only_the_fields(reference_world: World) -> None:
    declared = declare_store(reference_world.store, reference_world.root)  # keeps the authored project_graph (H5): the test removes it
    save_declaration(reference_world.store, declared.model_copy(update={"project_graph": None}))
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a")] == EXPECTED[:3]


def test_an_anchor_pinned_on_save_is_still_a_field_reference(reference_world: World) -> None:
    api.save_document_payload(reference_world.store, "Review", "r1", {"title": "R1", "subject": "doc:Card:card-a"}, reference_world.py)
    subject = reference_world.payload("Review:r1")["subject"]
    assert subject.startswith("doc:Card:card-a@sha256:") and len(subject) == len("doc:Card:card-a@sha256:") + 64
    assert [r.field for r in api.referrers(reference_world.store, "card-a") if r.source == "Review:r1"] == ["subject"]


def count_walks(monkeypatch: pytest.MonkeyPatch, root: Path) -> dict[str, int]:
    """Count `os.walk`, `Path.rglob` and `os.scandir` outside the store (q17: the shards signature stat-scans `.sldb_cache/edges`)."""
    counts = {"walk": 0, "rglob": 0, "scandir": 0}
    walk, rglob, scandir = os.walk, Path.rglob, os.scandir

    def counted_walk(*args, **kwargs):
        counts["walk"] += 1
        return walk(*args, **kwargs)

    def counted_rglob(self, *args, **kwargs):
        counts["rglob"] += 1
        return rglob(self, *args, **kwargs)

    def counted_scandir(path=".", *args, **kwargs):
        counts["scandir"] += not any(part.startswith(".sldb") for part in Path(str(path)).parts)
        return scandir(path, *args, **kwargs)

    monkeypatch.setattr(os, "walk", counted_walk)
    monkeypatch.setattr(Path, "rglob", counted_rglob)
    monkeypatch.setattr(os, "scandir", counted_scandir)
    return counts


def test_with_the_index_and_the_graph_warm_referrers_walks_nothing(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    api.referrers(reference_world.store, "card-a")
    counts = count_walks(monkeypatch, reference_world.root)
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a")] == EXPECTED
    assert counts == {"walk": 0, "rglob": 0, "scandir": 0}


def test_the_cli_prints_the_list_and_the_envelope_wraps_it(reference_world: World, capsys) -> None:
    assert main(["edges", "referrers", "card-a", "--store", str(reference_world.store), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out) == EXPECTED
    code, envelope = reference_world.cli(capsys, "referrers", "card:card-a")
    assert (code, envelope["ok"], envelope["data"]) == (0, True, EXPECTED[3:])
    code, envelope = reference_world.cli(capsys, "referrers", "nope")
    assert (code, envelope["error"]["type"]) == (1, "docs/missing")
    assert main(["edges", "referrers", "card-a", "--store", str(reference_world.store)]) == 0
    assert capsys.readouterr().out.splitlines() == ["schema: Card:card-b .about", "schema: Card:card-c .related[1]", "schema: Review:r1 .subject", "mention: cards/card-c.md:16", "mention: notes/d.md:3"]

FILE:tests/api/test_rewrite_references.py
"""GD22: `sldb.api.rewrite_references` and `sldb edges rewrite` (docs/architecture/references.md).

On the world of `test_referrers`: rewriting A to A2 leaves B and C pointing at A2 (C keeps its
order and its other values), the anchor of R unpinned so the save pins it again, and the
mentions of C and D rewritten as whole tokens; removing empties B, drops the element of C and
keeps the prose (skipped); a failure injected while C is written reverts B; a dry run changes
no byte and runs no `on_write` rule; nothing walks the project once the index and the graph
are warm; the same transaction can be joined.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sldb import api
from sldb.api.documents import payload_save, transaction_ops
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from tests.api.test_referrers import EXPECTED, World, count_walks, reference_world  # noqa: F401 - fixture

A2_CHANGES = [
    {"source": "Card:card-b", "field": "about", "index": None, "location": None, "before": "card-a", "after": "card-a2"},
    {"source": "Card:card-c", "field": "related", "index": 1, "location": None, "before": "card-a", "after": "card-a2"},
    {"source": "Review:r1", "field": "subject", "index": None, "location": None, "before": "doc:Card:card-a", "after": "doc:Card:card-a2"},
    {"source": "cards/card-c.md", "field": None, "index": None, "location": "cards/card-c.md:16", "before": "card:card-a", "after": "card:card-a2"},
    {"source": "notes/d.md", "field": None, "index": None, "location": "notes/d.md:3", "before": "card:card-a", "after": "card:card-a2"},
]


def test_rewriting_to_another_document_moves_every_field_and_mention_keeping_their_forms(reference_world: World) -> None:
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert report.to_dict() == {"changed": A2_CHANGES, "skipped": []}
    assert reference_world.payload("Card:card-b")["about"] == "card-a2"
    assert reference_world.payload("Card:card-c")["related"] == ["card-x", "card-a2", "card-z"]
    assert reference_world.payload("Card:card-c")["body"] == "Also card:card-a2."
    assert reference_world.text("notes/d.md") == "# D\n\nSee card:card-a2 and card:card-ab, not card:card-a2.\n"
    subject = reference_world.payload("Review:r1")["subject"]
    assert subject.startswith("doc:Card:card-a2@sha256:") and len(subject) == len("doc:Card:card-a2@sha256:") + 64
    assert api.referrers(reference_world.store, "card-a") == []
    assert _without_lines(api.referrers(reference_world.store, "card-a2")) == _without_lines(EXPECTED)  # C was rendered again: its line may move


def _without_lines(found: list) -> list[dict]:
    rows = [r.to_dict() if hasattr(r, "to_dict") else dict(r) for r in found]
    return [{**row, "location": row["location"] and row["location"].rsplit(":", 1)[0]} for row in rows]


def test_removing_empties_the_scalar_drops_the_element_and_keeps_the_prose(reference_world: World) -> None:
    before_d = reference_world.text("notes/d.md")
    report = api.rewrite_references(reference_world.store, "card-a", None, pythonpath=reference_world.py)
    assert report.changed == [{**change, "after": None} for change in A2_CHANGES[:3]]
    assert [s["location"] for s in report.skipped] == ["cards/card-c.md:16", "notes/d.md:3"]
    assert all("never deleted" in s["reason"] for s in report.skipped)
    assert "about" not in reference_world.payload("Card:card-b") and "about:" not in reference_world.text("cards/card-b.md")
    assert reference_world.payload("Card:card-c")["related"] == ["card-x", "card-z"]
    assert "subject" not in reference_world.payload("Review:r1")
    assert reference_world.text("notes/d.md") == before_d and reference_world.payload("Card:card-c")["body"] == "Also card:card-a."
    assert _without_lines(api.referrers(reference_world.store, "card-a")) == _without_lines(EXPECTED[3:])


def test_a_scalar_the_model_does_not_let_be_null_refuses_the_removal_and_nothing_is_written(reference_world: World) -> None:
    api.create_document(reference_world.store, "Strict", reference_world.root / "strict" / "s1.md", {"title": "S1", "about": "card-a"}, "s1", reference_world.py)
    before = reference_world.digests()
    with pytest.raises(SLDBValidationError, match="Strict:s1: the rewritten document does not validate under Strict") as refused:
        api.rewrite_references(reference_world.store, "card-a", None, pythonpath=reference_world.py)
    assert "about" in str(refused.value)
    assert reference_world.digests() == before
    with pytest.raises(SLDBValidationError, match="Strict:s1"):
        api.rewrite_references(reference_world.store, "card-a", None, dry_run=True, pythonpath=reference_world.py)
    assert reference_world.digests() == before


def test_a_failure_injected_while_c_is_written_puts_b_back_bytes_entry_and_index(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    before, entry = reference_world.digests(), api.edge_node(reference_world.store, "Card:card-b").source_hash
    update = transaction_ops.update

    def failing_update(state, ref, payload, expected_source_hash, expected):
        if str(ref).endswith("card-c.md"):
            raise RuntimeError("disk full while writing C")
        return update(state, ref, payload, expected_source_hash, expected)

    monkeypatch.setattr(transaction_ops, "update", failing_update)
    with pytest.raises(RuntimeError, match="disk full"):
        api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert reference_world.digests() == before
    assert reference_world.payload("Card:card-b")["about"] == "card-a" and api.edge_node(reference_world.store, "Card:card-b").source_hash == entry
    assert [r.to_dict() for r in api.referrers(reference_world.store, "card-a")] == EXPECTED


def test_a_dry_run_reports_the_same_changes_writes_no_byte_and_runs_no_on_write_rule(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    check = payload_save.check_rules_on_write
    monkeypatch.setattr(payload_save, "check_rules_on_write", lambda *args: calls.append(args[2]) or check(*args))
    before = reference_world.digests()
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", dry_run=True, pythonpath=reference_world.py)
    assert report.to_dict() == {"changed": A2_CHANGES, "skipped": []}
    assert reference_world.digests() == before and calls == []
    assert api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py).to_dict() == report.to_dict()
    assert reference_world.digests() != before and sorted(calls) == ["Card:card-b", "Card:card-c", "Review:r1"]


def test_with_the_index_and_the_graph_warm_a_dry_run_walks_nothing(reference_world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    api.rewrite_references(reference_world.store, "card-a", "card-a2", dry_run=True, pythonpath=reference_world.py)
    counts = count_walks(monkeypatch, reference_world.root)
    assert api.rewrite_references(reference_world.store, "card-a", "card-a2", dry_run=True, pythonpath=reference_world.py).changed == A2_CHANGES
    assert counts == {"walk": 0, "rglob": 0, "scandir": 0}


@pytest.mark.parametrize("before, after", [("Card:card-a", "Card:card-a2"), ("cards/card-a.md", "cards/card-a2.md"), ("`card-a`", "card-a2")])
def test_a_value_keeps_the_form_it_named_the_target_in(reference_world: World, before: str, after: str) -> None:
    reference_world.card("card-f", "Card F", about=before)
    api.rewrite_references(reference_world.store, "card-a", "Card/card-a2", pythonpath=reference_world.py)
    assert reference_world.payload("Card:card-f")["about"] == after


def test_a_replacement_that_is_no_document_is_written_as_given_and_an_ambiguous_one_is_refused(reference_world: World) -> None:
    with pytest.raises(SLDBValidationError, match="Review:r1: the rewritten document does not validate") as refused:
        api.rewrite_references(reference_world.store, "card-a", "card-elsewhere", pythonpath=reference_world.py)
    assert "is not a document anchor" in str(refused.value)  # an anchor field only takes `doc:Model:name`
    api.delete_document(reference_world.store, "r1", reference_world.py)
    api.rewrite_references(reference_world.store, "card-a", "card-elsewhere", pythonpath=reference_world.py)
    assert reference_world.payload("Card:card-b")["about"] == "card-elsewhere" and reference_world.payload("Card:card-c")["body"] == "Also card-elsewhere."
    assert reference_world.text("notes/d.md") == "# D\n\nSee card-elsewhere and card:card-ab, not card:card-a2.\n"
    api.create_document(reference_world.store, "Review", reference_world.root / "reviews" / "card-a2.md", {"title": "Same name"}, "card-a2", reference_world.py)
    with pytest.raises(SLDBDocumentTargetError, match="Ambiguous document target: card-a2"):
        api.rewrite_references(reference_world.store, "card-b", "card-a2", pythonpath=reference_world.py)


def test_a_list_never_duplicates_the_replacement(reference_world: World) -> None:
    reference_world.card("card-g", "Card G", related=["card-a2", "card-a", "card-a"])
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert reference_world.payload("Card:card-g")["related"] == ["card-a2"]
    assert [c["index"] for c in report.changed if c["source"] == "Card:card-g"] == [1, 1]


def test_a_mention_whose_token_is_gone_from_its_line_is_skipped(reference_world: World) -> None:
    (reference_world.root / "notes" / "d.md").write_text("# D\n\nSee card:card-ab only.\n", encoding="utf-8")
    api.project_graph(reference_world.store)  # the graph notices the file moved; the index did not change
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert [c["source"] for c in report.changed] == ["Card:card-b", "Card:card-c", "Review:r1", "cards/card-c.md"]
    assert report.skipped == [] and reference_world.text("notes/d.md") == "# D\n\nSee card:card-ab only.\n"


def test_sentence_dots_after_a_token_are_punctuation_but_a_dot_inside_one_is_not(reference_world: World) -> None:
    """q16 and q18: `card:card-a.` and `card:card-a...` are the token plus punctuation; `card:card-a.b` and `card:card-ab` are other tokens."""
    (reference_world.root / "notes" / "e.md").write_text("Ver card:card-a. Luego card:card-a... y card:card-a.b o card:card-ab, nunca.\n", encoding="utf-8")
    report = api.rewrite_references(reference_world.store, "card-a", "card-a2", pythonpath=reference_world.py)
    assert reference_world.text("notes/e.md") == "Ver card:card-a2. Luego card:card-a2... y card:card-a.b o card:card-ab, nunca.\n"
    assert [c for c in report.changed if c["source"] == "notes/e.md"] == [{"source": "notes/e.md", "field": None, "index": None, "location": "notes/e.md:1", "before": "card:card-a", "after": "card:card-a2"}]
    assert report.skipped == []


def test_the_call_joins_the_transaction_it_receives_and_the_outermost_one_rolls_back(reference_world: World) -> None:
    before = reference_world.digests()
    with pytest.raises(RuntimeError, match="later"):
        with api.transaction(reference_world.store, reference_world.py) as tx:
            api.rewrite_references(reference_world.store, "card-a", "card-a2", transaction=tx, pythonpath=reference_world.py)
            assert reference_world.payload("Card:card-b")["about"] == "card-a2"
            raise RuntimeError("something later fails")
    assert reference_world.digests() == before and reference_world.payload("Card:card-b")["about"] == "card-a"


def test_the_cli_rewrites_removes_and_dry_runs_with_the_envelope(reference_world: World, capsys) -> None:
    before = reference_world.digests()
    code, envelope = reference_world.cli(capsys, "rewrite", "card-a", "--to", "card-a2", "--dry-run")
    assert (code, envelope["ok"], envelope["data"]) == (0, True, {"changed": A2_CHANGES, "skipped": []}) and reference_world.digests() == before
    assert main(["edges", "rewrite", "card-a", "--remove", "--store", str(reference_world.store), "--pythonpath", reference_world.py, "--format", "json"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert [c["after"] for c in printed["changed"]] == [None, None, None] and len(printed["skipped"]) == 2
    assert reference_world.payload("Card:card-c")["related"] == ["card-x", "card-z"]
    code, envelope = reference_world.cli(capsys, "rewrite", "nope", "--to", "x")
    assert (code, envelope["error"]["type"]) == (1, "docs/missing")


@pytest.mark.parametrize("argv", [["card-a"], ["card-a", "--to", "x", "--remove"]])
def test_to_and_remove_exclude_each_other_and_one_is_required(reference_world: World, argv: list[str], capsys) -> None:
    assert main(["edges", "rewrite", *argv, "--store", str(reference_world.store)]) == 2
    err = capsys.readouterr().err
    assert "one of the arguments --to --remove is required" in err or "not allowed with argument" in err
    code, envelope = reference_world.cli(capsys, "rewrite", *argv)
    assert (code, envelope["error"]["type"]) == (6, "cli/usage")


def test_the_text_output_names_each_change(reference_world: World, capsys) -> None:
    assert main(["edges", "rewrite", "card-a", "--to", "card-a2", "--dry-run", "--store", str(reference_world.store), "--pythonpath", reference_world.py]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Card:card-b .about: 'card-a' -> 'card-a2'" and lines[-1] == "would change 5 reference(s), skipped 0"
    assert Path(reference_world.root / "cards" / "card-b.md").read_text(encoding="utf-8").count("card-a2") == 0

FILE:instruccion
Cold-bundle de la tarea task-referrers-y-rewrite-references-aceptan-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-duplican-men: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py

