"""GO08 p4: the end-to-end example of the plan (docs/architecture/rules.md §10).

A temporary store with Task (`__contract__` = title, goal) and Review (`__doc_anchors__` =
subject, plus verdict); an `on_transition` RuleDoc on `model <= Task` with severity error and
condition `any(^subject: anchor_state = "intact" and verdict = "accepted")`; two states and a
RelationDoc transition between them without condition. (1) A Task without Review: the edge is
not in `edges_holding`, it is in `edges_blocked` with a finding naming the `any(...)` clause.
(2) An accepted Review pinned to the Task: the edge holds. (3) The Task's goal edited: the
anchor is `changed`, the edge is blocked again and the explanation shows it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main

MODULE = "sldb_go08_end_to_end_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Task(StructuredNLDoc):
    __contract__ = ["title", "goal"]
    __template__ = "---\\ngoal: ⸢rev•goal⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    goal: str = Field(default="", description="What the task must achieve.")


class Review(StructuredNLDoc):
    __doc_anchors__ = ["subject"]
    __template__ = "---\\nsubject: ⸢rev•subject⸥\\nverdict: ⸢rev•verdict⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    subject: str = Field(default="", description="The reviewed document.")
    verdict: str = Field(default="", description="accepted or rejected.")


class State(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''
CLAUSE = 'any(^subject: anchor_state = "intact" and verdict = "accepted")'
RULE = {"title": "reviewed", "subject": "model <= Task", "condition": CLAUSE, "severity": "error", "moment": "on_transition"}
TASK = {"title": "t", "goal": "ship it"}


@pytest.fixture
def store(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root, py = tmp_path / "desk", str(tmp_path)
    root.mkdir()
    store = api.init_store(root).store_path
    for ref in (f"{MODULE}:Task", f"{MODULE}:Review", f"{MODULE}:State", "sldb.models.rule_doc:RuleDoc"):
        api.add_model(store, ref, py)
    api.init_relations(store, py)

    def create(model: str, name: str, payload: dict) -> None:
        api.create_document(store, model, root / f"{name}.md", payload, name, py)

    for state in ("doing", "done"):
        create("State", state, {"title": state})
    create("RelationTypeDoc", "rt-moves", {"title": "moves", "name": "moves_to", "source_types": ["State"], "target_types": ["State"], "description": "A transition."})
    create("RelationDoc", "e-finish", {"title": "finish", "source_id": "State:doing", "target_id": "State:done", "relation_type": "moves_to"})
    create("RuleDoc", "reviewed", RULE)
    create("Task", "t", TASK)
    try:
        yield store, py, create
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _transition(store: Path, task: dict) -> tuple[list, list]:
    args = (store, "State:doing", task, "moves_to")
    return api.edges_holding(*args, document="Task:t"), api.edges_blocked(*args, document="Task:t")


def test_the_transition_follows_the_review_and_its_anchor(store, capsys) -> None:
    store, py, create = store
    holding, [blocked] = _transition(store, TASK)
    assert holding == [] and blocked.target == "sldb://document/State:done"
    [finding] = blocked.findings
    assert (finding.level, finding.code, finding.subject) == ("error", "rules/reviewed", "Task:t")
    assert finding.what.startswith(CLAUSE)

    review = {"title": "r", "subject": "doc:Task:t", "verdict": "accepted"}
    create("Review", "r", review)
    api.save_document_payload(store, "Review", "r", review, py)
    assert api.edge_node(store, "Review:r").payload["subject"].startswith("doc:Task:t@sha256:")
    [held], blocked_now = _transition(store, TASK)
    assert held.target == "sldb://document/State:done" and held.findings == [] and blocked_now == []

    edited = {**TASK, "goal": "ship it twice"}
    api.save_document_payload(store, "Task", "t", edited, py)
    holding, [blocked] = _transition(store, edited)
    assert holding == []
    [finding] = blocked.findings
    assert finding.what.startswith(CLAUSE) and '(witness: Review:r {"anchor_state":"changed"})' in finding.what
    assert main(["--envelope", "stores", "check", "--store", str(store), "--pythonpath", py, "--format", "json"]) == 0
    warnings = json.loads(capsys.readouterr().out)["warnings"]
    assert ("anchors/doc_changed", "Review:r") in [(w["code"], w["subject"]) for w in warnings]
