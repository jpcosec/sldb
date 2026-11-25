FILE:desk/tasks/task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar.md
---
sldb:
  by: agent
  at: '2026-11-17T01:44:27Z'
  authority: generated
  via: create_document
id: task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-214137-suggestion-stores-check-errores-rules-builtin-tag-namespace-domain-llegan-con-fix-vac-o.md
depends_on: []
pills: []
files:
- src/sldb/api/rules/builtin_tag_findings.py
- tests/api/test_rules_evaluation.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La regla builtin tag_namespace:domain sugiere un fix concreto en stores check (qué namespace declarar o qué tag cambiar)

## Rationale

_Explain why this task exists or the business driver behind it._

En el store de sldb-ui, stores check --format json devuelve 5 errores rules/builtin:tag_namespace:domain con fix vacío, y la UI solo puede decir que el CLI no sugirió nada. Origen: desk/inbox/20261116-214137-suggestion-stores-check-errores-rules-builtin-tag-namespace-domain-llegan-con-fix-vac-o.md.

## Goal

_Describe the concrete result this task must produce._

Cada hallazgo de la regla builtin tag_namespace:domain trae en fix un texto accionable: el namespace a declarar en la política del store (con el comando o la clave exacta) o los tags válidos de ese namespace.

## Scope

_State what is in scope and what is out of scope._

Entra: el texto de fix en src/sldb/api/rules/builtin_tag_findings.py (y builtin_tag_rules.py si hace falta) para esa regla, nombrando el namespace y la acción; revisar las demás reglas builtin de tags y llenar su fix si también está vacío; tests en tests/api/test_rules_evaluation.py. CHANGELOG. No entra: cambiar qué detecta la regla.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer builtin_tag_rules.py y builtin_tag_findings.py. 2) Llenar fix. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_tags.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; ningún hallazgo builtin de tags sale con fix vacío; CHANGELOG y commit; aviso a sldb-ui.

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

FILE:src/sldb/api/rules/builtin_tag_findings.py
"""The findings of the built-in family `builtin:tag_namespace:*` (GD27) and the evaluations
behind them (H6): the pass over documents that `rules check`, `on_write`, `on_check` and
`tags check` share; the evaluation of one document is `builtin_tag_rules.evaluate`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.builtin_tag_rules import PREFIX, evaluate, in_scope, payload_of, tag_rules, tag_scope
from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.stores.open_store import open_store
from sldb.core.finding import Finding
from sldb.store.semantic_tags import namespaced_tags


def store_findings(store: str | Path | None) -> list[Finding]:
    """The family over every local document; a store without namespaces is not read."""
    store_path = open_store(store, mode="readonly").store_path
    return family_findings(rule_graph(store_path, None), None) if tag_rules(store_path) else []


def family_evaluations(graph: RuleGraph, nodes: list[str] | None) -> list[tuple[str, dict[str, Any]]]:
    """Every evaluation of the family on `nodes` (every local document when None), by document
    then namespace: `(namespace, eval finding)`. Findings and `tag_evaluations` read this one pass."""
    rules, models = tag_rules(graph.store_path), tag_scope(graph.store_path)
    scoped = [node for node in (sorted(graph.local) if nodes is None else nodes) if in_scope(graph, models, node)] if rules else []
    return [(name, evaluate(graph, rules, name, node)) for node in scoped for name in _names(graph, node)]


def family_findings(graph: RuleGraph, nodes: list[str] | None) -> list[Finding]:
    """The findings on `nodes` (every local document when None), by document then namespace."""
    return findings_of(graph, family_evaluations(graph, nodes))


def findings_of(graph: RuleGraph, evaluations: list[tuple[str, dict[str, Any]]]) -> list[Finding]:
    """The error findings of the evaluations that do not hold."""
    return [_finding(graph, name, result) for name, result in evaluations if result["holds"] != "true"]


def _names(graph: RuleGraph, node: str) -> list[str]:
    return sorted({namespace for namespace, _ in namespaced_tags(payload_of(graph, node))})




def _finding(graph: RuleGraph, name: str, found: dict[str, Any]) -> Finding:
    from sldb.api.rules.rules_check import explanation

    what = explanation({"name": PREFIX + name}, found)
    return Finding("error", f"rules/{PREFIX}{name}", found["node"], what, "", graph.semantics(found["node"]).get("path"))

FILE:tests/api/test_rules_evaluation.py
"""GO08: the rules evaluated when they are due (docs/architecture/rules.md §9).

`on_write` refuses a write on an error (nothing persisted, the explanation in the envelope) and
lets an alert pass (persisted, in `warnings`); `on_transition` keeps the edges of
`edges_holding` with their alerts and moves an edge an error blocks to `edges_blocked`;
`stores check` reports the `on_check` rules and the document anchors, exit 1 only on an error;
the `on_check` cache recomputes nothing when nothing changed, a whole family when its rule
changes, and gives the same findings without `.sldb_cache`; a closure terminates on a cycle;
`edges check` fails on a condition that does not parse.
"""

from __future__ import annotations

import importlib
import json
import shutil
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main
from sldb.core.exceptions import SLDBRuleViolationError
from sldb.store.layout import cache_dir

on_check_module = importlib.import_module("sldb.api.rules.rules_on_check")
MODULE = "sldb_go08_rule_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class X(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = "---\\nstatus: ⸢rev•status⸥\\ndepends_on: ⸢rev•depends_on⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(default="", description="Status.")
    depends_on: str = Field(default="", description="Referenced document.")


class Sub(X):
    pass


class State(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''
RULE = {"title": "closed", "subject": "model <= X", "condition": 'status = "closed"', "severity": "error", "moment": "on_check"}


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for ref in (f"{MODULE}:X", f"{MODULE}:Sub", f"{MODULE}:State", "sldb.models.rule_doc:RuleDoc"):
            api.add_model(self.store, ref, self.py)
        api.init_relations(self.store, self.py)
        for name in ("x1", "x2"):
            self.doc("X", name, {"title": name, "status": "open"})

    def doc(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def rule(self, name: str, **fields) -> None:
        api.create_document(self.store, "RuleDoc", self.root / "rules" / f"{name}.md", {**RULE, "title": name, **fields}, name, self.py)

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, payload, self.py)

    def envelope(self, capsys, *argv: str, pythonpath: bool = True) -> dict:
        main(["--envelope", *argv, "--store", str(self.store)] + (["--pythonpath", self.py] if pythonpath else []))
        return json.loads(capsys.readouterr().out)


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


@pytest.fixture
def recomputed(monkeypatch) -> list[str]:
    """Every recalculation (p8): one call of `recompute` per rule-document pair."""
    calls: list[str] = []
    real = on_check_module.recompute

    def counted(graph, rule, node):
        calls.append(f"{rule['name']}@{node}")
        return real(graph, rule, node)

    monkeypatch.setattr(on_check_module, "recompute", counted)
    return calls


def _codes(findings) -> list[tuple[str, str, str]]:
    return [(f.level, f.code, f.subject) for f in findings]


def test_an_error_rule_refuses_the_write_and_nothing_is_persisted(world: World, capsys) -> None:
    world.rule("closed", moment="on_write")
    before = (world.root / "x1.md").read_text(encoding="utf-8")
    with pytest.raises(SLDBRuleViolationError) as refused:
        world.save("X", "x1", {"title": "x1", "status": "review"})
    assert str(refused.value) == 'rules/closed: status = "closed" (seen: {"status":"review"})'
    assert (world.root / "x1.md").read_text(encoding="utf-8") == before
    assert api.edge_node(world.store, "X:x1").payload["status"] == "open"
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    assert (envelope["ok"], envelope["exit"], envelope["error"]["type"]) == (False, 1, "rules/violation")
    assert 'rules/closed: status = "closed" (seen: {"status":"review"})' in envelope["error"]["message"]
    assert (world.root / "x1.md").read_text(encoding="utf-8") == before


def test_two_error_rules_are_both_in_the_envelope_ordered_by_rule(world: World, capsys) -> None:
    world.rule("b-titled", moment="on_write", condition='title = "other"')
    world.rule("a-closed", moment="on_write")
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    lines = envelope["error"]["message"].splitlines()
    assert [line.split(":", 1)[0] for line in lines] == ["rules/a-closed", "rules/b-titled"]
    assert envelope["error"]["type"] == "rules/violation"


def test_an_alert_rule_lets_the_write_pass_and_reports_it_in_warnings(world: World, capsys) -> None:
    world.rule("closed", moment="on_write", severity="alert")
    envelope = world.envelope(capsys, "fields", "update", "docs/X/x1/status", "review")
    assert (envelope["ok"], [w["code"] for w in envelope["warnings"]]) == (True, ["rules/closed"])
    assert envelope["warnings"][0]["subject"] == "X:x1" and "review" in envelope["warnings"][0]["what"]
    assert api.edge_node(world.store, "X:x1").payload["status"] == "review"


def test_a_document_not_yet_indexed_is_refused_by_a_rule_on_its_base_family(world: World) -> None:
    from sldb.store.layout import edges_shard_path

    world.rule("closed", moment="on_write")
    world.doc("Sub", "s1", {"title": "s1", "status": "closed"})
    edges_shard_path(world.store, "Sub", "s1").unlink()
    assert api.edge_node(world.store, "Sub:s1") is None
    before = (world.root / "s1.md").read_text(encoding="utf-8")
    with pytest.raises(SLDBRuleViolationError, match="rules/closed"):
        world.save("Sub", "s1", {"title": "s1", "status": "open"})
    assert (world.root / "s1.md").read_text(encoding="utf-8") == before


def test_a_store_without_on_write_rules_writes_as_before(world: World) -> None:
    world.rule("closed")
    world.save("X", "x1", {"title": "x1", "status": "review"})
    assert api.edge_node(world.store, "X:x1").payload["status"] == "review"


def _machine(world: World) -> None:
    for state in ("open", "done"):
        world.doc("State", state, {"title": state})
    world.doc("RelationTypeDoc", "rt-moves", {"title": "moves", "name": "moves_to", "source_types": ["State"], "target_types": ["State"], "description": "A transition."})
    payload = {"title": "finish", "source_id": "State:open", "target_id": "State:done", "relation_type": "moves_to", "attributes": {"sets": {"status": "done"}}}
    world.doc("RelationDoc", "e-finish", payload)


def test_edges_holding_carries_the_alerts_and_an_error_moves_the_edge_to_edges_blocked(world: World) -> None:
    _machine(world)
    subject = {"title": "x1", "status": "open"}
    world.rule("titled", moment="on_transition", severity="alert", condition='title = "x9"')
    [edge] = api.edges_holding(world.store, "State:open", subject, "moves_to", document="X:x1")
    assert edge.effects == {"sets": {"status": "done"}, "terminal": False}
    assert _codes(edge.findings) == [("alert", "rules/titled", "X:x1")]
    assert api.edges_blocked(world.store, "State:open", subject, "moves_to", document="X:x1") == []
    world.rule("closed", moment="on_transition")
    assert api.edges_holding(world.store, "State:open", subject, "moves_to", document="X:x1") == []
    [blocked] = api.edges_blocked(world.store, "State:open", subject, "moves_to", document="X:x1")
    assert blocked.target == "sldb://document/State:done" and blocked.effects == edge.effects
    assert _codes(blocked.findings) == [("error", "rules/closed", "X:x1"), ("alert", "rules/titled", "X:x1")]
    assert "findings" not in api.edges_holding(world.store, "State:open", subject, "moves_to")[0].model_dump()


def test_stores_check_reports_on_check_rules_and_doc_anchors_and_fails_only_on_error(world: World, capsys, monkeypatch) -> None:
    from sldb.core.finding import alert

    anchor = alert("anchors/doc_changed", "X:x2", "subject: doc:X:x1 is changed")
    monkeypatch.setattr(on_check_module, "check_doc_anchors", lambda store, pythonpath=None: [anchor])
    world.rule("closed", severity="alert")
    envelope = world.envelope(capsys, "stores", "check", "--format", "json")
    assert (envelope["ok"], sorted(w["code"] for w in envelope["warnings"])) == (True, ["anchors/doc_changed", "rules/closed", "rules/closed"])
    world.rule("titled", condition='title = "x1"')
    envelope = world.envelope(capsys, "stores", "check", "--format", "json")
    assert (envelope["ok"], envelope["exit"]) == (False, 1)
    assert [(e["code"], e["subject"]) for e in envelope["data"]["errors"]] == [("rules/titled", "X:x2")]


def test_a_second_check_recomputes_nothing_and_a_changed_rule_recomputes_its_family(world: World, recomputed: list[str]) -> None:
    world.rule("closed")
    first = _codes(api.rules_on_check(world.store))
    assert first == [("error", "rules/closed", "X:x1"), ("error", "rules/closed", "X:x2")] and len(recomputed) == 2
    recomputed.clear()
    assert _codes(api.rules_on_check(world.store)) == first and recomputed == []
    world.save("RuleDoc", "closed", {**RULE, "condition": 'status = "open"'})
    assert api.rules_on_check(world.store) == [] and sorted(recomputed) == ["closed@X:x1", "closed@X:x2"]


def test_a_write_dirties_the_document_and_its_neighbours_only(world: World, recomputed: list[str]) -> None:
    world.doc("X", "x3", {"title": "x3", "status": "open"})
    world.rule("closed")
    api.rules_on_check(world.store)
    recomputed.clear()
    world.save("X", "x1", {"title": "x1", "status": "closed", "depends_on": "X:x2"})
    dirty = json.loads((cache_dir(world.store) / "rules" / "dirty.json").read_text(encoding="utf-8"))["dirty"]
    assert dirty == ["X:x1"]
    assert _codes(api.rules_on_check(world.store)) == [("error", "rules/closed", "X:x2"), ("error", "rules/closed", "X:x3")]
    assert sorted(recomputed) == ["closed@X:x1", "closed@X:x2"]


def test_without_the_cache_the_findings_are_the_same(world: World, recomputed: list[str]) -> None:
    world.rule("closed")
    first = _codes(api.rules_on_check(world.store))
    shutil.rmtree(cache_dir(world.store) / "rules")
    recomputed.clear()
    assert _codes(api.rules_on_check(world.store)) == first == _codes(api.rules_check(world.store))
    assert len(recomputed) == 2


def test_a_closure_over_a_cycle_terminates_and_names_the_open_document(world: World) -> None:
    for name, target in (("a", "b"), ("b", "c"), ("c", "a")):
        world.doc("X", name, {"title": name, "status": "closed", "depends_on": f"X:{target}"})
    api.rebuild_edges(world.store, world.py)
    world.save("X", "c", {"title": "c", "status": "open", "depends_on": "X:a"})
    world.rule("deps", where='title = "a"', condition='all(depends_on+: status = "closed")')
    [found] = api.rules_on_check(world.store)
    assert (found.code, found.subject) == ("rules/deps", "X:a") and found.what.endswith("(witness: X:c {\"status\":\"open\"})")
    world.save("X", "c", {"title": "c", "status": "closed", "depends_on": "X:a"})
    assert api.rules_on_check(world.store) == []


def test_edges_check_fails_on_a_condition_that_does_not_parse(world: World, capsys) -> None:
    _machine(world)
    assert api.check_edges(world.store).ok
    payload = {"title": "bad", "source_id": "State:done", "target_id": "State:open", "relation_type": "moves_to", "condition": 'status = = "x"'}
    world.doc("RelationDoc", "e-bad", payload)
    [error] = api.check_edges(world.store).errors
    assert "State:done -[moves_to]-> sldb://document/State:open: condition does not parse" in error
    envelope = world.envelope(capsys, "edges", "check", pythonpath=False)
    assert (envelope["ok"], envelope["exit"]) == (False, 1)

FILE:instruccion
Cold-bundle de la tarea task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_tags.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

