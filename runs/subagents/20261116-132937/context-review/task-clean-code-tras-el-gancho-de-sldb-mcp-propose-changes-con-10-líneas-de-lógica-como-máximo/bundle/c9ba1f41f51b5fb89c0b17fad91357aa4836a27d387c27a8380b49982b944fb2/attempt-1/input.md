FILE:desk/tasks/task-clean-code-tras-el-gancho-de-sldb-mcp-propose-changes-con-10-líneas-de-lógica-como-máximo.md
---
sldb:
  by: agent
  at: '2026-11-16T13:10:32Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-el-gancho-de-sldb-mcp-propose-changes-con-10-líneas-de-lógica-como-máximo
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
- src/sldb/mcp/write/tools.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
---

# Clean code tras el gancho de sldb mcp: propose_changes con 10 líneas de lógica como máximo

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: el método propose_changes de src/sldb/mcp/write/tools.py tiene 11 líneas de lógica (máximo 10). Lo introdujo task-sldb-mcp-gancho (11b6c537); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-sldb-mcp-gancho, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Extraer la corrida de validadores de dominio y la respuesta de rechazo (o el armado del lote sellado) a un método o función privada con nombre, compartida con apply_changes si aplica. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_extension.py
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_write_tools.py
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

FILE:desk/atoms/atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si.md
---
sldb:
  by: agent
  at: '2026-11-16T10:51:16Z'
  authority: generated
  via: create_document
id: atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
title: Una extensión de sldb mcp agrega reglas de dominio a la escritura registrando
  validadores de lote, sin reemplazar las herramientas de escritura
five_wh_one_plus: what
tags:
- system:sldb
- topic:mcp
provenance: src/sldb/mcp/extension.py
---

# Una extensión de sldb mcp agrega reglas de dominio a la escritura registrando validadores de lote, sin reemplazar las herramientas de escritura

## Answer

Una extensión de sldb mcp llama context.add_batch_validator(fn), con fn(changes, context) -> list[dict] y cada finding {code, level, what, subject}. WriteTools corre todos los validadores en propose_changes y en apply_changes antes de sellar o aplicar. Si algún finding es de nivel error, responde apply.rejected('domain', ...) con findings y no escribe. Las alertas viajan en domain_alerts sin bloquear. El contrato estable (Extension, BatchValidator, ServerContext.add_batch_validator) está en docs/architecture/mcp.md.

FILE:src/sldb/mcp/write/tools.py
"""The write surface over one SLDB store, at the level the server was started with."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import sldb.api as api
from sldb.api.actor import set_actor
from sldb.mcp.changes import Change, Proposal, Sealer, model_of
from sldb.mcp.mutability import CONTENT, model_level, require, server_level
from sldb.mcp.write import apply, pendings, propose
from sldb.mcp.write.pending import PENDING

if TYPE_CHECKING:
    from sldb.mcp.context import ServerContext

#: Who signs the provenance of what this server writes (an agent writes `authored` as
#: `agent:<id>`); `--actor` names the agent.
DEFAULT_ACTOR = "agent:sldb-mcp"


class WriteTools:
    """`propose_changes` (the dry run) and `apply_changes` (whole or nothing), through `sldb.api`."""

    def __init__(self, store: str | Path, level: int, actor: str | None = None, context: ServerContext | None = None) -> None:
        self.level = server_level(level)
        location = api.open_store(Path(store))
        self.store_path, self.project_root = location.store_path, location.project_root
        self.actor = actor or DEFAULT_ACTOR
        set_actor(self.actor)
        self.sealer = Sealer()
        self.context = context

    def propose_changes(self, changes: list[Change]) -> dict[str, Any]:
        """Dry run: turn typed changes (create/update/delete a document, assert_edge/retract_edge)
        into a sealed proposal with the server's guards, and answer what it would write. Writes nothing."""
        self._require(changes, "propose_changes")
        for change in changes:
            self._check_path(change)
        findings = self._domain_findings(changes)
        if self._has_errors(findings):
            return self._domain_rejected(findings)
        fingerprint = api.store_fingerprint(self.store_path)
        batch = [propose.batch_change(self.store_path, change, fingerprint) for change in changes]
        level = max(model_level(c.model) for c in batch)
        sealed = Proposal(changes=batch, level=level, store_hash=fingerprint.store_hash, seal=self.sealer.seal(batch, level, fingerprint.store_hash))
        return self._with_alerts(self._dry_run(sealed), findings)

    def apply_changes(self, proposal: Proposal) -> dict[str, Any]:
        """Apply a proposal exactly as propose_changes returned it: whole, or nothing and why
        (`stale` when the store changed since, `rules` naming the RuleDocs that refused it)."""
        require(self.level, max([CONTENT, *(model_level(c.model) for c in proposal.changes)]), "apply_changes")
        self.sealer.check(proposal)
        findings = self._domain_findings(proposal.changes)
        if self._has_errors(findings):
            return self._domain_rejected(findings)
        return self._with_alerts(apply.run_batch(self.store_path, proposal), findings)

    def _domain_findings(self, changes: list[Any]) -> list[dict[str, Any]]:
        """What every batch validator an extension registered finds in `changes` (all of them run)."""
        if self.context is None:
            return []
        return [finding for validator in self.context.batch_validators for finding in validator(list(changes), self.context)]

    @staticmethod
    def _has_errors(findings: list[dict[str, Any]]) -> bool:
        return any(f.get("level") == "error" for f in findings)

    @staticmethod
    def _domain_rejected(findings: list[dict[str, Any]]) -> dict[str, Any]:
        """A batch a validator refused: nothing sealed or written, with every finding."""
        errors = sum(1 for f in findings if f.get("level") == "error")
        return apply.rejected("domain", f"{errors} domain check(s) failed", findings=findings)

    @staticmethod
    def _with_alerts(answer: dict[str, Any], findings: list[dict[str, Any]]) -> dict[str, Any]:
        """The answer, with the validators' alerts as `domain_alerts` when there are any."""
        return {**answer, "domain_alerts": findings} if findings else answer

    def _dry_run(self, proposal: Proposal) -> dict[str, Any]:
        """The answer of a dry run: the proposal and what it would write."""
        checked = "apply_batch prevalidates the whole batch (shape, registered model, payload round-trip, guards, free destination) and runs the on_write RuleDocs; nothing is written if any check fails"
        pending = [PENDING["dry_run"], *pendings.edge_pending(proposal.changes), *pendings.level_pending(proposal.level)]
        would = [propose.would_write(self.store_path, c) for c in proposal.changes]
        return {"dry_run": True, "written": False, "proposal": proposal.model_dump(mode="json"), "would_write": would, "checked_on_apply": checked, "pending": pending}

    @staticmethod
    def _check_path(change: Any) -> None:
        """No tool writes code or any other file than Markdown."""
        path = getattr(change, "path", None)
        if path is not None and not path.endswith(".md"):
            raise ValueError(f"{change.name}: {path!r} is not a Markdown document; no tool writes code or any other file")

    def _require(self, changes: list[Any], tool: str) -> None:
        """Refuse before reading the store: the tool's level, then each change's model's."""
        require(self.level, CONTENT, tool)
        if not changes:
            raise ValueError("propose at least one change")
        for change in changes:
            require(self.level, model_level(model_of(change)), f"{tool} on {model_of(change)}:{change.name}")

FILE:instruccion
Cold-bundle de la tarea task-clean-code-tras-el-gancho-de-sldb-mcp-propose-changes-con-10-líneas-de-lógica-como-máximo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_extension.py
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_write_tools.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

