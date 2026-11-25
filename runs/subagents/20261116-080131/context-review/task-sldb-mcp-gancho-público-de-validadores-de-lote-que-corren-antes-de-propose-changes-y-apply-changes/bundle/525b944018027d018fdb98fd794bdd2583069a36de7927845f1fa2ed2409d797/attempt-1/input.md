FILE:desk/tasks/task-sldb-mcp-gancho-público-de-validadores-de-lote-que-corren-antes-de-propose-changes-y-apply-changes.md
---
sldb:
  by: agent
  at: '2026-11-16T07:43:46Z'
  authority: generated
  via: save_document_payload
id: task-sldb-mcp-gancho-público-de-validadores-de-lote-que-corren-antes-de-propose-changes-y-apply-changes
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-182013-suggestion-sldb-mcp-gancho-p-blico-de-comprobaciones-de-dominio-antes-de-propose-changes.md
depends_on: []
pills:
- desk/contexts/pill-pill-forma-del-rechazo-de-dominio-en-sldb-mcp.md
files:
- src/sldb/mcp/context.py
- src/sldb/mcp/extension.py
- src/sldb/mcp/server.py
- src/sldb/mcp/write/tools.py
- tests/mcp/test_extension.py
- tests/mcp/example_extension.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb mcp: gancho público de validadores de lote que corren antes de propose_changes y apply_changes

## Rationale

_Explain why this task exists or the business driver behind it._

IR03b monta specir.mcp_extension:register sobre sldb mcp y necesita una regla de dominio antes de proponer cambios (claims_verified, IR05 D2-E: un agente no escribe verificacion: verificado por el MCP). Hoy la extensión quita propose_changes/apply_changes y los vuelve a registrar desde WriteTools con su comprobación, importando internos de sldb.mcp (changes, paging, registry, write). build_server (src/sldb/mcp/server.py:38) solo acepta extensiones Callable[[server, context], None] (src/sldb/mcp/extension.py) y no hay forma de enganchar un validador. Origen: desk/inbox/20261115-182013-suggestion-sldb-mcp-gancho-p-blico-de-comprobaciones-de-dominio-antes-de-propose-changes.md.

## Goal

_Describe the concrete result this task must produce._

Una extensión registra validadores con context.add_batch_validator(fn), donde fn(changes, context) -> list[dict] devuelve findings; propose_changes y apply_changes de WriteTools llaman a todos los validadores antes de su trabajo y, si algún finding tiene level "error", responden rechazado con esos findings y no escriben; los de level "alert" se devuelven en la respuesta sin bloquear.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/mcp/context.py (ServerContext) una lista batch_validators y el método add_batch_validator(fn); BatchValidator = Callable[[list, ServerContext], list[dict]] definido en src/sldb/mcp/extension.py junto a Extension; en src/sldb/mcp/server.py build_server pasa el context a WriteTools (o WriteTools recibe la lista de validadores) y las extensiones se aplican antes de que se sirva la primera llamada; en src/sldb/mcp/write/tools.py propose_changes y apply_changes corren los validadores sobre los changes (en apply, sobre proposal.changes) antes de sellar o aplicar. Un finding es {"code", "level", "what", "subject"} con level en {"error", "alert"}; un rechazo usa apply.rejected("domain", ...) con los findings en detail. Documentar el contrato estable de extensión (Extension, BatchValidator, ServerContext.add_batch_validator) en docs/architecture/ en el doc donde ya se describe sldb mcp. Tests en tests/mcp/test_extension.py: un validador que devuelve error bloquea propose y apply sin escribir; uno con alert deja pasar y aparece en la respuesta; sin validadores el comportamiento es el de hoy. Actualizar tests/mcp/example_extension.py con un validador de ejemplo. CHANGELOG.md. No entra: mover sldb.mcp a sldb.api, cambiar el sellado de propuestas, ni tocar el repo IR.

Precisiones (preflight-1): diseño elegido: build_server pasa el ServerContext a WriteTools (parámetro context), y WriteTools lee context.batch_validators en cada llamada. En propose_changes los validadores corren después de self._require y _check_path y antes de construir el lote; en apply_changes corren después de require y sealer.check, sobre proposal.changes. Se corren todos los validadores siempre (no se corta en el primer error). Si hay algún error, la respuesta es apply.rejected("domain", "<n> domain check(s) failed", findings=<todos los findings, errores y alertas>) y no se escribe. Si solo hay alertas, la respuesta normal gana una clave "domain_alerts" con la lista. El contrato se documenta en docs/architecture/mcp.md.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/mcp/server.py, extension.py, context.py, write/tools.py, write/apply.py y tests/mcp/test_extension.py, tests/mcp/example_extension.py. 2) Agregar BatchValidator y add_batch_validator. 3) Conectar WriteTools con el context. 4) Correr validadores en propose y apply. 5) Tests y doc. 6) grep "mcp" docs/architecture para elegir el doc donde va el contrato.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/mcp/test_extension.py
- TMPDIR=/dev/shm pytest -q tests/mcp/test_write_tools.py

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos de test pasan con los tres casos nuevos; el contrato de extensión está documentado; CHANGELOG y commit; mensaje a IR con deskops message send --to IR (si ese repo no está registrado para el envío, el aviso va como línea "Aviso a IR" en el informe de cierre) avisando el gancho.

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

FILE:desk/contexts/pill-pill-forma-del-rechazo-de-dominio-en-sldb-mcp.md
---
sldb:
  by: agent
  at: '2026-11-16T07:43:25Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-forma-del-rechazo-de-dominio-en-sldb-mcp
status: active
summary: forma del rechazo de dominio en sldb mcp
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: forma del rechazo de dominio en sldb mcp

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

src/sldb/mcp/write/apply.py, src/sldb/mcp/write/tools.py

## How

_Describe the correct way to apply this guidance._

apply.rejected(cause, explanation, **detail) devuelve un dict con detail expandido, así que findings=lista queda como clave 'findings'. propose_changes y apply_changes responden los dos con ese mismo dict cuando hay errores de dominio. 'domain_alerts' se agrega al dict del dry-run de propose y al resultado de apply. Los validadores reciben los mismos objetos de cambio que tiene cada método (Change en propose, BatchChange en apply) y la firma se documenta como 'list de cambios del lote'. Los tres casos nuevos van en tests/mcp/test_extension.py; tests/mcp/test_write_tools.py se corre como regresión.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.

FILE:src/sldb/mcp/context.py
"""What a server knows and an extension may use: the store, the level, the actor and the signal log."""

from __future__ import annotations

from pathlib import Path

import sldb.api as api
from sldb.mcp.mutability import server_level
from sldb.mcp.signals import SignalLog


class ServerContext:
    """The store a server serves, the write level the operator fixed, who signs what it writes
    and the signal log. Handed to every extension next to the server."""

    def __init__(self, store: str | Path, level: int, actor: str | None) -> None:
        location = api.open_store(Path(store), mode="readonly")
        self.store_path, self.project_root = location.store_path, location.project_root
        self.level = server_level(level)
        self.actor = actor
        self.log = SignalLog(self.store_path, actor)

FILE:src/sldb/mcp/extension.py
"""The extension point: a consumer registers its own tools on the server of sldb."""

from __future__ import annotations

import importlib
from typing import Any, Callable

#: `extension(server, context)`: `server.add_tool(fn, name=..., annotations=...)` (or the `tool`
#: decorator) registers a tool that inherits the guard, the paging helpers (`sldb.mcp.paging`),
#: the actor and the signal log; `context` is a `ServerContext`.
Extension = Callable[[Any, Any], None]


def load_extension(spec: str) -> Extension:
    """The function named by `module:function`."""
    module, _, function = spec.partition(":")
    if not module or not function:
        raise ValueError(f"an extension is written module:function, not {spec!r}")
    found = getattr(importlib.import_module(module), function, None)
    if not callable(found):
        raise ValueError(f"{spec!r}: {module} has no callable {function!r}")
    return found

FILE:src/sldb/mcp/server.py
"""The sldb MCP server over stdio: `sldb mcp --store <project>/.sldb --level 0|1|2 --actor <who>`.

Level 0 (the default) serves the read tools and `list_signals`, all read-only: none writes to
the store or to its linked stores. `--level 1` (content) adds `propose_changes` and
`apply_changes`; `--level 2` also lets them write the store's rules as data. The level is the
operator's, never a tool argument. A consumer adds tools of its own with `--extension
module:function` or `build_server(..., extensions=[...])`. Every tool returns structured JSON."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from sldb.mcp.context import ServerContext
from sldb.mcp.extension import Extension, load_extension
from sldb.mcp.mutability import READ
from sldb.mcp.read import ReadTools
from sldb.mcp.registry import register_read, register_write
from sldb.mcp.signal_server import SignalServer
from sldb.mcp.signals import SignalTools
from sldb.mcp.write import WriteTools

INSTRUCTIONS = (
    "Read-only access to one SLDB store and the stores it links. Documents are named "
    "`Model:name` (`alias:Model:name` in a linked store); every document carries its stable "
    "address `sldb://document/<export id>`. Sets come as pages {items, total, offset, limit, "
    "truncated, next_offset}; an empty set carries an `explanation`. Asking for what does not "
    "exist (a tool, model, document, field, relation type, view or argument) is not an error: "
    "it is registered as a signal, answered with near names, and listed by list_signals."
)
WRITE_INSTRUCTIONS = (
    " Writing is two steps: propose_changes (typed changes; writes nothing and answers what "
    "would be written) and apply_changes (the proposal exactly as returned; applied whole or "
    "not at all, or rejected with its cause)."
)


def build_server(store: str | Path, level: int = READ, actor: str | None = None, extensions: Sequence[Extension] = ()) -> SignalServer:
    """An MCP server whose tools read `store` through `sldb.api`, write it at `level` >= 1, and
    carry the tools each of `extensions` (`extension(server, context)`) registers."""
    context = ServerContext(store, level, actor)
    server = SignalServer(context, instructions=INSTRUCTIONS + (WRITE_INSTRUCTIONS if level > READ else ""))
    register_read(server, ReadTools(store), SignalTools(context.log))
    if level > READ:
        register_write(server, WriteTools(store, level, actor))
    for extension in extensions:
        extension(server, context)
    return server


def serve(store: str | Path, level: int = READ, actor: str | None = None, extensions: Sequence[str] = ()) -> None:
    """Serve `store` over stdio until the client goes away; `extensions` are `module:function`."""
    build_server(store, level, actor, [load_extension(spec) for spec in extensions]).run("stdio")

FILE:src/sldb/mcp/write/tools.py
"""The write surface over one SLDB store, at the level the server was started with."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.api.actor import set_actor
from sldb.mcp.changes import Change, Proposal, Sealer, model_of
from sldb.mcp.mutability import CONTENT, model_level, require, server_level
from sldb.mcp.write import apply, pendings, propose
from sldb.mcp.write.pending import PENDING

#: Who signs the provenance of what this server writes (an agent writes `authored` as
#: `agent:<id>`); `--actor` names the agent.
DEFAULT_ACTOR = "agent:sldb-mcp"


class WriteTools:
    """`propose_changes` (the dry run) and `apply_changes` (whole or nothing), through `sldb.api`."""

    def __init__(self, store: str | Path, level: int, actor: str | None = None) -> None:
        self.level = server_level(level)
        location = api.open_store(Path(store))
        self.store_path, self.project_root = location.store_path, location.project_root
        self.actor = actor or DEFAULT_ACTOR
        set_actor(self.actor)
        self.sealer = Sealer()

    def propose_changes(self, changes: list[Change]) -> dict[str, Any]:
        """Dry run: turn typed changes (create/update/delete a document, assert_edge/retract_edge)
        into a sealed proposal with the server's guards, and answer what it would write. Writes nothing."""
        self._require(changes, "propose_changes")
        for change in changes:
            self._check_path(change)
        fingerprint = api.store_fingerprint(self.store_path)
        batch = [propose.batch_change(self.store_path, change, fingerprint) for change in changes]
        level = max(model_level(c.model) for c in batch)
        sealed = Proposal(changes=batch, level=level, store_hash=fingerprint.store_hash, seal=self.sealer.seal(batch, level, fingerprint.store_hash))
        return self._dry_run(sealed)

    def apply_changes(self, proposal: Proposal) -> dict[str, Any]:
        """Apply a proposal exactly as propose_changes returned it: whole, or nothing and why
        (`stale` when the store changed since, `rules` naming the RuleDocs that refused it)."""
        require(self.level, max([CONTENT, *(model_level(c.model) for c in proposal.changes)]), "apply_changes")
        self.sealer.check(proposal)
        return apply.run_batch(self.store_path, proposal)

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

FILE:tests/mcp/test_extension.py
"""The extension point: a consumer registers tools of its own on the server of sldb and inherits
its level, its actor, its paging and its signal log."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterator

import pytest

from mcp_helpers import files, page_items
from mcp_session import HERE, WRITER, McpSession, copy_of, server_env, served
from mcp_world import ITEM_COUNT
from test_read_tools import TOOLS

EXTENSION_TOOLS = {"count_by_model", "whoami", "find_model"}
SPEC = "example_extension:register"


@pytest.fixture(scope="module")
def extended_copy(built_world: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    return copy_of(built_world, tmp_path_factory, "mcp-extension")


@pytest.fixture(scope="module")
def extended(extended_copy: Path) -> Iterator[McpSession]:
    """The server at level 1 with the example extension, over its own copy."""
    with served(extended_copy, "--level", "1", "--actor", WRITER, "--extension", SPEC, extra_path=(HERE,)) as session:
        yield session


def test_the_extension_tools_join_the_built_in_ones(extended) -> None:
    names = {t.name for t in extended.list_tools()}
    assert names == TOOLS | {"propose_changes", "apply_changes"} | EXTENSION_TOOLS
    described = next(t for t in extended.list_tools() if t.name == "count_by_model")
    assert described.description and described.output_schema is not None


def test_an_extension_tool_pages_like_the_built_in_ones(extended, extended_copy: Path) -> None:
    rows = page_items(extended, "count_by_model", limit=2)
    assert {r["model"]: r["documents"] for r in rows}["Item"] == ITEM_COUNT == len(files(extended_copy, "item"))
    first = extended.call("count_by_model", limit=2)
    assert first["truncated"] and first["next_offset"] == 2 and len(first["items"]) == 2
    assert extended.call("count_by_model", model="Item")["total"] == 1


def test_an_extension_tool_sees_the_level_and_the_actor_of_the_server(extended) -> None:
    assert extended.call("whoami") == {"level": 1, "level_name": "content", "actor": WRITER}


def test_an_extension_tool_inherits_the_signal_log(extended, extended_copy: Path) -> None:
    misspelled = extended.portal.call(lambda: extended.client.call_tool("count_by_model", {"modle": "Item"}))
    assert misspelled.is_error is False and misspelled.structured_content["signal"] == "unknown_argument"
    assert "model" in misspelled.structured_content["suggestions"]
    answer = extended.call("find_model", name="Itm")
    assert answer["signal"] == "unknown_model" and answer["registered_as_signal"] is True and "Item" in answer["suggestions"]
    entries = extended.call("list_signals", limit=500)["items"]
    assert [(e["tool"], e["signal_class"], e["actor"]) for e in entries[-2:]] == [("count_by_model", "unknown_argument", WRITER), ("find_model", "unknown_model", WRITER)]
    assert extended.call("find_model", name="Item")["found"] is True


def test_an_extension_that_does_not_exist_stops_the_server(extended_copy: Path) -> None:
    for spec in ("no_such_module_for_sldb:register", "example_extension:no_such_function", "not-a-spec"):
        done = subprocess.run([sys.executable, "-m", "sldb", "mcp", "--store", str(extended_copy / ".sldb"), "--extension", spec], capture_output=True, text=True, timeout=120, cwd=extended_copy, env=server_env((HERE,)))
        assert done.returncode != 0 and spec.split(":")[0] in done.stderr + done.stdout, (spec, done.stderr)

FILE:tests/mcp/example_extension.py
"""A consumer's extension, the way specIR would write one: domain tools on the server of sldb.

Loaded by the tests with `--extension example_extension:register`."""

from __future__ import annotations

from typing import Any

import sldb.api as api
from sldb.mcp.mutability import LEVELS
from sldb.mcp.paging import DEFAULT_LIMIT, page


def register(server: Any, context: Any) -> None:
    """Two tools over the store of the context: one that pages, one that misses on purpose."""

    @server.tool()
    def count_by_model(model: str | None = None, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """How many documents each registered model tracks (or one model's), as a page."""
        rows = api.select_documents(context.store_path, {"include_linked": True})
        counts = {m.name: sum(1 for r in rows if r["model"] == m.name) for m in api.registered_models(context.store_path) if model in (None, m.name)}
        return page([{"model": name, "documents": total} for name, total in sorted(counts.items())], offset, limit)

    @server.tool()
    def whoami() -> dict[str, Any]:
        """The level and the actor this server was started with."""
        return {"level": context.level, "level_name": LEVELS[context.level], "actor": context.actor}

    @server.tool()
    def find_model(name: str) -> dict[str, Any]:
        """A registered model by name; a name it does not know is a signal, not an error."""
        known = [m.name for m in api.registered_models(context.store_path)]
        return {"found": True, "name": name} if name in known else {"found": False, "name": name, "explanation": f"no model {name!r}", "signal": {"class": "unknown_model", "name": name}}

FILE:instruccion
Cold-bundle de la tarea task-sldb-mcp-gancho-público-de-validadores-de-lote-que-corren-antes-de-propose-changes-y-apply-changes: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/mcp/test_extension.py
- TMPDIR=/dev/shm pytest -q tests/mcp/test_write_tools.py

