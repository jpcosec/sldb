"""G4: every write path validates the payload against the model.

A model whose `model_validator` rejects one value is given that value through each path:
`sldb fields update`, `sldb docs update`, `POST /save`, `sldb.api.apply_batch` and
`sldb.api.transaction`. Each one refuses it, and the file, the index entry and the derived
indexes stay exactly as they were.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

import sldb.api as api
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBValidationError
from tests.test_serve import _request_json, _serve, _stop

MODULE = "sldb_write_paths_test_models"
MODELS = '''from pydantic import Field, model_validator
from sldb import StructuredNLDoc


class GuardedDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")

    @model_validator(mode="after")
    def _refuse_forbidden(self):
        if self.title == "FORBIDDEN":
            raise ValueError("the model rejects the title FORBIDDEN")
        return self
'''
REJECTED = {"title": "FORBIDDEN"}
INITIAL = {"title": "Allowed"}


class Guarded:
    """A store with GuardedDoc registered and `g1` tracked, plus what must not move."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "repo", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        api.add_model(self.store, f"{MODULE}:GuardedDoc", self.py)
        api.create_document(self.store, "GuardedDoc", "g1.md", INITIAL, "g1", self.py)
        self.before = self.state()

    def state(self) -> dict[str, str]:
        """sha256 of every file of the project: the Markdown, `.sldb/` entries, `.sldb_cache/` shards."""
        return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(self.root.rglob("*")) if p.is_file() and "locks" not in p.parts}

    def unchanged(self) -> bool:
        return self.state() == self.before and api.check_store(self.store, self.root, self.py)["ok"]

    def cli(self, *args: str) -> list[str]:
        return [*args, "--store", str(self.store), "--pythonpath", self.py]


@pytest.fixture
def guarded(tmp_path: Path) -> Guarded:
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.modules.pop(MODULE, None)
    yield Guarded(tmp_path)
    sys.modules.pop(MODULE, None)


def test_fields_update_rejects_what_the_model_rejects(guarded: Guarded) -> None:
    with pytest.raises(SystemExit, match="rejects the title"):
        cli_main(guarded.cli("fields", "update", "docs/g1/title", "FORBIDDEN"))
    assert guarded.unchanged()


def test_docs_update_rejects_what_the_model_rejects(guarded: Guarded) -> None:
    with pytest.raises(SystemExit, match="rejects the title"):
        cli_main(guarded.cli("docs", "update", "g1", '{"title": "FORBIDDEN"}'))
    assert guarded.unchanged()


def test_save_route_rejects_what_the_model_rejects_with_422(guarded: Guarded) -> None:
    server, thread, base_url = _serve(guarded.store, guarded.py)
    try:
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "g1", "action": "update", "model": "GuardedDoc", "payload": REJECTED, "expected": INITIAL},
        ]}, expected_error=422)
    finally:
        _stop(server, thread)
    assert status == 422 and body["ok"] is False and "rejects the title" in body["error"]
    assert guarded.unchanged()


def test_apply_batch_rejects_what_the_model_rejects(guarded: Guarded) -> None:
    with pytest.raises(SLDBValidationError, match="rejects the title"):
        api.apply_batch(guarded.store, [{"id": "g1", "action": "update", "payload": REJECTED, "expected": INITIAL}], guarded.py)
    assert guarded.unchanged()


def test_transaction_rejects_what_the_model_rejects_and_rolls_back(guarded: Guarded) -> None:
    with pytest.raises((SLDBValidationError, ValidationError), match="rejects the title"):
        with api.transaction(guarded.store, guarded.py) as tx:
            tx.update("g1", REJECTED)
    assert guarded.unchanged()
