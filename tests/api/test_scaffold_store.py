"""`sldb.api.scaffold_store`: a store's declared folders and seeds, planned or written, idempotent."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from sldb.api import Seed, StoreDeclaration, add_model, doc_exists, init_store, scaffold_store, tracked_documents
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import load_declaration, save_declaration
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBStoreError

MODULE = "sldb_seed_test_models"
MODELS_SOURCE = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

## Body

⸢rev•body⸥
""".strip()
    title: str = Field(description="Title.")
    body: str = Field(description="Body.")
'''
PAYLOAD = {"title": "Welcome", "body": "Start here."}
RENDERED = b"# Welcome\n\n## Body\n\nStart here."


@pytest.fixture
def project(tmp_path: Path) -> tuple[Path, Path]:
    """A declared store with `NoteDoc` registered from a module inside the project, a template
    beside `store.yaml`, and the scaffold keys of the acceptance in its declaration."""
    root = tmp_path / "repo"
    root.mkdir()
    (root / f"{MODULE}.py").write_text(MODELS_SOURCE, encoding="utf-8")
    init_store(root)
    store = root / ".sldb"
    add_model(store, f"{MODULE}:NoteDoc", str(root))
    (store / "readme.tpl").write_bytes(b"managed template\n")
    declaration = declare_store(store, root)
    declaration.folders, declaration.seeds = FOLDERS, [Seed.model_validate(s) for s in SEEDS]
    save_declaration(store, declaration)
    yield store, root
    sys.modules.pop(MODULE, None)


FOLDERS = ["inbox", "notes/archive"]
SEEDS = [
    {"path": "inbox/.keep", "mode": "if_missing", "text": "keep"},
    {"path": "README.md", "mode": "managed", "file": "readme.tpl"},
    {"path": "notes/welcome.md", "mode": "if_missing", "document": {"model": "NoteDoc", "name": "welcome", "payload": PAYLOAD}, "track": True},
]
ALL = FOLDERS + [s["path"] for s in SEEDS]


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode() + path.read_bytes())
    return digest.hexdigest()


def test_without_apply_everything_missing_is_created_pending_and_nothing_is_written(project):
    store, root = project
    before = _tree_hash(root)
    report = scaffold_store(store)
    assert report.model_dump() == {"created": ALL, "rewritten": [], "present": [], "conflicts": [], "applied": False}
    assert _tree_hash(root) == before


def test_apply_creates_the_folders_and_seeds_and_tracks_the_document(project):
    store, root = project
    report = scaffold_store(store, apply=True)
    assert (report.created, report.applied) == (ALL, True)
    assert (root / "notes" / "archive").is_dir() and (root / "inbox" / ".keep").read_bytes() == b"keep"
    assert (root / "README.md").read_bytes() == b"managed template\n"
    assert (root / "notes" / "welcome.md").read_bytes() == RENDERED
    assert doc_exists(store, "welcome") and tracked_documents(store, ["welcome"])["welcome"].path == "notes/welcome.md"


def test_a_second_run_reports_everything_present(project):
    store, _root = project
    scaffold_store(store, apply=True)
    report = scaffold_store(store, apply=True)
    assert report.model_dump() == {"created": [], "rewritten": [], "present": ALL, "conflicts": [], "applied": True}


def test_an_edited_managed_file_is_reported_rewritten_and_restored(project):
    store, root = project
    scaffold_store(store, apply=True)
    (root / "README.md").write_bytes(b"edited\n")
    planned = scaffold_store(store)
    assert planned.rewritten == ["README.md"] and (root / "README.md").read_bytes() == b"edited\n"
    applied = scaffold_store(store, apply=True)
    assert applied.rewritten == ["README.md"] and (root / "README.md").read_bytes() == b"managed template\n"


def test_an_edited_if_missing_file_is_left_alone(project):
    store, root = project
    scaffold_store(store, apply=True)
    (root / "inbox" / ".keep").write_bytes(b"mine")
    report = scaffold_store(store, apply=True)
    assert "inbox/.keep" in report.present and (root / "inbox" / ".keep").read_bytes() == b"mine"


def test_a_package_template_is_resolved_with_importlib_resources(project, tmp_path, monkeypatch):
    store, root = project
    package = tmp_path / "seedpkg"
    (package / "templates").mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "templates" / "guide.md").write_bytes(b"# From the package\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    declaration = StoreDeclaration(seeds=[Seed(path="GUIDE.md", mode="managed", file="pkg:seedpkg/templates/guide.md")])
    try:
        report = scaffold_store(store, declaration=declaration, apply=True)
    finally:
        sys.modules.pop("seedpkg", None)
    assert report.created == ["GUIDE.md"] and (root / "GUIDE.md").read_bytes() == b"# From the package\n"


def test_the_same_declaration_in_process_gives_the_same_result_and_leaves_store_yaml_alone(project):
    store, root = project
    declaration = StoreDeclaration(folders=FOLDERS, seeds=[Seed.model_validate(s) for s in SEEDS])
    authored = load_declaration(store)
    authored.folders, authored.seeds = [], []
    authored.include = [{"model": "NoteDoc", "glob": "notes/*.md"}]
    save_declaration(store, authored)
    before = hashlib.sha256((store / "store.yaml").read_bytes()).hexdigest()
    report = scaffold_store(store, declaration=declaration, apply=True, template_root=store)
    assert report.created == ALL and doc_exists(store, "welcome")
    assert hashlib.sha256((store / "store.yaml").read_bytes()).hexdigest() == before
    assert scaffold_store(store, declaration=declaration, apply=True, template_root=store).present == ALL


def test_a_relative_file_source_is_read_from_template_root(project, tmp_path):
    store, root = project
    (tmp_path / "tpl").mkdir()
    (tmp_path / "tpl" / "a.txt").write_bytes(b"A")
    declaration = StoreDeclaration(seeds=[Seed(path="a.txt", file="a.txt")])
    with pytest.raises(SLDBStoreError, match="not found"):
        scaffold_store(store, declaration=declaration)
    assert scaffold_store(store, declaration=declaration, apply=True, template_root=tmp_path / "tpl").created == ["a.txt"]


def test_an_unknown_seed_key_fails_at_load_naming_it(project):
    store, _root = project
    text = yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))
    text["seeds"][0]["modo"] = "managed"
    (store / "store.yaml").write_text(yaml.safe_dump(text), encoding="utf-8")
    with pytest.raises(ValidationError, match="modo"):
        load_declaration(store)


@pytest.mark.parametrize("seed, message", [
    ({"path": "x", "text": "a", "file": "b"}, "exactly one source"),
    ({"path": "x"}, "exactly one source"),
    ({"path": "x", "text": "a", "track": True}, "document source only"),
    ({"path": "x", "document": {"model": "NoteDoc", "name": "n"}}, "exactly the keys"),
    ({"path": "x", "text": "a", "mode": "always"}, "mode"),
])
def test_a_seed_breaking_its_invariants_is_rejected(seed, message):
    with pytest.raises(ValidationError, match=message):
        Seed.model_validate(seed)


def test_track_defaults_to_true_for_a_document_and_false_otherwise():
    assert Seed(path="d.md", document={"model": "M", "name": "d", "payload": {}}).tracked is True
    assert Seed(path="d.md", document={"model": "M", "name": "d", "payload": {}}, track=False).tracked is False
    assert Seed(path="t.txt", text="t").tracked is False


def test_a_folder_held_by_a_file_and_a_seed_held_by_a_folder_are_conflicts(project):
    store, root = project
    (root / "inbox").write_bytes(b"not a folder")
    (root / "README.md").mkdir()
    report = scaffold_store(store, apply=True)
    assert report.conflicts == ["inbox", "inbox/.keep", "README.md"] and (root / "inbox").read_bytes() == b"not a folder"
    assert report.created == ["notes/archive", "notes/welcome.md"] and (root / "notes" / "welcome.md").is_file()


def test_a_path_outside_the_project_is_refused(project):
    store, _root = project
    for raw in ("../out", "/tmp/out", "."):
        with pytest.raises(SLDBStoreError, match="project root"):
            scaffold_store(store, declaration=StoreDeclaration(folders=[raw]))


def test_a_failure_halfway_rolls_the_earlier_seeds_back(project):
    store, root = project
    taken = {"model": "NoteDoc", "name": "welcome", "payload": PAYLOAD}
    declaration = StoreDeclaration(seeds=[Seed(path="first.txt", text="1"), Seed(path="a.md", document=taken), Seed(path="b.md", document=taken)])
    with pytest.raises(SLDBStoreError, match="already tracked"):
        scaffold_store(store, declaration=declaration, apply=True)
    assert not (root / "first.txt").exists() and not (root / "a.md").exists() and not doc_exists(store, "welcome")


def test_the_cli_reports_plans_and_applies_with_an_envelope(project, capsys):
    store, root = project
    assert cli_main(["stores", "scaffold", "--store", str(store), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["created"] == ALL and not (root / "inbox").exists()
    assert cli_main(["--envelope", "stores", "scaffold", "--store", str(store), "--apply", "--format", "json"]) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["ok"] and envelope["command"] == "stores scaffold" and envelope["data"]["applied"] is True
    assert cli_main(["stores", "scaffold", "--store", str(store), "--apply"]) == 0
    assert capsys.readouterr().out.startswith("scaffolded: created: 0, rewritten: 0, present: 5, conflicts: 0")


def test_the_cli_exits_one_on_a_conflict(project, capsys):
    store, root = project
    (root / "inbox").write_bytes(b"file")
    assert cli_main(["stores", "scaffold", "--store", str(store)]) == 1
    assert "conflicts: inbox" in capsys.readouterr().out
