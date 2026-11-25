FILE:desk/tasks/task-test-apply-batch-lock-no-deja-procesos-huérfanos-el-segundo-proceso-termina-siempre-falle-o-venza-el.md
---
sldb:
  by: agent
  at: '2026-11-17T12:35:02Z'
  authority: generated
  via: create_document
id: task-test-apply-batch-lock-no-deja-procesos-huérfanos-el-segundo-proceso-termina-siempre-falle-o-venza-el
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-092921-suggestion-procesos-hu-rfanos-de-test-second-process-with-the-s-apply-batch-con-hold-en-dev-shm.md
depends_on: []
pills: []
files:
- tests/api/test_apply_batch_lock.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
---

# test_apply_batch_lock no deja procesos huérfanos: el segundo proceso termina siempre, falle o venza el test

## Rationale

_Explain why this task exists or the business driver behind it._

En robocop2 quedaron dos procesos huérfanos de tests/api/test_apply_batch_lock.py (test_second_process_with_the_same_guard_conflicts_and_leaves_no_partial_write), uno de 19 h y otro de 16 h, esperando un archivo marks/go que nunca llega: la prueba no limpia el proceso que retiene el cerrojo si falla o vence su timeout. Ocupan memoria en una máquina que ya colapsó por RAM. Origen: desk/inbox/20261117-092921-suggestion-procesos-hu-rfanos-de-test-second-process-with-the-s-apply-batch-con-hold-en-dev-shm.md.

## Goal

_Describe the concrete result this task must produce._

Cada proceso que lanza test_apply_batch_lock.py termina siempre al salir del test (pase, falle o venza), y la espera del archivo de señal tiene un tope; un test que falla no deja ningún proceso vivo.

## Scope

_State what is in scope and what is out of scope._

Entra: en tests/api/test_apply_batch_lock.py, lanzar los procesos en un contexto que los mata y los espera en finally (o una fixture con yield), y poner un tope de tiempo a la espera de marks/go dentro del proceso hijo, para que salga solo si el padre muere; un test que simula un fallo del padre y comprueba que no queda ningún hijo vivo. No entra: cambiar apply_batch ni lock.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/api/test_apply_batch_lock.py. 2) Implementar la limpieza y el tope. 3) Test del caso de fallo. 4) Validation, comprobando con ps que no quedan procesos del test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; tras forzar un fallo del test no queda ningún proceso python del test vivo; commit; aviso a IR.

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

FILE:desk/atoms/atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso.md
---
sldb:
  by: agent
  at: '2026-11-16T19:44:52Z'
  authority: generated
  via: create_document
id: atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
title: apply_batch prevalida y escribe bajo el cerrojo del store y rechaza con ConflictError
  un guarda obsoleto
five_wh_one_plus: what
tags:
- system:sldb
- topic:store-lock
provenance: tarea 022444, piloto scion + ejecutor deskops-e-4e4ba795934b, tester deskops-t-a6ddcc3e4afc
  PASA
---

# apply_batch prevalida y escribe bajo el cerrojo del store y rechaza con ConflictError un guarda obsoleto

## Answer

apply_batch toma store_lock(store, wait=True) alrededor de la prevalidación y de toda la transacción; update pasa expected_source_hash y expected a tx.update, y delete, move y untrack quedan protegidos porque la prevalidación corre bajo el mismo cerrojo. StoreIOLock es reentrante dentro del proceso (contador por ruta resuelta), así que una escritura anidada no se bloquea a sí misma. Dos procesos con el mismo guarda: uno escribe y el otro recibe ConflictError sin escritura parcial. La exclusión es por proceso, no por hilo.

FILE:tests/api/test_apply_batch_lock.py
"""`apply_batch` holds the store lock from prevalidation to the last write: with two real
processes carrying the same `expected_source_hash`, one wins and the other gets `ConflictError`
and writes nothing, not even the other change of its batch."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path

from sldb.api.stores.store_check import check_store
from sldb.store.io import store_lock
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path

CHILD = r'''
import sys, time
from pathlib import Path
import sldb.api as api
import sldb.api.documents.apply_batch as ab
from sldb.core.exceptions import ConflictError

store, pythonpath, hold, marks, title, source_hash = sys.argv[1:7]
marks = Path(marks)
real = ab.prevalidate_changes
def marked(*args, **kwargs):
    plan = real(*args, **kwargs)
    (marks / ("ready" if hold == "1" else "entered")).write_text("x")
    while hold == "1" and not (marks / "go").exists():
        time.sleep(0.02)                    # the first holds here, after prevalidating
    return plan
ab.prevalidate_changes = marked
payload = {"title": title, "status": "open", "tags": ["auth"]}
changes = [
    {"id": "login", "action": "update", "payload": payload, "expected_source_hash": source_hash},
    {"id": "extra-" + title.lower(), "action": "create", "model": "TicketDoc", "payload": payload, "path": "extra-" + title.lower() + ".md"},
]
(marks / ("started" if hold == "0" else "_")).write_text("x")
try:
    api.apply_batch(store, changes, pythonpath)
    print("OK")
except ConflictError:
    print("CONFLICT")
'''


def _spawn(api_store, tmp_path, hold, title, source_hash):
    args = [sys.executable, "-c", CHILD, str(api_store.store), api_store.pythonpath, hold, str(tmp_path), title, source_hash]
    return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _wait_for(path: Path) -> None:
    for _ in range(500):
        if path.exists():
            return
        time.sleep(0.02)


def _shard(api_store, name: str):
    return load_document_shard(documents_shard_path(api_store.store, "TicketDoc", name))


def test_second_process_with_the_same_guard_conflicts_and_leaves_no_partial_write(api_store, tmp_path):
    source_hash = _shard(api_store, "login").source_hash
    first = _spawn(api_store, tmp_path, "1", "Winner", source_hash)
    _wait_for(tmp_path / "ready")
    assert (tmp_path / "ready").exists(), first.communicate()
    second = _spawn(api_store, tmp_path, "0", "Loser", source_hash)
    _wait_for(tmp_path / "started")
    assert (tmp_path / "started").exists(), second.communicate()
    time.sleep(1.0)
    assert not (tmp_path / "entered").exists()  # the second waits on the lock before prevalidating
    (tmp_path / "go").write_text("x")
    out1, err1 = first.communicate(timeout=60)
    out2, err2 = second.communicate(timeout=60)
    assert (out1.strip(), out2.strip()) == ("OK", "CONFLICT"), (err1, err2)
    login = (api_store.root / "login.md").read_bytes()
    assert b"Winner" in login and b"Loser" not in login
    assert _shard(api_store, "login").source_hash.removeprefix("sha256:") == hashlib.sha256(login).hexdigest() != source_hash
    assert (api_store.root / "extra-winner.md").exists()
    assert not (api_store.root / "extra-loser.md").exists()  # the loser's create was not written
    assert not documents_shard_path(api_store.store, "TicketDoc", "extra-loser").exists()
    assert check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]


def test_store_lock_is_reentrant_in_process_and_keeps_excluding_others(api_store):
    other = [sys.executable, "-c", "import sys\nfrom pathlib import Path\nfrom sldb.store.io import store_lock\nfrom sldb.store.exceptions import SLDBStoreError\ntry:\n    with store_lock(Path(sys.argv[1])): print('GOT')\nexcept SLDBStoreError: print('BUSY')", str(api_store.store)]
    with store_lock(api_store.store, wait=True):
        with store_lock(api_store.store):
            pass
        assert subprocess.run(other, capture_output=True, text=True, timeout=60).stdout.strip() == "BUSY"  # the inner release did not drop the outer lock
    assert subprocess.run(other, capture_output=True, text=True, timeout=60).stdout.strip() == "GOT"

FILE:instruccion
Cold-bundle de la tarea task-test-apply-batch-lock-no-deja-procesos-huérfanos-el-segundo-proceso-termina-siempre-falle-o-venza-el: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

