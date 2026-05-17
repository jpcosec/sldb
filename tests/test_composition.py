from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from desk.models import BoardDoc, RitualDoc, StepDoc, TaskDoc
from sldb.runtime.validation import render_model_markdown


def test_board_doc_renders_composed_task_summaries(tmp_path: Path):
    task_path = tmp_path / "task-a.md"
    task_path.write_text(
        render_model_markdown(
            TaskDoc,
            {
                "title": "Improve model editing",
                "id": "task-a",
                "status": "active",
                "goal": "Support safer contract editing from the CLI.",
                "scope": "CLI model workflow only.",
                "references": [],
                "depends_on": [],
                "pills": [],
                "files": ["src/sldb/cli/commands/models.py"],
                "implementation_path": "Add draft-first mutations and validate before promotion.",
                "validation": ["targeted pytest"],
                "done_when": "The model edit workflow is safe.",
                "tags": ["system:sldb"],
            },
        ),
        encoding="utf-8",
    )

    rendered = render_model_markdown(
        BoardDoc,
        {
            "title": "Desk Board",
            "id": "board-001",
            "scope": "desk",
            "purpose": "Route active execution.",
            "tasks": [str(task_path)],
            "pills": ["desk/contexts/pill-001-task-closure-commit.md"],
            "rituals": ["desk/rituals/execution.md"],
            "notes": "No additional notes.",
            "tags": ["system:sldb"],
        },
    )

    assert "## Task Details" in rendered
    assert (
        "- Improve model editing [active] - Support safer contract editing from the CLI."
        in rendered
    )
    assert "desk/contexts/pill-001-task-closure-commit.md" in rendered


def test_ritual_doc_renders_composed_step_details(tmp_path: Path):
    step_path = tmp_path / "step-a.md"
    step_path.write_text(
        render_model_markdown(
            StepDoc,
            {
                "title": "Validate draft",
                "id": "step-a",
                "action": "Run model validation against tracked docs.",
                "outcome": "A promotable contract draft.",
                "tags": ["topic:validation"],
            },
        ),
        encoding="utf-8",
    )

    rendered = render_model_markdown(
        RitualDoc,
        {
            "title": "Promotion ritual",
            "id": "ritual-promotion",
            "purpose": "Promote safe drafts only.",
            "trigger": "A model draft is ready.",
            "preconditions": ["A draft exists."],
            "steps": [str(step_path)],
            "validation": ["Tracked docs still pass."],
            "failure_modes": ["Promoting an invalid draft."],
            "completion": "The active model has been updated safely.",
            "tags": ["system:sldb"],
        },
    )

    assert "## Step Details" in rendered
    assert (
        "1. Validate draft: Run model validation against tracked docs. -> A promotable contract draft."
        in rendered
    )
