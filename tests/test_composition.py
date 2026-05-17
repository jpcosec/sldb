from __future__ import annotations

import importlib
from pathlib import Path
import sys

from pydantic import Field

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sldb import StructuredNLDoc
from sldb.runtime.validation import render_model_markdown


class ComposedBoardDoc(StructuredNLDoc):
    __compositions__ = {
        "task_summaries": {
            "source_field": "tasks",
            "model": "composition_models:ComposedTaskDoc",
            "template": "- {title} [{status}] - {goal}",
        }
    }
    __template__ = """
# ⸢rev•title⸥

## Tasks

- ⸢rev,list•tasks⸥

## Task Details

⸢render•task_summaries⸥
""".strip()

    title: str = Field(description="Board title.")
    tasks: list[str] = Field(default_factory=list, description="Task refs.")


class ComposedRitualDoc(StructuredNLDoc):
    __compositions__ = {
        "step_details": {
            "source_field": "steps",
            "model": "composition_models:ComposedStepDoc",
            "template": "1. {title}: {action} -> {outcome}",
        }
    }
    __template__ = """
# ⸢rev•title⸥

## Steps

1. ⸢rev,list•steps⸥

## Step Details

⸢render•step_details⸥
""".strip()

    title: str = Field(description="Ritual title.")
    steps: list[str] = Field(default_factory=list, description="Step refs.")


def _load_composition_models(tmp_path: Path):
    module_path = tmp_path / "composition_models.py"
    module_path.write_text(
        """from pydantic import Field\nfrom sldb import StructuredNLDoc\n\n\nclass ComposedTaskDoc(StructuredNLDoc):\n    __template__ = \"# ⸢rev•title⸥\\n\\nStatus: ⸢rev•status⸥\\n\\n## Goal\\n\\n⸢rev•goal⸥\"\n    title: str = Field(description=\"Task title.\")\n    status: str = Field(description=\"Task status.\")\n    goal: str = Field(description=\"Task goal.\")\n\n\nclass ComposedStepDoc(StructuredNLDoc):\n    __template__ = \"# ⸢rev•title⸥\\n\\n## Action\\n\\n⸢rev•action⸥\\n\\n## Outcome\\n\\n⸢rev•outcome⸥\"\n    title: str = Field(description=\"Step title.\")\n    action: str = Field(description=\"Step action.\")\n    outcome: str = Field(description=\"Step outcome.\")\n""",
        encoding="utf-8",
    )
    if str(tmp_path) not in sys.path:
        sys.path.insert(0, str(tmp_path))
    return importlib.import_module("composition_models")


def test_board_doc_renders_composed_task_summaries(tmp_path: Path):
    models = _load_composition_models(tmp_path)
    task_path = tmp_path / "task-a.md"
    task_path.write_text(
        render_model_markdown(
            models.ComposedTaskDoc,
            {
                "title": "Improve model editing",
                "status": "active",
                "goal": "Support safer contract editing from the CLI.",
            },
        ),
        encoding="utf-8",
    )

    rendered = render_model_markdown(
        ComposedBoardDoc,
        {
            "title": "Composition Board",
            "tasks": [str(task_path)],
        },
    )

    assert "## Task Details" in rendered
    assert (
        "- Improve model editing [active] - Support safer contract editing from the CLI."
        in rendered
    )


def test_ritual_doc_renders_composed_step_details(tmp_path: Path):
    models = _load_composition_models(tmp_path)
    step_path = tmp_path / "step-a.md"
    step_path.write_text(
        render_model_markdown(
            models.ComposedStepDoc,
            {
                "title": "Validate draft",
                "action": "Run model validation against tracked docs.",
                "outcome": "A promotable contract draft.",
            },
        ),
        encoding="utf-8",
    )

    rendered = render_model_markdown(
        ComposedRitualDoc,
        {
            "title": "Composition Ritual",
            "steps": [str(step_path)],
        },
    )

    assert "## Step Details" in rendered
    assert (
        "1. Validate draft: Run model validation against tracked docs. -> A promotable contract draft."
        in rendered
    )
