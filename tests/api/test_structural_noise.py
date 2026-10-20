"""Structural noise: a heading inside a field is a field the model is missing.

The document is not corrupt — it extracts and re-renders — but the section is
swallowed into a field value and its own identity is lost. The refusal is at
registration, and the way out is a child model declaring the sections `optrev`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from pydantic import Field

from sldb import StructuredNLDoc
from sldb.api import add_model, check_store, init_store, track_document_file
from sldb.api.documents.frontmatter_keys import (
    refuse_undeclared_frontmatter,
    undeclared_frontmatter_keys,
)
from sldb.api.stores.scan_structural_noise import scan_structural_noise
from sldb.core.exceptions import SLDBValidationError

MODULE = "sldb_noise_test_models"

# NoteDoc declares one heading; NoteWithSections inherits it and declares the two more
# that the noisy document carries, as optrev so plain notes still validate.
MODELS_SOURCE = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## Answer\\n\\n⸢rev•body⸥"
    title: str = Field(description="Note title.")
    body: str = Field(description="Note body.")


class NoteWithSections(NoteDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## Answer\\n\\n⸢rev•body⸥\\n\\n## Entidades\\n\\n⸢optrev•entidades⸥\\n\\n## Medicion 1\\n\\n⸢optrev•medicion_1⸥"
    entidades: str = Field(default="", description="Referenced atoms.")
    medicion_1: str = Field(default="", description="First verifiable criterion.")
'''

CLEAN = "# Alpha\n\n## Answer\n\nJust prose, no headings inside the body.\n"
NOISY = "# Alpha\n\n## Answer\n\nBody text\n\n## Entidades\n\n- one\n\n## Medicion 1\n\n- two\n"


@pytest.fixture
def noise_store(tmp_path: Path):
    """A store with NoteDoc and its child NoteWithSections registered."""
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS_SOURCE, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    init_store(root)
    store = root / ".sldb"
    for name in ("NoteDoc", "NoteWithSections"):
        add_model(store, f"{MODULE}:{name}", str(tmp_path))
    yield SimpleStore(root, store, str(tmp_path))
    sys.modules.pop(MODULE, None)


class SimpleStore:
    """Paths of a throwaway store, plus a way to drop a Markdown file into it."""

    def __init__(self, root: Path, store: Path, pythonpath: str) -> None:
        self.root, self.store, self.pythonpath = root, store, pythonpath

    def write(self, name: str, text: str) -> Path:
        """Write `text` to `root/<name>.md` without tracking it."""
        path = self.root / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        return path


def test_track_refuses_a_document_whose_headings_the_model_does_not_declare(noise_store):
    """The refusal is an error that names every offending heading, not a warning."""
    path = noise_store.write("noisy", NOISY)
    with pytest.raises(SLDBValidationError) as excinfo:
        track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath)
    message = str(excinfo.value)
    assert "ruido estructural en 'noisy'" in message
    assert "## Entidades" in message and "## Medicion 1" in message
    assert excinfo.value.details["undeclared"] == ["## Entidades", "## Medicion 1"]
    assert "herede de NoteDoc" in message


def test_the_refusal_leaves_the_document_untracked(noise_store):
    """Nothing enters the store: the refusal is a block, not a logged complaint."""
    path = noise_store.write("noisy", NOISY)
    with pytest.raises(SLDBValidationError):
        track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath)
    assert scan_structural_noise(noise_store.store, noise_store.root, noise_store.pythonpath) == []


def test_a_document_that_fits_its_model_still_tracks(noise_store):
    """The happy path is untouched: no headings beyond the template, no refusal."""
    path = noise_store.write("clean", CLEAN)
    tracked = track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath)
    assert (tracked.model, tracked.name) == ("NoteDoc", "clean")


def test_a_child_model_declaring_the_sections_optrev_accepts_the_document(noise_store):
    """The way out: inherit, declare the sections, and the same bytes are admitted."""
    path = noise_store.write("noisy", NOISY)
    tracked = track_document_file(noise_store.store, "NoteWithSections", path, pythonpath=noise_store.pythonpath)
    assert (tracked.model, tracked.name) == ("NoteWithSections", "noisy")


def test_the_noise_is_swallowed_into_a_field_value_under_the_parent(noise_store):
    """Why it matters: under the parent both sections end up as raw markdown inside `body`.

    That is the loss the refusal exists to stop: the document still round-trips, so
    nothing else in the system ever complains. Declaring the sections keeps `body` to
    the answer and gives each section a field of its own.
    """
    from sldb.api import resolve_model_ref
    from sldb.runtime.validation import extract_model_data

    parent = resolve_model_ref(f"{MODULE}:NoteDoc", noise_store.pythonpath)
    child = resolve_model_ref(f"{MODULE}:NoteWithSections", noise_store.pythonpath)
    assert "## Entidades" in extract_model_data(parent, NOISY)["body"]
    assert extract_model_data(child, NOISY)["body"] == "Body text"


def test_undeclared_frontmatter_key_is_refused():
    """A frontmatter key the model never declares was silently dropped; now refused.

    Symmetric with the heading refusal: `docs track` rejects a heading the model
    never declares, but a frontmatter key it never declares used to vanish on the
    first re-render. The same document, the same contract, the same refusal.
    """

    class CardDoc(StructuredNLDoc):
        __template__ = "---\nid: ⸢rev•id⸥\ntitle: ⸢rev•title⸥\n---\n\n# ⸢rev•title⸥"
        id: str = Field(description="Stable id.")
        title: str = Field(description="Card title.")

    clean = "---\nid: c1\ntitle: Card\n---\n\n# Card"
    assert undeclared_frontmatter_keys(CardDoc, clean) == []
    with_owner = clean.replace("---\nid:", "---\nowner: jp\nid:", 1)
    assert undeclared_frontmatter_keys(CardDoc, with_owner) == ["owner"]
    with pytest.raises(SLDBValidationError, match="owner"):
        refuse_undeclared_frontmatter(CardDoc, with_owner, "card")


def test_a_dict_placeholder_frontmatter_declares_every_key():
    """A frontmatter that is one `dict` placeholder carries any key through extraction and
    back on re-render, so no key is lost and none is refused (deskops' TaskDoc)."""

    class TaskDoc(StructuredNLDoc):
        __template__ = "---\n⸢rev,dict•frontmatter⸥\n---\n\n# ⸢rev•title⸥"
        title: str = Field(description="Task title.")
        frontmatter: dict | None = Field(default=None, description="Metadata.")

    assert undeclared_frontmatter_keys(TaskDoc, "---\npriority: p0\ndomain: x\n---\n\n# T") == []


def test_stores_check_reports_noise_already_tracked_without_blocking(noise_store):
    """`stores check` diagnoses what `docs track` would now refuse; force put it there."""
    path = noise_store.write("noisy", NOISY)
    track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath, force=True)
    report = check_store(noise_store.store, noise_store.root, noise_store.pythonpath)
    entry = next(item for item in report["structural_noise"] if item["document"] == "noisy")
    assert entry["model"] == "NoteDoc"
    assert entry["undeclared"] == ["## Entidades", "## Medicion 1"]


def test_the_cli_refusal_is_loud_and_exits_nonzero(noise_store, capsys):
    """Not a warning and not an empty dict: the CLI names the headings and fails.

    Guards the recurring failure mode of this codebase, where a document that does
    not fit its contract is skipped (`store/query.py::_load_one`) or reduced to a
    `logger.warning` plus `{}` (`cli/graph_ops/map_fields.py`).
    """
    from sldb.cli import main as cli_main

    path = noise_store.write("noisy", NOISY)
    with pytest.raises(SystemExit) as excinfo:
        cli_main(["docs", "track", str(path), "--model", "NoteDoc", "--store", str(noise_store.store), "--pythonpath", noise_store.pythonpath])
    assert excinfo.value.code != 0
    assert "## Entidades" in str(excinfo.value)


def test_stores_check_prints_every_noisy_heading_not_just_a_count(noise_store, capsys):
    """The diagnosis is actionable: each document, its model, and the headings."""
    from sldb.cli import main as cli_main

    path = noise_store.write("noisy", NOISY)
    track_document_file(noise_store.store, "NoteDoc", path, pythonpath=noise_store.pythonpath, force=True)
    capsys.readouterr()
    assert cli_main(["stores", "check", "--store", str(noise_store.store), "--pythonpath", noise_store.pythonpath]) == 0, "noise on a model with declared headings is an alert (policy default)"
    out = capsys.readouterr().out
    assert "alert: [store/structural-noise] NoteDoc:noisy" in out
    assert "## Entidades" in out and "## Medicion 1" in out
