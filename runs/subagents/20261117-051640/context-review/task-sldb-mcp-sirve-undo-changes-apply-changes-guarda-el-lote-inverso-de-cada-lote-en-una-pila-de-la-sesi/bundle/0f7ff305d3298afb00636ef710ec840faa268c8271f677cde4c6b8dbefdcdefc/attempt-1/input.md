FILE:desk/tasks/task-sldb-mcp-sirve-undo-changes-apply-changes-guarda-el-lote-inverso-de-cada-lote-en-una-pila-de-la-sesi.md
---
sldb:
  by: agent
  at: '2026-11-17T01:34:47Z'
  authority: generated
  via: create_document
id: task-sldb-mcp-sirve-undo-changes-apply-changes-guarda-el-lote-inverso-de-cada-lote-en-una-pila-de-la-sesi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-184421-unclear-ir04b-undo-changes-lo-sirve-sldb-mcp-o-es-una-extensi-n-de-specir-qui-n-guarda-la-pila-de-lotes-inversos-de-la-sesi-n.md
depends_on: []
pills: []
files:
- src/sldb/mcp/write/apply.py
- src/sldb/mcp/write/pending.py
- src/sldb/mcp/signals/catalog.py
- tests/mcp/test_write_tools.py
- docs/architecture/mcp.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
---

# sldb mcp sirve undo_changes: apply_changes guarda el lote inverso de cada lote en una pila de la sesión y undo_changes lo aplica con guardas (IR04b)

## Rationale

_Explain why this task exists or the business driver behind it._

apply_batch ya devuelve report.inverse (83c60239). src/sldb/mcp/signals/catalog.py dice que undo_changes es de sldb y se registra cuando exista; src/sldb/mcp/write/pending.py lo declara no servido; apply_changes (src/sldb/mcp/write/apply.py) no guarda el inverso. IR pregunta quién sirve undo_changes y dónde vive la pila; decisión del coordinador de sldb, siguiendo el catálogo: lo sirve sldb mcp y la pila vive en la sesión del servidor. Origen: desk/inbox/20261116-184421-unclear-ir04b-undo-changes-lo-sirve-sldb-mcp-o-es-una-extensi-n-de-specir-qui-n-guarda-la-pila-de-lotes-inversos-de-la-sesi-n.md.

## Goal

_Describe the concrete result this task must produce._

En una sesión de sldb mcp, cada apply_changes exitoso apila su report.inverse; undo_changes deshace el último lote aplicado (o los N últimos) aplicando su inverso con apply_batch, con las mismas guardas: si alguien escribió entre medio, se rechaza con ConflictError sin escritura parcial y el lote queda en la pila.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) la pila de lotes inversos en el estado de la sesión del servidor mcp (por sesión, en memoria, sin persistir), con push en apply_changes tras un apply exitoso; (2) la tool undo_changes con argumento opcional steps (default 1), que aplica los inversos del más reciente al más antiguo y devuelve lo deshecho; un fallo deja la pila como estaba desde ese lote; (3) quitar undo_changes de pending y del catálogo de no servidos; (4) dry-run si las demás tools de escritura lo tienen; (5) tests en tests/mcp/test_write_tools.py: aplicar, deshacer y comparar el store; deshacer tras una escritura ajena da conflicto y no escribe; deshacer con la pila vacía da un error claro. CHANGELOG y docs/architecture/mcp.md. No entra: persistir la pila entre sesiones, redo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/mcp/write/apply.py, pending.py, pendings.py, tools.py, src/sldb/mcp/signals/catalog.py, el estado de sesión del servidor y src/sldb/api/documents/batch_inverse.py. 2) Implementar la pila y la tool en módulos nuevos del paquete sldb.mcp.write si hace falta por la regla de 80 líneas. 3) Tests y docs. 4) Validation (los tests de mcp necesitan el extra mcp).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_signals.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_dry_run.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; undo_changes figura entre las tools servidas; CHANGELOG, docs y commit; aviso a IR (IR04b se reduce a verificarlo desde specIR).

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

FILE:desk/atoms/atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas.md
---
sldb:
  by: agent
  at: '2026-11-16T20:31:24Z'
  authority: generated
  via: create_document
id: atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
title: apply_batch devuelve en BatchReport.inverse el lote que lo deshace, con guardas
five_wh_one_plus: what
tags:
- system:sldb
- topic:batch
provenance: tarea 123855 (IR04b), ejecutor deskops-e-779515b3884a, tester deskops-t-937f21dafaca
  PASA
---

# apply_batch devuelve en BatchReport.inverse el lote que lo deshace, con guardas

## Answer

Bajo el cerrojo del store, apply_batch anota el estado previo de cada cambio y, tras la transacción, arma BatchReport.inverse: create->delete, update->update con el payload previo, delete->create con modelo, ruta y payload previos, move->move de vuelta, track<->untrack; cada paso lleva expected_source_hash del estado nuevo salvo el track inverso de un untrack. Deshacer es apply_batch(report.inverse): deja payloads e índice como antes y bytes iguales en documentos canónicos (la procedencia sldb.by/at/via puede cambiar). Si alguien escribió entre medio, el inverso se rechaza con ConflictError (o SLDBStoreError si el documento fue recreado) sin escritura parcial.

FILE:src/sldb/mcp/write/apply.py
"""Apply a proposal with `sldb.api.apply_batch`: whole, or nothing and the cause."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.mcp.addresses import document_address
from sldb.mcp.changes import EDGE_MODEL, BatchChange, Proposal
from sldb.mcp.write.findings import edge_findings, on_write_alerts
from sldb.mcp.write.pending import PENDING
from sldb.mcp.write.pendings import edge_pending, level_pending


def rejected(cause: str, explanation: str, **detail: Any) -> dict[str, Any]:
    """A refused proposal: nothing was written, and why."""
    return {"applied": False, "rejected": cause, "explanation": explanation, "written": False, **detail}


def refusal(error: Exception) -> dict[str, Any]:
    """SLDB's refusals come back with their cause; anything else is a tool error."""
    if not type(error).__module__.startswith("sldb."):
        raise error
    findings = [f.as_dict() for f in getattr(error, "findings", [])]
    if not findings:
        return rejected(type(error).__name__, str(error))
    rules = sorted({f["code"] for f in findings})
    return rejected("rules", f"refused by {', '.join(rules)}: {error}", findings=findings, rules=rules)


def written_row(store_path: Path, change: BatchChange) -> dict[str, Any]:
    """A document just written: its address, path, version and provenance."""
    document = api.serialize_document(api.runtime_document(store_path, None, f"{change.model}/{change.id}"))
    export_id = f"{change.model}:{change.id}"
    return {"export_id": export_id, "address": document_address(export_id), "path": document["path"], "version": document["version"], "provenance": document["provenance"]}


def applied(store_path: Path, proposal: Proposal, report: Any) -> dict[str, Any]:
    """The answer of an applied proposal."""
    written = [c for c in proposal.changes if c.action != "delete"]
    pending = [*edge_pending(proposal.changes), *level_pending(proposal.level), PENDING["guards_in_transaction"], PENDING["on_write_alerts"]]
    deleted = [document_address(f"{c.model}:{c.id}") for c in proposal.changes if c.action == "delete"]
    edges = [c for c in written if c.model == EDGE_MODEL]
    return {"applied": True, "saved": list(report.saved), "documents": [written_row(store_path, c) for c in written], "deleted": deleted, "alerts": on_write_alerts(store_path, written), "edge_findings": edge_findings(store_path, edges), "pending": pending}


def run_batch(store_path: Path, proposal: Proposal) -> dict[str, Any]:
    """`apply_batch` on the proposal, answered as applied, stale or refused."""
    try:
        report = api.apply_batch(store_path, [c.batch_form() for c in proposal.changes])
    except api.ConflictError as error:
        return rejected("stale", f"the store changed after the proposal was made: {error} Read it again and propose anew.", document=error.ref)
    except Exception as error:
        return refusal(error)
    return applied(store_path, proposal, report)

FILE:src/sldb/mcp/write/pending.py
"""What SLDB does not offer yet, and the note that asks for it. Nothing replaces it here:
every answer that depends on it says so."""

from __future__ import annotations

PENDING = {
    "dry_run": {
        "what": "a public dry run of apply_batch: propose_changes answers what would be written, but the prevalidation (model round-trip, guards, on_write rules, edge types) runs only when apply_changes calls apply_batch",
        "note": "sldb:20261115-022430-suggestion-specir-dry-run-p-blico-de-apply-batch",
    },
    "edge_validation_before_write": {
        "what": "an edge checked against its RelationTypeDoc (source and target types, cardinality, condition) before the RelationDoc is written: SLDB checks it only in check_edges, after the write, so apply_changes reports the violation instead of refusing it",
        "note": "sldb:20261115-022655-suggestion-specir-validar-aristas-antes-de-escribir-y-devolver-las-alertas-on-write-de-apply-batch",
    },
    "store_hash_precondition": {
        "what": "the store's fingerprint as an atomic precondition of apply_batch (level 2): only the per-document guards protect the apply",
        "note": "sldb:20261114-074447-suggestion-specir-brechas-api-p-blica-sldb-para-mcp",
    },
    "guards_in_transaction": {
        "what": "the guards re-checked inside apply_batch's transaction, or a store write lock: a concurrent writer between prevalidation and write is not detected",
        "note": "sldb:20261115-022444-suggestion-specir-guardas-de-apply-batch-bajo-el-cerrojo-del-store",
    },
    "on_write_alerts": {
        "what": "the on_write alerts of a write in apply_batch's answer: SLDB hands them only to in-process listeners, so apply_changes re-reads them with rules_check, which cannot take a document that is not a node of the edge index (a RelationDoc) as subject; those alerts are not reported",
        "note": "sldb:20261115-022655-suggestion-specir-validar-aristas-antes-de-escribir-y-devolver-las-alertas-on-write-de-apply-batch",
    },
    "undo": {
        "what": "undo_changes: apply_batch does not return the inverse batch with guards yet, so the MCP does not serve the tool; calling it is logged as a not_implemented signal",
        "note": "sldb:20261115-123855-suggestion-specir-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-en-sldb",
    },
}

FILE:src/sldb/mcp/signals/catalog.py
"""The closed catalog of signal classes: what a request can ask for that does not exist."""

from __future__ import annotations

UNKNOWN_TOOL = "unknown_tool"
UNKNOWN_ARGUMENT = "unknown_argument"
NOT_IMPLEMENTED = "not_implemented"

CLASSES = (UNKNOWN_TOOL, "unknown_model", "unknown_document", "unknown_field", "unknown_relation", "unknown_view", UNKNOWN_ARGUMENT, NOT_IMPLEMENTED)

#: Tools that are declared but not served yet, and what they wait for. Calling one is a signal.
PENDING_TOOLS = {
    "undo_changes": "re-applies the inverse batch that apply_batch will return (inbox request 20261115-123855, undo belongs to sldb); the tool is registered when that exists",
}

#: How many suggestions an answer carries.
SUGGESTIONS = 5

FILE:tests/mcp/test_write_tools.py
"""Propose and apply, called by the real MCP client on the real server at write level 2 over its
own copy of a real store. Payloads start from documents the store tracks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from mcp_helpers import an_item, files, page_items, tracked, valid_edge
from mcp_session import WRITER
from mcp_world import front_matter

EDGE_PENDING = "edge_validation_before_write"


def apply(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    """Propose `changes` and apply the proposal exactly as it came back."""
    return session.call("apply_changes", proposal=session.call("propose_changes", changes=changes)["proposal"])


def applied(session, changes: list[dict[str, Any]]) -> dict[str, Any]:
    answer = apply(session, changes)
    assert answer["applied"] is True, answer
    return answer


def signed_by_the_writer(answer: dict[str, Any], write_copy: Path, via: str) -> None:
    """Every document written carries who wrote it and through which operation, in the answer and on disk."""
    for document in answer["documents"]:
        assert document["provenance"]["by"] == WRITER and document["provenance"]["via"] == via, document
        on_disk = front_matter(write_copy / document["path"])["sldb"]
        assert on_disk["by"] == WRITER and on_disk["via"] == via, (document["path"], on_disk)


def test_cycle_on_a_document(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    name = "item-cycle"
    payload = {**item["payload"], "title": "The cycle: propose, validate, apply", "depends_on": []}
    created = applied(writer, [{"action": "create", "model": item["model"], "name": name, "payload": payload, "path": f"item/{name}.md"}])
    export_id = f"{item['model']}:{name}"
    assert [d["export_id"] for d in created["documents"]] == [export_id]
    signed_by_the_writer(created, write_copy, "create_document")
    read = writer.call("read_document", ref=export_id)
    assert read["found"] and read["payload"] == payload

    updated = applied(writer, [{"action": "update", "model": item["model"], "name": name, "fields": {"title": payload["title"] + " (edited)"}}])
    signed_by_the_writer(updated, write_copy, "save_document_payload")
    assert writer.call("read_document", ref=export_id, field="title")["value"] == payload["title"] + " (edited)"

    deleted = applied(writer, [{"action": "delete", "model": item["model"], "name": name}])
    assert deleted["deleted"] == [read["address"]] and deleted["documents"] == []
    assert writer.call("read_document", ref=export_id)["found"] is False
    assert not (write_copy / read["path"]).exists()


def test_cycle_on_an_edge(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "cycle-edge")
    target = writer.call("read_document", ref=edge["target"])["address"]

    def targets() -> set[str]:
        return {e["target"] for e in page_items(writer, "neighbors", node=edge["source"], direction="outgoing", relation=edge["relation_type"])}

    assert target not in targets(), "the edge exists already; it would prove nothing"
    asserted = applied(writer, [edge])
    assert asserted["edge_findings"] == [], asserted["edge_findings"]
    signed_by_the_writer(asserted, write_copy, "create_document")
    assert target in targets()
    stored = writer.call("read_document", ref="RelationDoc:cycle-edge")["payload"]
    assert (stored["source_id"], stored["target_id"], stored["relation_type"]) == (edge["source"], edge["target"], edge["relation_type"])

    applied(writer, [{"action": "retract_edge", "name": "cycle-edge"}])
    assert target not in targets()
    assert not (write_copy / edge["path"]).exists()


def test_a_change_to_a_store_that_moved_since_the_proposal_is_rejected(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    first = writer.call("propose_changes", changes=[{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": "first proposal"}}])
    second = writer.call("propose_changes", changes=[{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": "second proposal"}}])
    assert writer.call("apply_changes", proposal=second["proposal"])["applied"] is True
    stale = writer.call("apply_changes", proposal=first["proposal"])
    assert stale["applied"] is False and stale["rejected"] == "stale" and stale["document"] == item["name"]
    assert "changed" in stale["explanation"]
    assert "# second proposal" in (write_copy / item["path"]).read_text(encoding="utf-8")


def test_an_edited_proposal_is_refused(writer, write_copy: Path) -> None:
    item = an_item(writer, write_copy)
    proposal = writer.call("propose_changes", changes=[{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": "sealed"}}])["proposal"]
    proposal["changes"][0]["expected_source_hash"] = None
    assert "propose it again" in writer.error_of("apply_changes", proposal=proposal)


def a_rule(writer, root: Path, name: str, **fields: Any) -> dict[str, Any]:
    """A RuleDoc change: the world's first RuleDoc, under a new name with `fields`."""
    rule = tracked(writer, root, files(root, "ruledoc")[0])
    return {"action": "create", "model": "RuleDoc", "name": name, "payload": {**rule["payload"], **fields}, "path": f"ruledoc/{name}.md"}


def test_an_error_rule_refuses_the_change_and_is_named(writer, write_copy: Path) -> None:
    rule = a_rule(writer, write_copy, "rule-edges-explain-themselves", title="An authored edge explains itself", subject="model <= RelationDoc", where="", condition="nonempty(notes)", severity="error", moment="on_write", message="An authored edge explains itself in its notes.")
    applied(writer, [rule])
    try:
        silent = {**valid_edge(write_copy, "edge-without-notes"), "notes": ""}
        refused = apply(writer, [silent])
        assert refused["applied"] is False and refused["rejected"] == "rules"
        assert refused["rules"] == [f"rules/{rule['name']}"] and rule["name"] in refused["explanation"]
        assert refused["findings"][0]["level"] == "error" and refused["findings"][0]["subject"] == "RelationDoc:edge-without-notes"
        assert not (write_copy / silent["path"]).exists()
    finally:
        applied(writer, [{"action": "delete", "model": "RuleDoc", "name": rule["name"]}])


def test_an_alert_rule_is_reported_by_name(writer, write_copy: Path) -> None:
    rules = [p for p in files(write_copy, "ruledoc") if front_matter(p)["moment"] == "on_write" and front_matter(p)["severity"] == "alert"]
    assert rules, "the world declares no on_write alert"
    item = tracked(writer, write_copy, next(p for p in files(write_copy, "item") if not front_matter(p)["owner"]))
    answer = applied(writer, [{"action": "update", "model": item["model"], "name": item["name"], "fields": {"title": item["payload"]["title"] + " (touched)"}}])
    codes = {a["code"] for a in answer["alerts"] if a["subject"] == item["export_id"]}
    assert {f"rules/{tracked(writer, write_copy, p)['name']}" for p in rules} <= codes, answer["alerts"]


def test_an_edge_against_its_relation_type_is_reported(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "edge-wrong-source")
    allowed = front_matter(files(write_copy, "relationtypedoc")[0])["source_types"]
    item = an_item(writer, write_copy)
    assert item["model"] not in allowed
    wrong = {**edge, "source": item["export_id"]}
    proposal = writer.call("propose_changes", changes=[wrong])
    assert any(p["note"].startswith("sldb:") for p in proposal["pending"] if EDGE_PENDING in p["what"] or "RelationTypeDoc" in p["what"])
    answer = writer.call("apply_changes", proposal=proposal["proposal"])
    try:
        assert answer["applied"] is True
        assert any("source_types" in f and item["export_id"] in f for f in answer["edge_findings"]), answer["edge_findings"]
    finally:
        applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])


def test_cardinality_and_condition_of_a_declared_type_are_reported(writer, write_copy: Path) -> None:
    base = tracked(writer, write_copy, files(write_copy, "relationtypedoc")[0])
    name = "one_to_one"
    declared = {"action": "create", "model": "RelationTypeDoc", "name": f"type-{name}", "path": f"relationtypedoc/type-{name}.md", "payload": {**base["payload"], "name": name, "title": "One to one", "cardinality": "one_to_one", "target_types": []}}
    applied(writer, [declared])
    first, second = valid_edge(write_copy, "card-1"), valid_edge(write_copy, "card-2")
    # Two targets for one source under a one_to_one type, the second with a condition that does not parse.
    edges = [{**first, "relation_type": name}, {**second, "relation_type": name, "target": "Stage:review", "condition": "status = "}]
    try:
        findings = applied(writer, edges)["edge_findings"]
        assert any(f"has 2 '{name}' targets but cardinality is one_to_one" in f for f in findings), findings
        assert any("condition does not parse" in f for f in findings), findings
    finally:
        applied(writer, [{"action": "retract_edge", "name": e["name"]} for e in edges] + [{"action": "delete", "model": "RelationTypeDoc", "name": f"type-{name}"}])


@pytest.mark.xfail(strict=True, reason="SLDB checks an edge against its RelationTypeDoc only after the write (check_edges); asked by note, see PENDING['edge_validation_before_write']")
def test_an_edge_against_its_relation_type_is_refused_before_writing(writer, write_copy: Path) -> None:
    edge = valid_edge(write_copy, "edge-refused")
    item = an_item(writer, write_copy)
    wrong = {**edge, "source": item["export_id"]}
    answer = apply(writer, [wrong])
    try:
        assert answer["applied"] is False and not (write_copy / wrong["path"]).exists()
    finally:
        if answer["applied"]:
            applied(writer, [{"action": "retract_edge", "name": wrong["name"]}])

FILE:docs/architecture/mcp.md
# `sldb mcp`: the store served to an MCP client

`sldb mcp --store <project>/.sldb [--level 0|1|2] [--actor <who>] [--extension module:function]...`
serves one store over stdio as a Model Context Protocol server. It is the server of specIR
(`specir.mcp`, IR03 reads and IR04 writes) moved here, because it knows nothing of specIR's domain: it
reads and writes a store only through `sldb.api`. A consumer mounts its own domain tools on top
(see *Extension point*) instead of copying it.

Code: `src/sldb/mcp/`. Layer: transport (`contracts/layers.toml`), beside `cli`. Optional extra
`mcp` (`pip install 'structuredLanguageDB[mcp]'`, `mcp>=2.2`); only `sldb.mcp.server`'s own
modules import the library, so sldb without the extra works and `sldb mcp` says how to install it.

## Levels

The level is the operator's (`--level`), never a tool argument, and levels are cumulative.

| level | serves |
| --- | --- |
| 0 (default) | the eleven read tools and `list_signals`, all read-only |
| 1 content | adds `propose_changes` and `apply_changes` for documents of registered models and authored edges (`RelationDoc`) |
| 2 rules as data | the same two tools may also write `RelationTypeDoc` and `RuleDoc` |

Models as Python code (level 3) are never served: no tool writes a Python module.

Read tools: `list_models`, `describe_model`, `list_relation_types`, `describe_relation_type`,
`read_document`, `select_documents`, `neighbors`, `neighborhood`, `list_views`, `resolve_view`,
`check_integrity`. Documents have the stable address `sldb://document/<export_id>`; every set is
a page `{items, total, offset, limit, truncated, next_offset}`.

## Writing: propose, then apply

`propose_changes` turns typed changes (`create`, `update`, `delete`, `assert_edge`, `retract_edge`)
into a batch for `sldb.api.apply_batch` with the `expected_source_hash` guard of every document it
touches, seals it, and answers what it would write; it writes nothing. `apply_changes` takes that
proposal back unchanged and hands it to `apply_batch`: all or nothing, or rejected with its cause
(`stale` when a guarded document changed, `rules` naming the RuleDocs that refused it). `--actor`
signs the provenance of what is written. What `sldb.api` does not offer yet (a public dry run,
edge validation before the write, the store hash as a precondition) is listed in every answer's
`pending`, with the inbox note that asks for it.

## Signals

Asking for something that does not exist, or is called differently, is not an error: it is a
signal. The answer says it does not exist or is not implemented and was registered as a signal,
and carries `suggestions` (the five names `sldb.api.matching.Matcher.rank` ranks nearest, in its
order). The closed catalog of classes: `unknown_tool`, `unknown_model`, `unknown_document`,
`unknown_field`, `unknown_relation`, `unknown_view`, `unknown_argument` and `not_implemented`.
For an unknown tool or argument nothing runs.

Each signal is one JSON line appended (`O_APPEND`) to **`<project>/.sldb_cache/signals.jsonl`**:

```json
{"at": "2026-11-15T16:15:32.896Z", "tool": "describe_model", "arguments": {"model": "Itm"}, "signal_class": "unknown_model", "suggestions": ["Item", "Stage"], "actor": null}
```

`list_signals(signal_class?, offset, limit)` reads it, paged like every set, at every level. The
log lives in the cache (`sldb.store.layout.cache_dir`), next to `.sldb_cache/rules` and
`.sldb_cache/composed`: it is derived, ignored by git, and not store state, so recording a signal
at level 0 writes no tracked document and no linked store. There is no rotation yet.

## Undo (pending)

`undo_changes` is declared and not served: `apply_batch` does not yet return the inverse batch
with guards (inbox request 20261115-123855; undo belongs to sldb). Calling it answers
`not_implemented` and is logged. When the request is resolved the tool re-applies the inverse.

## Extension point

```python
from sldb.mcp.server import build_server

def register(server, context):          # context: store_path, project_root, level, actor, log
    @server.tool()
    def my_tool(name: str, offset: int = 0, limit: int = 50) -> dict: ...

server = build_server(store, level=1, actor="agent:me", extensions=[register])
```

or `sldb mcp ... --extension my_package.tools:register` (repeatable). Every tool registered on the
server, the built-in ones and an extension's, goes through the same guard: a failure reaches the
agent with its cause, an unknown argument is a signal, and a dict answer carrying
`{"signal": {"class": ..., "name": ...}}` is logged with suggestions. Pages come from
`sldb.mcp.paging.page`; an extension reads `context.level` to refuse what the operator did not allow.

### Batch validators

An extension adds a domain rule to the write tools without re-registering them:

```python
def register(server, context):
    def claims_verified(changes, context):   # changes: the batch's list of changes
        return [{"code": "claims_verified", "level": "error", "what": "only the server verifies", "subject": c.name} for c in changes if ...]
    context.add_batch_validator(claims_verified)
```

The stable extension contract is `sldb.mcp.extension.Extension` (`extension(server, context)`),
`sldb.mcp.extension.BatchValidator` (`validator(changes, context) -> list[dict]`) and
`ServerContext.add_batch_validator(validator)`. `build_server` runs every extension before the server
answers its first call and hands the `ServerContext` to the write tools, which read
`context.batch_validators` on every call:

- `propose_changes` runs them after its level and path checks and before building the batch, over
  its typed changes (`create`/`update`/`delete`/`assert_edge`/`retract_edge`); `apply_changes` runs
  them after its level check and the seal check, over the proposal's `BatchChange`s (`id`, `action`,
  `model`, `payload`, `path`).
- Every validator runs, always. A finding is `{"code", "level", "what", "subject"}` with `level`
  `"error"` or `"alert"`.
- Any `"error"`: the answer is `{"applied": false, "rejected": "domain", "explanation": "<n> domain
  check(s) failed", "written": false, "findings": [every finding, errors and alerts]}`; nothing is
  sealed or written.
- Only alerts: the dry run of `propose_changes` and the answer of `apply_changes` gain
  `"domain_alerts": [...]`. Without findings (or without validators) the answers are as before.

FILE:instruccion
Cold-bundle de la tarea task-sldb-mcp-sirve-undo-changes-apply-changes-guarda-el-lote-inverso-de-cada-lote-en-una-pila-de-la-sesi: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_signals.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_dry_run.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

