FILE:desk/tasks/task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse.md
---
sldb:
  by: agent
  at: '2026-11-17T02:47:46Z'
  authority: generated
  via: create_document
id: task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/architecture/provenance.md
depends_on: []
pills: []
files:
- src/sldb/api/anchors/anchor_docs.py
- tests/api/test_provenance.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El parámetro actor de la API de escritura se respeta en lugar de aceptarse e ignorarse

## Rationale

_Explain why this task exists or the business driver behind it._

Varias funciones de sldb.api aceptan actor y lo ignoran: unas 15 tienen actor: str | None = None, y algunas lo pisan (por ejemplo src/sldb/api/anchors/anchor_docs.py:47 llama save_document_payload con actor=None). Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

Toda función pública de escritura que acepta actor lo pasa hasta donde se registra la procedencia (sello sldb.by del documento), de modo que un documento escrito con actor=X queda firmado por X; ninguna lo descarta.

## Scope

_State what is in scope and what is out of scope._

Entra: inventario de las funciones con parámetro actor; ver cómo se forma el sello de procedencia (docs/architecture/provenance.md y el código que lo escribe); pasar actor hasta ahí en cada camino, incluido anchor_docs.write_anchor; tests en tests/api/test_provenance.py. Si alguna no puede respetarlo, se documenta en su docstring y en result-summary.md. CHANGELOG. No entra: cambiar el formato del sello.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep de 'actor' en src/sldb/api. 2) Seguir el camino hasta el sello. 3) Corregir cada función. 4) Tests. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; ninguna función pública de escritura descarta actor; CHANGELOG y commit.

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

FILE:src/sldb/api/anchors/anchor_docs.py
"""The anchor documents of a store, and the two writes anchoring makes: a reconnection, and a
(re)recorded anchor written through the documents API, so it is signed like any document."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sldb.api.documents.payload_save import save_document_payload
from sldb.api.stores.open_store import open_store
from sldb.store.layout import project_root

MODEL = "CodeAnchorDoc"


@dataclass
class AnchorDocument:
    root: Path
    name: str
    path: str
    payload: dict[str, Any]


def anchor_documents(store: str | Path | None, pythonpath: str | None) -> list[AnchorDocument]:
    """Every tracked `CodeAnchorDoc`, extracted; none when the model is not registered."""
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.query import load_runtime_documents

    location = open_store(store, mode="readonly")
    root = project_root(location.store_path)
    docs = load_runtime_documents(location.store_path, resolve_model_ref, pythonpath)
    return [AnchorDocument(root, d.name, d.path, dict(d.payload)) for d in docs if d.model_name == MODEL]


def record_reconnection(store: str | Path | None, pythonpath: str | None, doc: AnchorDocument, to: str) -> None:
    """The anchor now points at `to`, and its signature and shape are the new name's (the
    docstring and body it saw stay: a body that moved is still reported); where it pointed
    before stays in `history`."""
    from sldb.api.anchors.record_anchor import record_anchor

    now = record_anchor(doc.root, to)["seen"]
    seen = {**doc.payload.get("seen", {}), "signature": now["signature"], "shape": now["shape"]}
    event = {"event": "reconnected", "from": doc.payload["ref"], "to": to, "at": _now()}
    payload = {**doc.payload, "ref": to, "seen": seen, "history": [*doc.payload.get("history", []), event]}
    save_document_payload(store, MODEL, doc.name, payload, pythonpath, actor=None)


def write_anchor(store: str | Path | None, pythonpath: str | None, path: Path, block: dict[str, Any], claim: str, name: str | None = None) -> Any:
    """Create the anchor document, or re-record an existing one (its claim and history kept)."""
    from sldb.api.documents.create_document import create_document

    existing = next((d for d in anchor_documents(store, pythonpath) if (project_root(open_store(store, mode="readonly").store_path) / d.path).resolve() == path.resolve()), None)
    if existing is None:
        return create_document(store, MODEL, path, {**block, "claim": claim, "history": [{"event": "recorded", "at": _now()}]}, name, pythonpath)
    payload = {**existing.payload, **block, "claim": claim or existing.payload.get("claim", ""), "history": [*existing.payload.get("history", []), {"event": "recorded", "at": _now()}]}
    return save_document_payload(store, MODEL, existing.name, payload, pythonpath)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

FILE:tests/api/test_provenance.py
"""Provenance (docs/architecture/provenance.md): the `sldb` block every write signs, what a
document without one reads as, and what a stamp does and does not move."""
from __future__ import annotations

import json

import pytest

import sldb.api as api
from sldb.api.actor import current_actor, set_actor
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.provenance_stamp import provenance_of, stamped
from sldb.cli import main as cli_main
from sldb.models.provenance_block import attach_block, read_block, strip_block
from sldb.runtime.validation import extract_model_data

from .conftest import MODULE, PAYLOAD

BLOCK = {"by": "human:jp", "at": "2026-10-20T10:00:00Z", "authority": "authored"}


@pytest.fixture(autouse=True)
def _no_process_actor():
    set_actor(None)
    yield
    set_actor(None)


def test_the_block_goes_first_in_a_frontmatter_and_makes_one_when_there_is_none():
    plain = "# T\n\nbody\n"
    with_fm = "---\nkind: unclear\n---\n\n# T\n\nbody\n"
    assert attach_block(plain, BLOCK) == "---\nsldb:\n  by: human:jp\n  at: '2026-10-20T10:00:00Z'\n  authority: authored\n---\n\n# T\n\nbody\n"
    assert attach_block(with_fm, BLOCK).startswith("---\nsldb:\n  by: human:jp\n") and "kind: unclear\n---\n\n# T" in attach_block(with_fm, BLOCK)
    for text in (plain, with_fm):
        assert read_block(attach_block(text, BLOCK)) == BLOCK
        assert strip_block(attach_block(text, BLOCK)) == text, "strip is attach's inverse"
    assert read_block(plain) is None and strip_block(plain) == plain


def test_a_document_without_a_block_reads_as_agent_zero_generated():
    found = provenance_of("# T\n\nbody\n")
    assert (found.by, found.at, found.authority, found.declared) == ("agent", 0, "generated", False)


def test_create_signs_with_the_actor_the_time_and_the_models_authority(api_store):
    created = api.create_document(api_store.store, "TicketDoc", api_store.root / "new.md", PAYLOAD, "new", api_store.pythonpath, actor="agent:test")
    text = created.path.read_text(encoding="utf-8")
    found = provenance_of(text)
    assert (found.by, found.authority, found.via, found.declared) == ("agent:test", "generated", "create_document", True)
    assert str(found.at).endswith("Z")
    assert extract_model_data(api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath), text) == PAYLOAD, "the block is not a field"


def test_a_save_that_changes_nothing_keeps_the_block_and_one_that_does_restamps(api_store):
    model = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    api.save_document_payload(api_store.store, "TicketDoc", "login", PAYLOAD, api_store.pythonpath, actor="agent:one")
    path = api_store.root / "login.md"
    first = read_block(path.read_text(encoding="utf-8"))
    api.save_document_payload(api_store.store, "TicketDoc", "login", PAYLOAD, api_store.pythonpath, actor="agent:two")
    assert read_block(path.read_text(encoding="utf-8")) == first, "nothing changed: the signature stays"
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Other"}, api_store.pythonpath, actor="agent:two")
    second = read_block(path.read_text(encoding="utf-8"))
    assert second["by"] == "agent:two" and second["via"] == "save_document_payload"
    assert extract_model_data(model, path.read_text(encoding="utf-8"))["title"] == "Other"


def test_a_declared_authority_survives_a_save_and_a_stamp_moves_only_the_text_hash(api_store):
    from sldb.store.hashing import hash_fields, hash_text

    model = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    path = api_store.root / "login.md"
    path.write_text(attach_block(path.read_text(encoding="utf-8"), {**BLOCK, "authority": "source_raw"}), encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Edited"}, api_store.pythonpath)
    after = path.read_text(encoding="utf-8")
    assert provenance_of(after).authority == "source_raw" and provenance_of(after).by == "agent"
    stamped_twice = stamped(strip_block(after), model, "x", "agent:z", previous=before)
    assert hash_fields(model, stamped_twice) == hash_fields(model, after) and hash_text(stamped_twice) != hash_text(after)


def test_the_block_is_never_an_undeclared_frontmatter_key(api_store):
    model = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    assert undeclared_frontmatter_keys(model, attach_block("# T\n\nStatus: open\n\n## Tags\n\n- a\n", BLOCK)) == []
    path = api_store.root / "hand.md"
    path.write_text(attach_block("# Hand\n\nStatus: open\n\n## Tags\n\n- a\n", BLOCK), encoding="utf-8")
    api.track_document_file(api_store.store, "TicketDoc", path, "hand", api_store.pythonpath)
    assert provenance_of(path.read_text(encoding="utf-8")).by == "human:jp", "track does not rewrite the file"


def test_the_cli_actor_flag_and_the_env_sign_every_write(api_store, capsys, monkeypatch):
    assert current_actor() == "agent"
    monkeypatch.setenv("SLDB_ACTOR", "agent:env")
    assert current_actor() == "agent:env" and current_actor("agent:explicit") == "agent:explicit"
    args = ["--store", str(api_store.store), "--pythonpath", api_store.pythonpath]
    assert cli_main(["--actor", "human:cli", "docs", "update", "login", json.dumps({**PAYLOAD, "title": "From cli"}), *args]) == 0
    assert provenance_of((api_store.root / "login.md").read_text(encoding="utf-8")).by == "human:cli"
    capsys.readouterr()
    assert cli_main(["docs", "show", "login", *args, "--format", "json"]) == 0
    shown = json.loads(capsys.readouterr().out)["document"]
    assert shown["provenance"]["by"] == "human:cli" and shown["provenance"]["declared"] is True

FILE:instruccion
Cold-bundle de la tarea task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

