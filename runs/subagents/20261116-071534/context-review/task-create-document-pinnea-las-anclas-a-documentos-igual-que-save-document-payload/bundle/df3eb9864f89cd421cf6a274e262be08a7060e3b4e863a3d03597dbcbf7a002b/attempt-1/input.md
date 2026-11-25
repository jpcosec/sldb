FILE:desk/tasks/task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload.md
---
sldb:
  by: agent
  at: '2026-11-16T05:10:14Z'
  authority: generated
  via: save_document_payload
id: task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-g-consumer-cumplido-por-deskops-cc32-6afc78b0.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/create_document.py
- tests/api/test_doc_anchors.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# create_document pinnea las anclas a documentos igual que save_document_payload

## Rationale

_Explain why this task exists or the business driver behind it._

GO07 pinnea al guardar: un doc:Model:name sin @sha256 en un campo de __doc_anchors__ o en el from: de procedencia recibe el hash de contrato del destino (src/sldb/api/documents/doc_anchor_pinning.py, pin_payload y pin_provenance). save_document_payload lo hace (src/sldb/api/documents/payload_save.py:46), pero create_document (src/sldb/api/documents/create_document.py) renderiza el payload sin pinnear. Un recibo creado y nunca reescrito queda con anchor_state lost aunque su destino exista; deskops lo esquiva con create + update en la misma transacción (hipótesis H-CC32-2 de deskops CC32). Origen: desk/inbox/inbox-note-g-consumer-cumplido-por-deskops-cc32-6afc78b0.md (hipótesis 2).

## Goal

_Describe the concrete result this task must produce._

Un documento creado con create_document cuyo campo de __doc_anchors__ nombra un destino trackeado sin @sha256 queda escrito con el ancla pinneada (anchor_state intact al leerlo), igual que si se hubiera guardado con save_document_payload.

## Scope

_State what is in scope and what is out of scope._

Entra: en create_document llamar pin_payload(location.store_path, model_type, payload) antes de _rendered (y pin_provenance sobre el texto si save_document_payload también lo hace; seguir exactamente el mismo orden que payload_save.py). Lo mismo dentro de la transacción si create pasa por otro camino (buscar create en src/sldb/api/documents/transaction*.py). Test en tests/api/test_doc_anchors.py: un modelo con __doc_anchors__ y un destino trackeado; create_document deja el valor con @sha256 y el ancla intact; un destino no trackeado deja el valor como estaba (lost), como en save. CHANGELOG.md. No entra: cambiar el testigo de any en los findings (hipótesis 1 de la nota) ni anchors check sobre índices anteriores a GO07 (hipótesis 3).

Precisiones (preflight-1): verificado en HEAD: save_document_payload llama pin_payload (payload_save.py:46) y, al renderizar, pin_provenance sobre el texto (render_checked en payload_save_steps.py:92); create_document debe llamar a los dos en el mismo orden relativo (pin_payload sobre el payload antes de renderizar, pin_provenance sobre el texto renderizado antes de escribir). Si Transaction.create (transaction.py:79, que llama create de transaction_ops.py:27) usa otro camino que no pasa por create_document, se agrega el mismo pinneo ahí; si pasa por create_document, no hace falta nada más. "Destino trackeado" es un documento que el store tiene en su índice (store_current lo encuentra); anchor_state "intact" es el valor que devuelve la lectura de anclas para un ancla pinneada con el hash actual del destino (lo que ya prueba tests/api/test_doc_anchors.py para save). El alcance incluye los dos: campos de __doc_anchors__ y el from: de procedencia.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer payload_save.py (líneas 30-60), doc_anchor_pinning.py, create_document.py y grep -rn "create_document\|def create" src/sldb/api/documents/transaction*.py. 2) Agregar el pinneo en el mismo punto relativo. 3) Tests.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos pasan con el test nuevo; CHANGELOG y commit; aviso a deskops con deskops message send --to deskops de que create ya pinnea (puede quitar su create + update).

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

FILE:src/sldb/api/documents/create_document.py
"""Render a payload to a new Markdown file and track it as a document of a registered model."""

from __future__ import annotations
from sldb.api.stores.declaration_sync import declare_tracked, project_relative

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.documents.on_write_gate import check_entering
from sldb.api.documents.refuse_structural_noise import refuse_structural_noise
from sldb.api.documents.frontmatter_keys import refuse_undeclared_frontmatter
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from sldb.api.documents.provenance_stamp import stamped
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.ops import track_document
from sldb.store.source_guard import READ_CODES, write_source_text
from sldb.store.source_read import SYMLINK


def create_document(store: str | Path | None, model_name: str, path: str | Path, payload: dict[str, Any], name: str | None = None, pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Write the Markdown a model renders from `payload` and start tracking it.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file to write (parents are created, an existing file is
            overwritten); a relative path is relative to the project root, not the cwd.
        payload: The document's field values; it has no fixed schema beyond the model's own.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        actor: Optional caller label, stamped into the document's provenance block.

    Returns:
        The created document.

    Raises:
        SLDBStoreError: When the model is not registered, or a RuleDoc's subject names a model
            the store does not register.
        SLDBValidationError: When the rendered Markdown does not round-trip under the model,
            or when it carries headings the model does not declare; nothing is written then.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    rendered = _rendered(location, registered.model_type, payload, pythonpath)
    doc_path = _resolve_path(path, location.project_root)
    doc_name = name or doc_path.stem
    _admit(location.store_path, registered, rendered, doc_name, payload)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    write_source_text(doc_path, stamped(rendered + "\n", registered.model_type, "create_document", actor))
    _track(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def refuse_noise(model_type: type, markdown: str, name: str, store_path: Path | None = None) -> None:
    """Refuse a document whose headings (unless the store's policy allows them) or frontmatter
    keys the model never declares."""
    from sldb.api.stores.policy import Policy

    refuse_structural_noise(model_type, markdown, name, Policy.of_store(store_path) if store_path else None)
    refuse_undeclared_frontmatter(model_type, markdown, name)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    """The new document's path, resolved; a symlink there is refused BEFORE resolving (the write
    would go where it points). A plain path outside the project is still created (spec2viz)."""
    raw_path = Path(raw) if Path(raw).is_absolute() else root / raw
    if raw_path.is_symlink():
        raise SLDBDocumentTargetError(f"[{READ_CODES[SYMLINK]}] {raw}: the path is a symlink; sldb does not write it")
    return raw_path.resolve()


def _track(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, pythonpath: str | None) -> None:
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    declare_tracked(sp, root, registered.entry.name, project_relative(root, doc_path), doc_name)


def _rendered(location, model_type: type, payload: dict[str, Any], pythonpath: str | None) -> str:
    """The round-tripped Markdown, once a RuleDoc's subject names only registered models."""
    rendered = _render_roundtrip(model_type, payload, location.project_root)
    refuse_unknown_family(location.store_path, model_type, payload, pythonpath)
    return rendered


def _render_roundtrip(model_type: type, payload: dict[str, Any], ref_root: Path) -> str:
    """The payload rendered to Markdown, refused unless it extracts back identically.

    `ref_root` is the project root, so a composed field resolves its refs the way the project
    names them; without it they would resolve against whatever directory the caller runs in.
    """
    rendered = render_model_markdown(model_type, payload, ref_root)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
    return rendered


def _admit(sp: Path, registered, rendered: str, doc_name: str, payload: dict[str, Any]) -> None:
    """Refuse a document the model's structure or an `on_write` rule (H4) does not admit."""
    refuse_noise(registered.model_type, rendered, doc_name, sp)
    check_entering(sp, registered.model_type, registered.entry.name, doc_name, payload)

FILE:tests/api/test_doc_anchors.py
"""GO07: document anchors pinned with the target's contract hash (docs/architecture/anchoring.md §6).

A Review's `subject` (in `__doc_anchors__`) anchors a TaskDoc whose `__contract__` is title and
status; `notes` is outside it. The save pins, the composed index derives `subject__anchor_state`
(never written to a shard), `anchors check` reports what moved as alerts, and the rules
language reads it through `^subject`. A malformed form or model definition is refused.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import Field, ValidationError

from sldb import StructuredNLDoc, api
from sldb.api.rules.rule_graph import rule_graph
from sldb.cli import main
from sldb.core.exceptions import SLDBModelError
from sldb.models.provenance import Provenance
from sldb.models.provenance_block import attach_block, read_block
from sldb.store.edge_index.doc_anchor_states import field_states
from sldb.store.edge_index.node_ids import EDGE_INDEX_VERSION
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.layout import edges_shard_path

MODULE = "sldb_go07_doc_anchor_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class TaskDoc(StructuredNLDoc):
    __contract__ = ["title", "status"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\nnotes: ⸢rev•notes⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    notes: str = Field(default="", description="Free notes, outside the contract.")


class Review(StructuredNLDoc):
    __doc_anchors__ = ["subject"]
    __template__ = "---\\nsubject: ⸢rev•subject⸥\\nverdict: ⸢rev•verdict⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subject: str = Field(default="", description="The reviewed document.")
    verdict: str = Field(default="", description="accepted or rejected.")


class Bundle(StructuredNLDoc):
    __doc_anchors__ = ["subjects"]
    __template__ = "---\\nsubjects: ⸢rev•subjects⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subjects: list[str] = Field(default_factory=list, description="Anchored documents.")


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''
ACCEPTED = 'any(^subject: anchor_state = "intact" and verdict = "accepted")'
TASK = {"title": "b", "status": "open", "notes": ""}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("TaskDoc", "Review", "Bundle", "Note"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.create_document(self.store, "TaskDoc", self.root / "b.md", TASK, "b", self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, payload, self.py)

    def payload(self, export_id: str) -> dict:
        return api.edge_node(self.store, export_id).payload

    def b_hash(self) -> str:
        return contract_hash(sys.modules[MODULE].TaskDoc, api.edge_node(self.store, "TaskDoc:b").field_hashes)

    def review(self, name: str = "a", subject: str = "doc:TaskDoc:b", verdict: str = "accepted") -> None:
        payload = {"title": name, "subject": subject, "verdict": verdict}
        self.create("Review", name, payload)
        self.save("Review", name, payload)

    def codes(self) -> list[tuple[str, str, str]]:
        return [(f.level, f.code, f.subject) for f in api.check_doc_anchors(self.store, self.py)]

    def holds(self, predicate: str = ACCEPTED, node: str = "TaskDoc:b") -> str:
        return rule_graph(self.store).holds(predicate, node)["holds"]


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_saved_anchor_is_pinned_with_the_target_contract_hash(world: World) -> None:
    world.review()
    assert world.payload("Review:a")["subject"] == f"doc:TaskDoc:b@sha256:{world.b_hash()}"
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"
    assert world.codes() == []


def test_the_anchor_follows_the_target_contract_and_anchors_check_alerts(world: World, capsys) -> None:
    world.review()
    world.save("TaskDoc", "b", {**TASK, "notes": "outside the contract"})
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.payload("Review:a")["subject__anchor_state"] == "changed"
    assert world.codes() == [("alert", "anchors/doc_changed", "Review:a")]
    found = api.check_doc_anchors(world.store, world.py)[0]
    assert found.document == "a.md" and "subject" in found.what and "TaskDoc:b" in found.what and "changed" in found.what and found.fix == ""
    assert main(["--envelope", "anchors", "check", "--store", str(world.store), "--pythonpath", world.py, "--format", "json"]) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert [w["code"] for w in envelope["warnings"]] == ["anchors/doc_changed"]
    api.delete_document(world.store, "b", world.py)
    assert world.payload("Review:a")["subject__anchor_state"] == "lost"
    assert world.codes() == [("alert", "anchors/doc_lost", "Review:a")]


def test_an_anchor_to_a_missing_target_is_saved_without_hash_and_pinned_by_a_later_write(world: World) -> None:
    world.review(subject="doc:TaskDoc:later")
    assert world.payload("Review:a")["subject"] == "doc:TaskDoc:later"
    world.create("TaskDoc", "later", {**TASK, "title": "later"})
    assert world.payload("Review:a")["subject__anchor_state"] == "lost"
    world.save("Review", "a", {"title": "a", "subject": "doc:TaskDoc:later", "verdict": "accepted"})
    assert world.payload("Review:a")["subject"].startswith("doc:TaskDoc:later@sha256:")
    assert world.payload("Review:a")["subject__anchor_state"] == "intact"


def test_the_subject_anchor_is_an_edge_and_the_derived_state_never_reaches_the_shard(world: World) -> None:
    world.review()
    edges = api.edges_from(world.store, "Review:a", "references")
    assert [(e.target, e.metadata["field"]) for e in edges] == [("sldb://document/TaskDoc:b", "subject")]
    shard = edges_shard_path(world.store, "Review", "a").read_text(encoding="utf-8")
    assert "__anchor_state" not in shard and EDGE_INDEX_VERSION == "5"


def test_the_rule_reads_anchor_state_through_the_inverse_subject(world: World) -> None:
    assert world.holds() == "false"
    world.review("r1", verdict="rejected")
    assert world.holds() == "false"
    world.review("r2", verdict="accepted")
    assert world.holds() == "true"
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.holds() == "false"


def test_a_list_field_has_one_state_and_one_edge_per_anchor(world: World) -> None:
    payload = {"title": "set", "subjects": ["doc:TaskDoc:b", "doc:TaskDoc:ghost"]}
    world.create("Bundle", "set", payload)
    world.save("Bundle", "set", payload)
    assert world.payload("Bundle:set")["subjects__anchor_state"] == ["intact", "lost"]
    assert [e.target for e in api.edges_from(world.store, "Bundle:set", "references")] == ["sldb://document/TaskDoc:b"]
    assert world.codes() == [("alert", "anchors/doc_lost", "Bundle:set")]
    assert field_states(["doc:A:x", "", "  "], lambda _: (True, None)) == ["lost", None, None]


def test_a_provenance_from_anchor_is_pinned_and_alerts_when_the_target_contract_moves(world: World) -> None:
    world.create("Note", "c", {"title": "c"})
    path = world.root / "c.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(attach_block(text, {**(read_block(text) or {}), "from": ["code:src/x.py::f", "doc:TaskDoc:b"]}), encoding="utf-8")
    world.save("Note", "c", {"title": "c"})
    assert read_block(path.read_text(encoding="utf-8"))["from"] == ["code:src/x.py::f", f"doc:TaskDoc:b@sha256:{world.b_hash()}"]
    assert world.codes() == []
    world.save("TaskDoc", "b", {**TASK, "status": "closed"})
    assert world.codes() == [("alert", "anchors/provenance_changed", "Note:c")]
    api.delete_document(world.store, "b", world.py)
    assert world.codes() == [("alert", "anchors/provenance_lost", "Note:c")]


def test_a_value_that_is_not_an_anchor_is_refused_when_written(world: World) -> None:
    with pytest.raises(Exception, match="subject.*not a document anchor"):
        world.create("Review", "bad", {"title": "bad", "subject": "TaskDoc:b", "verdict": ""})
    world.review()
    with pytest.raises(Exception, match="subject.*not a document anchor"):
        world.save("Review", "a", {"title": "a", "subject": "see TaskDoc:b", "verdict": ""})


@pytest.mark.parametrize("value", ["TaskDoc:b", "doc:TaskDoc", "doc:TaskDoc:b@sha256:", "doc:TaskDoc:b@sha256:abc", "doc:TaskDoc:b@sha256:" + "g" * 64, "doc:TaskDoc:b@md5:" + "a" * 64])
def test_a_malformed_anchor_form_is_rejected_in_a_field_and_in_from(world: World, value: str) -> None:
    review = sys.modules[MODULE].Review
    with pytest.raises(ValidationError, match="subject"):
        review(title="x", subject=value)
    if value.startswith("doc:"):
        with pytest.raises(ValidationError, match="from"):
            Provenance(from_=[value])


def test_the_accepted_forms_and_from_items_that_are_not_doc_anchors(world: World) -> None:
    review = sys.modules[MODULE].Review
    assert review(title="x", subject="").subject == ""
    assert review(title="x", subject="doc:TaskDoc:b@sha256:" + "a" * 64).subject.endswith("a" * 64)
    assert Provenance(from_=["code:src/x.py::f", "whatever"]).from_ == ["code:src/x.py::f", "whatever"]


@pytest.mark.parametrize(
    ("body", "reason"),
    [
        ('__doc_anchors__ = ["count"]\n    count: int = Field(default=0, description="A number.")', "count"),
        ('__doc_anchors__ = ["ghost"]\n    title: str = Field(description="Title.")', "ghost"),
        ('__doc_anchors__ = ["meta"]\n    meta: dict = Field(default_factory=dict, description="Nested.")', "meta"),
        ('subject__anchor_state: str = Field(default="", description="Reserved.")', "reserved suffix"),
    ],
)
def test_an_invalid_model_definition_is_refused_when_loaded(tmp_path: Path, body: str, reason: str) -> None:
    module = "sldb_go07_bad_definition"
    (tmp_path / f"{module}.py").write_text(f"from pydantic import Field\nfrom sldb import StructuredNLDoc\n\n\nclass Bad(StructuredNLDoc):\n    {body}\n", encoding="utf-8")
    try:
        with pytest.raises(SLDBModelError, match=f"Bad.*{reason}"):
            api.resolve_model_ref(f"{module}:Bad", str(tmp_path))
    finally:
        sys.modules.pop(module, None)


def test_optional_str_and_list_fields_are_valid_anchor_fields() -> None:
    class Fine(StructuredNLDoc):
        __doc_anchors__ = ["one", "many"]
        one: str | None = Field(default=None, description="One.")
        many: list[str] = Field(default_factory=list, description="Many.")

    from sldb.store.model_contract import doc_anchor_fields

    assert doc_anchor_fields(Fine) == ["one", "many"]

FILE:instruccion
Cold-bundle de la tarea task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py

