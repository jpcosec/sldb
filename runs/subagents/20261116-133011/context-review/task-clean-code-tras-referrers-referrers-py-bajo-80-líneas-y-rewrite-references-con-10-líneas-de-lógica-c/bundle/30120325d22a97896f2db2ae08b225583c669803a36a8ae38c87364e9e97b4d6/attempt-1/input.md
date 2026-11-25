FILE:desk/tasks/task-clean-code-tras-referrers-referrers-py-bajo-80-líneas-y-rewrite-references-con-10-líneas-de-lógica-c.md
---
sldb:
  by: agent
  at: '2026-11-16T13:08:49Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-referrers-referrers-py-bajo-80-líneas-y-rewrite-references-con-10-líneas-de-lógica-c
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
- src/sldb/api/edges/referrers.py
- src/sldb/api/edges/rewrite_references.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
---

# Clean code tras referrers: referrers.py bajo 80 líneas y rewrite_references con 10 líneas de lógica como máximo

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: src/sldb/api/edges/referrers.py tiene 97 líneas efectivas (máximo 80) y la función rewrite_references de src/sldb/api/edges/rewrite_references.py tiene 15 líneas de lógica (máximo 10). Lo introdujo task-referrers-y-rewrite-references (3772a1fa); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-referrers-y-rewrite-references, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Mover document_paths, frontmatter_lines y _in_frontmatter de referrers.py a un módulo nuevo referrer_frontmatter.py del paquete sldb.api.edges (reexportar document_paths y frontmatter_lines desde referrers.py); partir rewrite_references en pasos con nombre (resolver grafo y exclusiones, planificar, escribir) dentro de rewrite_references.py o en un módulo vecino. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py
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

FILE:desk/atoms/atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent.md
---
sldb:
  by: agent
  at: '2026-11-16T11:31:46Z'
  authority: generated
  via: create_document
id: atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
title: referrers y rewrite_references trabajan sobre un grafo armado en proceso, excluyen
  fuentes y no cuentan dos veces un campo del frontmatter
five_wh_one_plus: what
tags:
- system:sldb
- topic:references
provenance: src/sldb/api/edges/referrers.py
---

# referrers y rewrite_references trabajan sobre un grafo armado en proceso, excluyen fuentes y no cuentan dos veces un campo del frontmatter

## Answer

sldb.api.referrers(store, target, *, graph=g) y rewrite_references(..., graph=g, excluded_sources=[...]) usan el ProjectGraph que se les pasa en lugar del declarado en store.yaml. excluded_sources (rutas o Model:name, resueltos con resolve_target) deja esas fuentes intactas, en campos y en menciones. find_hits no devuelve como mención una línea del frontmatter de un documento que ya es hit schema. Así un consumidor como deskops, que arma su grafo en proceso, no tiene que recomponer la reescritura.

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

A caller that builds its project graph in process (no `project_graph` in its `store.yaml`)
passes it as `graph`; then it is used instead of the declared one. A mention on a frontmatter
line of a document that is already a `schema` referrer is that same field, so it is left out.
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


def referrers(store: str | Path | None, target: str, pythonpath: str | None = None, *, graph: ProjectGraph | None = None) -> list[Referrer]:
    """Every reference to `target`, fields first (by source, field and position), then mentions (by path and line).

    Args:
        store: The store (path, alias, or None to discover it).
        target: A tracked document (`name`, `Model/name`, `Model:name`, tracked path) or a project node id.
        pythonpath: Unused by the read; accepted so callers pass what they pass `rewrite_references`.
        graph: A project graph built in process, used instead of the one the store declares; None reads the declared one.

    Raises:
        SLDBDocumentTargetError: `target` names no document and no project node, or several documents.
    """
    location = open_store(store, mode="readonly")
    graph = graph if graph is not None else optional_graph(location.store_path)
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
    """Field hits (with the value as written) then mention hits (value found when rewriting).

    A mention on a frontmatter line of a document that has a field hit repeats that field: it is dropped.
    """
    hits: list[Hit] = list(schema_hits(location.store_path, target.export_id)) if target.export_id else []
    if graph is not None and target.node_id:
        mentions = mention_hits(graph, target.node_id)
        paths = document_paths(location.store_path)
        with_fields = {paths[r.source] for r, _ in hits if r.source in paths}
        frontmatters = {path: frontmatter_lines(location.project_root / path) for path in with_fields if any(r.source == path for r, _ in mentions)}
        hits += [(r, v) for r, v in mentions if not _in_frontmatter(r, frontmatters)]
    return hits


def document_paths(store_path: Path) -> dict[str, str]:
    """The tracked path (relative to the project) of every tracked document, by export id `Model:name`."""
    return {f"{d['model']}:{d['name']}": d["path"] for d in indexed_documents(store_path)}


def frontmatter_lines(file: Path) -> range:
    """The lines (from 1) of the frontmatter: the first line `---` through the next `---`, both included; empty when there is none."""
    try:
        lines = file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return range(0)
    if not lines or lines[0].strip() != "---":
        return range(0)
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    return range(1, end + 2) if end is not None else range(0)


def _in_frontmatter(referrer: Referrer, frontmatters: dict[str, range]) -> bool:
    lines = frontmatters.get(referrer.source)
    if not lines or referrer.location is None:
        return False
    line = referrer.location.rsplit(":", 1)[-1]
    return line.isdigit() and int(line) in lines

FILE:src/sldb/api/edges/rewrite_references.py
"""`sldb.api.rewrite_references(store, target, replacement, *, transaction=None, dry_run=False,
pythonpath=None, graph=None, excluded_sources=())` (GD22): every incoming reference of `target` (what `referrers` finds) rewritten to
name `replacement`, or removed when it is None, inside one `sldb.api.transaction` of GD24 (the one
given or its own): a write that fails puts every document back (docs/architecture/references.md).
A scalar field takes the new value (None removes it: the model decides whether it may be null); a
list field has the element replaced in place, or dropped, never duplicated; a mention has the
captured text replaced on its line (`rewrite_mentions`) through `replace_text`. Every new payload
and text is validated in memory first; with `dry_run` that is all: nothing is opened for writing
and the `on_write` rules do not run. `graph` is a project graph built in process, used instead of
the declared one; the documents named in `excluded_sources` are left untouched, fields and mentions.
"""

from __future__ import annotations

from contextlib import nullcontext
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from sldb.api.documents.document_payload import runtime_document
from sldb.api.documents.replace_text import replace_text
from sldb.api.documents.transaction import Transaction, transaction as open_transaction
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.referrers import Hit, Target, document_paths, find_hits, matching_documents, optional_graph, resolve_target
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


def rewrite_references(store: str | Path | None, target: str, replacement: str | None, *, transaction: Transaction | None = None, dry_run: bool = False, pythonpath: str | None = None, graph: ProjectGraph | None = None, excluded_sources: Iterable[str] = ()) -> RewriteReport:
    """Rewrite (or remove) every reference to `target` (what `referrers` accepts); see the module.

    `replacement` is resolved like `target` (a document keeps each value's form), written as given
    when it names nothing, None to remove. `transaction` is an open one over `store` to join.
    `graph` replaces the declared project graph when given. Each of `excluded_sources` names a
    tracked document like `target` does (`Model:name` and its path exclude the same one); its
    fields and mentions are not rewritten.
    Raises `SLDBDocumentTargetError` (unknown or ambiguous target, ambiguous replacement, an
    excluded source that names no tracked document) and `SLDBValidationError` (a rewritten
    payload or text the model refuses); nothing is written then.
    """
    location = open_store(store, mode="readonly" if dry_run else "default")
    graph = graph if graph is not None else optional_graph(location.store_path)
    found = resolve_target(location, graph, target)
    new = None if replacement is None else replacement_target(location, graph, replacement)
    excluded = excluded_paths(location, graph, excluded_sources)
    fields, mentions = _grouped(find_hits(location, found, graph))
    if excluded:
        paths = document_paths(location.store_path)
        fields = {source: hits for source, hits in fields.items() if paths.get(source) not in excluded}
        mentions = {path: hits for path, hits in mentions.items() if path not in excluded}
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


def excluded_paths(location: StoreLocation, graph: ProjectGraph | None, sources: Iterable[str]) -> set[str]:
    """The tracked paths (relative to the project) of the documents `sources` name; one that names no tracked document is `SLDBDocumentTargetError`."""
    paths: set[str] = set()
    for source in sources:
        resolved = resolve_target(location, graph, source)
        if resolved.path is None:
            raise SLDBDocumentTargetError(f"Excluded source is not a tracked document: {source}")
        paths.add(resolved.path)
    return paths


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

FILE:instruccion
Cold-bundle de la tarea task-clean-code-tras-referrers-referrers-py-bajo-80-líneas-y-rewrite-references-con-10-líneas-de-lógica-c: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

