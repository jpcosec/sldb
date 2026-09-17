"""Fixtures for the `sldb.api` library tests: a store with one registered model and one document."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb.api import add_model, init_store, resolve_model_ref, track_document_file
from sldb.runtime.validation import render_model_markdown

MODULE = "sldb_api_test_models"

MODELS_SOURCE = '''from pydantic import Field
from typing import Literal
from sldb import StructuredNLDoc


class TicketDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

Status: ⸢rev•status⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()
    title: str = Field(description="Ticket title.")
    status: Literal["open", "closed"] = Field(description="Ticket state.")
    tags: list[str] = Field(description="Free tags.")
'''

PAYLOAD = {"title": "Broken login", "status": "open", "tags": ["auth"]}


class ApiStore:
    """A throwaway store: `root/.sldb`, models importable from `pythonpath`."""

    def __init__(self, root: Path, pythonpath: str) -> None:
        self.root, self.store, self.pythonpath = root, root / ".sldb", pythonpath

    def write_document(self, name: str, payload: dict) -> Path:
        """Render a TicketDoc payload to `root/<name>.md` without tracking it."""
        model_type = resolve_model_ref(f"{MODULE}:TicketDoc", self.pythonpath)
        path = self.root / f"{name}.md"
        path.write_text(render_model_markdown(model_type, payload) + "\n", encoding="utf-8")
        return path


@pytest.fixture
def api_store(tmp_path: Path) -> ApiStore:
    """A store with TicketDoc registered and the document `login` tracked."""
    for name in [MODULE, f"{MODULE}__draft__"]:
        sys.modules.pop(name, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS_SOURCE, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    init_store(root)
    store = ApiStore(root, str(tmp_path))
    add_model(store.store, f"{MODULE}:TicketDoc", store.pythonpath)
    track_document_file(store.store, "TicketDoc", store.write_document("login", PAYLOAD), "login", store.pythonpath)
    yield store
    sys.modules.pop(MODULE, None)
