FILE:desk/tasks/task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el.md
---
sldb:
  by: agent
  at: '2026-11-16T07:53:35Z'
  authority: generated
  via: save_document_payload
id: task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el
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
pills:
- desk/contexts/pill-pill-regla-de-aristas-en-el-test-de-on-write.md
files:
- src/sldb/api/rules/rules_on_write.py
- src/sldb/api/rules/rule_graph.py
- src/sldb/api/documents/payload_save.py
- src/sldb/core/finding_route.py
- tests/api/test_rules.py
- tests/api/test_on_write_entering.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-evaluates-declared-rules-consumers-author-them
from_drawer: desk/drawer/tasks/task-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura.md
---

# on_write: save_document_payload devuelve las alertas de la escritura y la regla ve las aristas que el payload nuevo declara

## Rationale

_Explain why this task exists or the business driver behind it._

Hallazgos de GO08 (H2, H3). (1) Las alertas de on_write viajan por sldb.core.finding_route (route en src/sldb/core/finding_route.py:24-27 no hace nada sin listener) y solo la CLI instala alert_sink: un programa que usa sldb.api sin instalar listener no las recibe; check_on_write (src/sldb/api/rules/rules_on_write.py:30-42) solo las manda por route y save_document_payload (src/sldb/api/documents/payload_save.py:15) devuelve un DocumentReference sin findings. La tarea task-apply-batch-aristas-validadas-antes-de-escribir-alertas-on-write-en-batchreport-rules-check-sobre-re cubre esto solo para apply_batch (BatchReport.alerts), no para guardar un documento. (2) RuleGraph.with_payload (src/sldb/api/rules/rule_graph.py:62-64) deja el modelo y las aristas del índice, así que una regla on_write ve las aristas de antes de la escritura. Origen: drawer desk/drawer/tasks/task-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura.md.

## Goal

_Describe the concrete result this task must produce._

save_document_payload devuelve en el DocumentReference un campo alerts: list[dict] con las alertas on_write de esa escritura (además de enviarlas por route como hoy), y una regla on_write cuya condición depende de una arista declarada por el payload nuevo la ve al evaluarse.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) check_on_write devuelve la lista de findings de nivel alert que emitió; save_document_payload la pone en un campo nuevo alerts del DocumentReference (opcional, lista vacía por defecto, para no romper a quien lo construye); route sigue recibiéndolas. (2) En RuleGraph.with_payload, construir las aristas salientes declaradas (__references__ y __doc_anchors__) del documento a partir del payload nuevo y reemplazar con ellas las del documento en el grafo que evalúa la regla; las demás aristas quedan como están. Tests en tests/api/test_rules.py (una regla on_write de nivel alert: save_document_payload la devuelve en alerts sin listener instalado) y tests/api/test_on_write_entering.py (una regla que exige una arista references: guardar un payload que la agrega pasa; uno que la quita da el finding). CHANGELOG.md. No entra: BatchReport.alerts de apply_batch (otra tarea), cambiar el nivel de las reglas existentes.

Precisiones (preflight-1): cada alerta es Finding.as_dict() (el mismo dict que devuelve rules_check), solo las de nivel alert; DocumentReference.alerts: list[dict[str, Any]] = Field(default_factory=list). Las aristas del payload nuevo se construyen con la misma función que usa el índice para un documento (declared_reference_edges de src/sldb/store/edge_index/declared_references.py y doc_anchor_edges de doc_anchor_edges.py) aplicada al payload nuevo; with_payload devuelve un RuleGraph nuevo (no muta el del índice) con las aristas salientes de ese documento reemplazadas. Test de alerta: una RuleDoc on_write de nivel alert con condición falsa para el payload; sin listener se asegura con monkeypatch sobre la lista de listeners de finding_route. Test de aristas: RuleDoc on_write de nivel error con condición "exists(references)" o equivalente en el lenguaje de reglas; guardar con la referencia pasa; quitarla da el finding con ese code.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer finding_route.py, rules_on_write.py, rule_graph.py (with_payload) y payload_save.py, más la clase DocumentReference (grep -rn "class DocumentReference" src/sldb). 2) Devolver findings desde check_on_write. 3) Agregar alerts a DocumentReference. 4) Aristas del payload nuevo en with_payload. 5) Tests y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_rules.py
- TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los tests nuevos; DocumentReference.alerts existe y viene vacía cuando no hay reglas; CHANGELOG y commit; aviso a deskops con deskops message send --to deskops.

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

FILE:desk/contexts/pill-pill-regla-de-aristas-en-el-test-de-on-write.md
---
sldb:
  by: agent
  at: '2026-11-16T07:53:14Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-regla-de-aristas-en-el-test-de-on-write
status: active
summary: regla de aristas en el test de on_write
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: regla de aristas en el test de on_write

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

docs/architecture/rules-language.md, tests/api/test_on_write_entering.py

## How

_Describe the correct way to apply this guidance._

El lenguaje no tiene exists(); la condición del test es count(<campo de referencia>: title != "") > 0 (si ese predicado no parsea, cualquier predicado sobre un campo del documento destino que los tests de tests/api/test_rules.py ya usen), con la forma count(camino: p) cmp término de docs/architecture/rules-language.md (líneas 36 y 127-135), sobre un campo declarado en __references__ del modelo de prueba. Las aristas salientes que el payload nuevo ya no declara se quitan del grafo de evaluación. DocumentReference (src/sldb/api/documents/document_reference.py) es pydantic: alerts: list[dict[str, Any]] = Field(default_factory=list). Para aislar listeners se usa monkeypatch.setattr sobre sldb.core.finding_route._LISTENERS (lista vacía). tests/api/test_rules_evaluation.py es solo regresión.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.

FILE:desk/atoms/atom-sldb-evaluates-declared-rules-consumers-author-them.md
---
id: atom-sldb-evaluates-declared-rules-consumers-author-them
title: sldb evaluates declared rules; consumers author them
five_wh_one_plus: what
tags:
- system:sldb
- system:deskops
- topic:boundary
- topic:rules
---

# sldb evaluates declared rules; consumers author them

## Answer

sldb evaluates declared rules over documents, edges and content hashes: a predicate language with quantifiers over relations, RuleDoc documents with a subject family, a severity and a moment, doc: anchors pinned to a contract hash, and transitions carried as edge data. Which rules exist, what a task type is and what a workflow gate means is authored by consumers such as deskops, as documents in their own desks; sldb only evaluates them, with an explanation, incrementally, and never persists a derived result. Owner decision D1 of 2026-11-04 (desk/drawer/plans/grafo-operable/decisiones.md); the generic evaluator lives in sldb, the specific rules outside it.

FILE:src/sldb/api/rules/rules_on_write.py
"""`on_write` (GO08, rules.md §9): the rules a write must pass before anything is persisted.

A step of `save_document_payload`, right after the document anchors are pinned (GO07): the rule
reads the pinned payload, with the anchors' states (`<field>__anchor_state`) as the index would
compose them; paths follow the index as it is before the write. An `error` finding refuses the
write (`SLDBRuleViolationError`, nothing written); alerts are routed (`sldb.core.finding_route`)
whether the write passes or not. The document and its neighbours enter the dirty set.
The built-in family `builtin:tag_namespace:*` (GD27) runs beside the RuleDocs, also in a store
that registers none but declares `tag_namespaces`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import model_type_of
from sldb.api.rules.builtin_tag_findings import family_findings
from sldb.api.rules.builtin_tag_rules import tag_rules
from sldb.api.rules.dirty_set import mark_dirty
from sldb.api.rules.rule_graph import rule_graph
from sldb.api.rules.rules_on_transition import has_rules, payload_findings
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.core.finding import split
from sldb.core.finding_route import route
from sldb.store.edge_index.doc_anchor_states import SUFFIX, field_states, store_current
from sldb.store.model_contract import doc_anchor_fields


def check_on_write(store_path: Path, model_type: type, node: str, payload: dict[str, Any]) -> None:
    """Evaluate the `on_write` rules on `node` (`Model:name`) as `payload`; raise on an error."""
    declared = has_rules(store_path)
    if not declared and not tag_rules(store_path):
        return
    graph, read = rule_graph(store_path, None), anchored(store_path, model_type, payload)
    found = payload_findings(graph, "on_write", node, read) if declared else []
    errors, alerts = split(found + family_findings(graph.with_payload(node, read), [node]))
    mark_dirty(store_path, graph.index, node)
    route(alerts)
    if errors:
        raise SLDBRuleViolationError(errors)


def anchored(store_path: Path, model_type: type, payload: dict[str, Any]) -> dict[str, Any]:
    """`payload` with the state of each of its `__doc_anchors__` fields, as the index adds it."""
    names = [name for name in doc_anchor_fields(model_type) if payload.get(name)]
    if not names:
        return payload
    current = store_current(store_path, model_type_of)
    return {**payload, **{name + SUFFIX: field_states(payload[name], current) for name in names}}

FILE:src/sldb/api/rules/rule_graph.py
"""The store a rule is evaluated over: its edge index, loaded once into the store's
`GraphBackend`, and which documents are the local store's own. The index holds the linked
stores, except for the rules' own evaluations (`rule_graph(store, None)`), which compose them
only when the rules may read them (`rule_reach`): otherwise the index is the store's own, and a
local document reads exactly as it would in the composed one.

`with_payload(node, payload)` is the same graph where `node` reads `payload` instead of its
projection (GO08: the payload a write is about to persist, or the subject a transition reads);
paths still follow the index's edges."""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import cached_property
from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph.analyze import backend_for
from sldb.api.rules.rule_reach import needs_linked
from sldb.api.stores.open_store import open_store
from sldb.store.edge_index.node_ids import bare, kind
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_api import node_finding
from sldb.store.graph.language.predicate_view import node as view_node, with_node


@dataclass(frozen=True)
class RuleGraph:
    """`eval` over one store: `holds` is the finding of a predicate on one document."""

    backend: Any
    index: Any
    local: frozenset[str]
    store_path: Path
    override: tuple[str, dict[str, Any]] | None = None
    linked: bool = True

    def holds(self, predicate: str, node: str) -> dict[str, Any]:
        """The eval finding (node, holds, clause, seen) of `predicate` on the document `node`."""
        if self.override is None or node != self.override[0]:
            return self.backend.eval(predicate, node)[0]
        view, item = self.located(node)
        return node_finding(predicate, view, item)

    def located(self, node: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """The graph view and the element of `node` an evaluation reads (the override's payload)."""
        known = self._view["node"](node) or self._unindexed(node)
        if self.override is None or node != self.override[0]:
            return self._view, known
        item = {**known, "payload": self.override[1]}
        return with_node(self._view, item), item

    def _unindexed(self, node: str) -> dict[str, Any]:
        """A document the index does not hold yet: its family from the store's model registry
        (`indexed_model_bases`, no class imported), so `model <= Base` reads as for an indexed one."""
        from sldb.api.stores.resolve_indexed_document import indexed_model_bases

        model = node.rsplit(":", 1)[0].rsplit(":", 1)[-1]
        return view_node(node, model, {}, indexed_model_bases(self.store_path).get(model, []))

    def with_payload(self, node: str, payload: dict[str, Any]) -> "RuleGraph":
        """This graph, with `node` reading `payload` (its model and edges stay the index's)."""
        return replace(self, override=(node, payload))

    @cached_property
    def index_documents(self) -> list[str]:
        """Every document of the index (the linked stores' too when `linked`), by export id."""
        return [bare(n.id) for n in self.index.nodes.values() if kind(n.id) == "document"]

    @cached_property
    def _view(self) -> dict[str, Any]:
        return index_view(self.index)

    def domain(self, predicate: str) -> list[str]:
        """The local documents `predicate` holds on, over its domain (rules-language.md §6)."""
        return [f["node"] for f in self.backend.eval(predicate) if f["holds"] == "true" and f["node"] in self.local]

    def semantics(self, node: str) -> dict[str, Any]:
        """What the index records of a document: its name, model and path."""
        record = self.index.node(node)
        return dict(record.semantics) if record is not None else {}

    def payload(self, node: str) -> dict[str, Any]:
        record = self.index.node(node)
        return dict(record.payload) if record is not None else {}


def rule_graph(store: str | Path | None, linked: bool | None = True) -> RuleGraph:
    """The store's graph with its linked stores, every document's projection loaded. With
    `linked` None (the rules' evaluations) they are composed only when the store's rules may
    read them (`rule_reach.needs_linked`); with False, never."""
    store_path = open_store(store, mode="readonly").store_path
    own = load_edge_index(store_path, False)
    local = _documents(own)
    if linked is None:
        graph = _loaded(own, local, store_path, False)
        linked = needs_linked(graph)
        if not linked:
            return graph
    return _loaded(load_edge_index(store_path, True) if linked else own, local, store_path, linked)


def reading(graph: RuleGraph, node: str) -> RuleGraph:
    """`graph`, or the store's graph with its linked stores when `node` is not a local document
    (a subject behind `alias:`): a rule on it reads what the composed index says."""
    return graph if graph.linked or node in graph.local else rule_graph(graph.store_path, True)


def _loaded(index: Any, local: frozenset[str], store_path: Path, linked: bool) -> RuleGraph:
    backend = backend_for(store_path)
    backend.load(index, {bare(n.id): n.payload for n in index.nodes.values() if kind(n.id) == "document"})
    return RuleGraph(backend, index, local, store_path, linked=linked)


def _documents(index: Any) -> frozenset[str]:
    return frozenset(bare(n.id) for n in index.nodes.values() if kind(n.id) == "document")

FILE:src/sldb/api/documents/payload_save.py
"""Write a whole payload back to a tracked document: render, round-trip, rehash, reindex."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.doc_anchor_pinning import pin_payload
from sldb.api.documents.payload_save_steps import check_rules_on_write, load_document_entry, load_model_indexes, model_class, render_checked, save_document_indexes, write_rendered_document
from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.stores.open_store import open_store


def save_document_payload(store: str | Path | None, model_name: str, document_name: str, payload: dict[str, Any], pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Replace a tracked document's content with the Markdown rendered from `payload`.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        model_name: Registered model name of the document.
        document_name: Tracked document name.
        payload: The complete new payload; it has no fixed schema beyond the model's own.
        pythonpath: Directory to import the model module from; the store's project root
            is tried next, since a linked store's models import from where it lives.
        actor: Optional caller label, stamped into the document's provenance block.

    Returns:
        The document written.

    Raises:
        SLDBPayloadSaveError: When the model or document is not registered, or the rendered
            Markdown does not round-trip back to the payload.
        SLDBStoreError: When a RuleDoc's subject names a model the store does not register.
        SLDBRuleViolationError: When an `on_write` rule of severity error fails on the payload
            (after its anchors are pinned); nothing is written.
    """
    location = open_store(store)
    idx, m_entry, m_idx = load_model_indexes(location.store_path, location.project_root, model_name)
    doc_entry = load_document_entry(location.store_path, m_entry.name, document_name)
    model_type = model_class(m_entry.model_ref, pythonpath, location.project_root)
    _save(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor)
    return DocumentReference(model=m_entry.name, name=doc_entry.name, path=location.project_root / doc_entry.path)


def _save(location, idx, m_idx, m_entry, doc_entry, model_type, payload, pythonpath, actor) -> None:
    payload = pin_payload(location.store_path, model_type, payload)
    check_rules_on_write(location.store_path, model_type, f"{m_entry.name}:{doc_entry.name}", payload)
    rendered = render_checked(model_type, payload, location.project_root)
    refuse_unknown_family(location.store_path, model_type, payload, pythonpath)
    write_rendered_document(location.project_root, doc_entry, model_type, rendered, actor=actor, store_path=location.store_path)
    save_document_indexes(location.store_path, location.project_root, idx, m_idx, m_entry, doc_entry, pythonpath, model_type)

FILE:src/sldb/core/finding_route.py
"""Where findings raised below the CLI go: the listeners the application installed (GO08).

The library reports what it finds while it works (an `on_write` rule's alerts, for one) by
`route(findings)`; it cannot import the CLI. The CLI installs `sldb.cli.alert_sink` as a
listener when it starts, so those findings print and reach the envelope's `warnings`. With no
listener (an embedding program that installed none) `route` does nothing.
"""

from __future__ import annotations

from typing import Callable

from sldb.core.finding import Finding

_LISTENERS: list[Callable[[list[Finding]], None]] = []


def listen(listener: Callable[[list[Finding]], None]) -> None:
    """Add `listener`, once: installing it again is a no-op."""
    if listener not in _LISTENERS:
        _LISTENERS.append(listener)


def route(findings: list[Finding]) -> None:
    """Hand `findings` to every listener; nothing to hand, nothing called."""
    for listener in list(_LISTENERS) if findings else []:
        listener(findings)

FILE:tests/api/test_rules.py
"""GO06: RuleDoc, `sldb rules check` and `sldb rules explain` (docs/architecture/rules.md).

The store has Base, X < Base, Y < X and Z < Base. A malformed RuleDoc is refused when written,
one test per field; the rest is the acceptance of the node.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb import api
from sldb.cli import main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBStoreError

MODULE = "sldb_go06_rule_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Base(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\ndepends_on: ⸢rev•depends_on⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    depends_on: str = Field(default="", description="Referenced document.")


class X(Base):
    pass


class Y(X):
    pass


class Z(Base):
    pass
'''
RULE = {"title": "closed", "subject": "model <= X", "condition": 'status = "closed"', "severity": "error", "moment": "on_check"}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Base", "X", "Y", "Z"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.add_model(self.store, "sldb.models.rule_doc:RuleDoc", self.py)
        api.init_relations(self.store, self.py)
        for model, name in (("X", "x1"), ("Y", "y1"), ("Z", "z1")):
            self.doc(model, name, {"title": name, "status": "open"})

    def doc(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def rule(self, name: str, **fields) -> None:
        api.create_document(self.store, "RuleDoc", self.root / "rules" / f"{name}.md", {**RULE, "title": name, **fields}, name, self.py)

    def cli(self, capsys, *argv: str) -> tuple[int, dict]:
        code = main(["--envelope", "rules", *argv, "--store", str(self.store), "--pythonpath", self.py, "--format", "json"])
        return code, json.loads(capsys.readouterr().out)


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _check(world: World, subject: str | None = None) -> list[tuple[str, str, str]]:
    return sorted((f.level, f.code, f.subject) for f in api.rules_check(world.store, subject, world.py))


def test_a_rule_about_x_applies_to_x_and_y_and_not_to_z(world: World) -> None:
    world.rule("closed")
    assert _check(world) == [("error", "rules/closed", "X:x1"), ("error", "rules/closed", "Y:y1")]
    assert _check(world, "Z:z1") == []


def test_check_reports_errors_and_alerts_with_clause_and_node_and_fails_only_on_error(world: World, capsys) -> None:
    world.rule("owner", severity="alert", subject="model <= Y", condition="has(depends_on)", message="sin dependencia")
    code, alert_only = world.cli(capsys, "check")
    assert (code, alert_only["ok"], alert_only["warnings"][0]["code"]) == (0, True, "rules/owner")
    world.rule("closed")
    code, envelope = world.cli(capsys, "check", "--subject", "Y:y1")
    found = {f["code"]: f for f in envelope["data"]["findings"]}
    assert (code, envelope["exit"], found["rules/owner"]["level"], found["rules/closed"]["level"]) == (1, 1, "alert", "error")
    assert found["rules/closed"]["subject"] == "Y:y1" and found["rules/closed"]["document"] == "y1.md"
    assert found["rules/closed"]["what"] == 'status = "closed" (seen: {"status":"open"})'
    assert found["rules/owner"]["what"] == "sin dependencia | has(depends_on) (seen: {\"depends_on\":\"\"})"


def test_check_without_subject_runs_only_on_check_rules(world: World) -> None:
    world.rule("later", moment="on_write")
    assert _check(world) == []
    assert _check(world, "X:x1") == [("error", "rules/later", "X:x1")]


def test_subject_accepts_model_name_and_path(world: World) -> None:
    world.rule("closed")
    assert _check(world, "Y:y1") == _check(world, "y1.md") == _check(world, str(world.root / "y1.md")) == [("error", "rules/closed", "Y:y1")]


def test_explain_returns_the_eval_finding_and_exits_by_its_value(world: World, capsys) -> None:
    world.rule("closed")
    world.rule("open", condition='status = "open"')
    world.rule("filtered", where='status = "closed"')
    code, holds = world.cli(capsys, "explain", "RuleDoc:open", "X:x1")
    assert (code, holds["data"]) == (0, {"rule": "RuleDoc:open", "subject": "X:x1", "finding": {"node": "X:x1", "holds": "true", "clause": 'status = "open"', "seen": {"status": "open"}}})
    code, fails = world.cli(capsys, "explain", "closed", "y1.md")
    assert (code, fails["data"]["finding"]["holds"]) == (1, "false")
    code, skipped = world.cli(capsys, "explain", str(world.root / "rules" / "filtered.md"), "X:x1")
    assert (code, skipped["data"]) == (3, {"rule": "RuleDoc:filtered", "subject": "X:x1", "applies": False, "reason": "where", "detail": 'status = "closed"'})
    assert api.rules_explain(world.store, "closed", "Z:z1", world.py)["reason"] == "subject"


def test_an_incomplete_result_is_an_alert_whatever_the_severity(world: World, capsys, monkeypatch) -> None:
    world.doc("X", "x2", {"title": "x2", "depends_on": "Z:z1"})
    api.rebuild_edges(world.store, world.py)
    world.rule("deps", condition='all(depends_on: status = "closed")')
    monkeypatch.setattr("sldb.api.rules.rule_graph.load_edge_index", _unavailable(api.load_edge_index))
    assert _check(world, "X:x2") == [("alert", "rules/deps/incomplete", "X:x2")]
    code, envelope = world.cli(capsys, "explain", "deps", "X:x2")
    assert (code, envelope["data"]["finding"]["holds"]) == (2, "incomplete")


def test_an_unknown_rule_or_subject_is_the_unknown_document_error(world: World, capsys) -> None:
    world.rule("closed")
    with pytest.raises(SLDBDocumentTargetError, match="Unknown document target: nope"):
        api.rules_explain(world.store, "nope", "X:x1", world.py)
    code, envelope = world.cli(capsys, "check", "--subject", "X:nope")
    assert (code, envelope["error"]["type"]) == (1, "docs/missing")


@pytest.mark.parametrize("field, value", [
    ("condition", "has("),
    ("where", 'status = "open" and'),
    ("severity", "warning"),
    ("moment", "nightly"),
    ("subject", 'model <= X or status = "open"'),
])
def test_a_malformed_rule_is_refused_when_written(world: World, field: str, value: str) -> None:
    with pytest.raises(ValidationError) as refused:
        world.rule("bad", **{field: value})
    assert [e["loc"] for e in refused.value.errors()] == [(field,)]
    assert not (world.root / "rules" / "bad.md").exists()


def test_a_rule_about_an_unregistered_model_is_refused_when_written(world: World) -> None:
    with pytest.raises(SLDBStoreError, match="Model 'Missing' not registered."):
        world.rule("bad", subject="model <= Missing")
    assert not (world.root / "rules" / "bad.md").exists()


def _unavailable(load):
    """`load_edge_index` whose `depends_on` edges reach an unavailable linked store (H4)."""

    def marked(index):
        class Index:
            def __getattr__(self, name):
                return getattr(index, name)

            def edges_from(self, export_id, relation=None):
                return [e.model_copy(update={"metadata": {**e.metadata, "unavailable": e.metadata.get("field") == "depends_on"}}) for e in index.edges_from(export_id, relation)]

        return Index()

    return lambda *args, **kwargs: marked(load(*args, **kwargs))

FILE:tests/api/test_on_write_entering.py
"""H4: `create_document` and `track_document_file` evaluate the `on_write` rules as a save does
(rules.md §9.1). An error refuses the document and nothing is written or tracked; `apply_batch`
and `transaction` inherit the refusal and restore the tree; `stores build` does not evaluate."""

from __future__ import annotations

import pytest

from sldb import api
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.runtime.validation import render_model_markdown
from tests.api.test_rules_evaluation import MODULE, World, world  # noqa: F401 - the fixture

OPEN, CLOSED = {"title": "x3", "status": "open"}, {"title": "x3", "status": "closed"}


def _tracked(world: World, name: str) -> bool:
    return api.edge_node(world.store, f"X:{name}") is not None


def _hand_written(world: World, name: str, payload: dict):
    model_type = api.resolve_model_ref(f"{MODULE}:X", world.py)
    path = world.root / f"{name}.md"
    path.write_text(render_model_markdown(model_type, payload) + "\n", encoding="utf-8")
    return path


def test_a_created_document_that_breaks_an_on_write_rule_is_refused_and_nothing_is_written(world: World) -> None:
    world.rule("closed", moment="on_write")
    with pytest.raises(SLDBRuleViolationError, match="rules/closed"):
        world.doc("X", "x3", OPEN)
    assert not (world.root / "x3.md").exists() and not _tracked(world, "x3")


def test_a_created_document_that_passes_is_written_and_tracked(world: World) -> None:
    world.rule("closed", moment="on_write")
    world.doc("X", "x3", CLOSED)
    assert (world.root / "x3.md").exists() and _tracked(world, "x3")


def test_a_tracked_file_that_breaks_an_on_write_rule_is_refused_and_not_tracked(world: World) -> None:
    world.rule("closed", moment="on_write")
    path = _hand_written(world, "x3", OPEN)
    with pytest.raises(SLDBRuleViolationError, match="rules/closed"):
        api.track_document_file(world.store, "X", path, "x3", world.py)
    assert path.exists() and not _tracked(world, "x3")


def test_a_tracked_file_that_passes_is_tracked(world: World) -> None:
    world.rule("closed", moment="on_write")
    api.track_document_file(world.store, "X", _hand_written(world, "x3", CLOSED), "x3", world.py)
    assert _tracked(world, "x3")


def test_apply_batch_inherits_the_refusal_and_leaves_the_tree_as_it_was(world: World) -> None:
    world.rule("closed", moment="on_write")
    changes = [{"id": "x3", "action": "create", "model": "X", "payload": CLOSED}, {"id": "x4", "action": "create", "model": "X", "payload": {**OPEN, "title": "x4"}}]
    with pytest.raises(SLDBRuleViolationError):
        api.apply_batch(world.store, changes, world.py)
    assert not any((world.root / f"{name}.md").exists() or _tracked(world, name) for name in ("x3", "x4"))


def test_transaction_create_inherits_the_refusal_and_restores_the_tree(world: World) -> None:
    world.rule("closed", moment="on_write")
    with pytest.raises(SLDBRuleViolationError), api.transaction(world.store, world.py) as tx:
        tx.create("X", "x3", CLOSED, world.root / "x3.md")
        tx.create("X", "x4", {**OPEN, "title": "x4"}, world.root / "x4.md")
    assert not any((world.root / f"{name}.md").exists() or _tracked(world, name) for name in ("x3", "x4"))


def test_a_store_without_on_write_rules_creates_as_before(world: World) -> None:
    world.rule("closed")
    world.doc("X", "x3", OPEN)
    assert _tracked(world, "x3")

FILE:instruccion
Cold-bundle de la tarea task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_rules.py
- TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rules_evaluation.py

