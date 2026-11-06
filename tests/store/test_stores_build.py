"""`stores declare` / `stores build`: the derived store comes back from what the store declares."""
from __future__ import annotations

import shutil
import subprocess
import sys

import hashlib
import json

import pytest
import yaml

from sldb.api import Seed
from sldb.api import build_store as api_build_store
from sldb.api.stores.apply_declaration import undeclared
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.store_declaration import load_declaration, save_declaration
from sldb.cli import main as cli_main
from sldb.cli.commands.stores_build import build_store
from sldb.cli.commands.stores_build_check import check_build
from sldb.store.io import invalidate_index_cache

from .test_semantic_export import _build_tracked_store


@pytest.fixture(autouse=True)
def _forget_the_tmp_model_package():
    yield
    for name in [m for m in sys.modules if m == "tmpdocs" or m.startswith("tmpdocs.")]:
        del sys.modules[name]


def _declared(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    save_declaration(store, declare_store(store, root))
    return store, root


def test_the_declaration_names_what_is_tracked_and_nothing_else(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    assert [m["name"] for m in declaration.models] == ["TaskDoc"]
    assert declaration.include == [{"model": "TaskDoc", "paths": ["task.md"]}]
    assert undeclared(store, root, declaration) == []


def test_a_store_rebuilt_from_its_declaration_tracks_the_same(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    before = tracked_rows(store, root)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    invalidate_index_cache()
    report = build_store(store, root)
    assert report["models"] == ["TaskDoc"] and report["tracked"] == ["task.md"]
    assert tracked_rows(store, root) == before
    assert cli_main(["stores", "check", "--store", str(store), "--quiet"]) == 0


EMPTY_SCAFFOLD = {"created": [], "rewritten": [], "present": [], "conflicts": []}
REPORT_KEYS = ["links", "models", "predicates_changed", "tracked", "generated", "undeclared", "missing", "scaffold"]


def test_building_a_current_store_changes_nothing(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    report = build_store(store, root)
    assert report["links"] == report["models"] == report["tracked"] == report["undeclared"] == []
    assert report["predicates_changed"] is False


def test_the_build_report_is_the_golden_one_plus_an_empty_scaffold_section(tmp_path, capsys):
    """A declaration without folders or seeds builds as before; the report only gains `scaffold`."""
    store, root = _declared(tmp_path, capsys)
    report = build_store(store, root)
    assert list(report) == REPORT_KEYS
    assert report == {"links": [], "models": [], "predicates_changed": False, "tracked": [], "generated": [], "undeclared": [], "missing": [], "scaffold": EMPTY_SCAFFOLD}
    capsys.readouterr()
    assert cli_main(["stores", "build", "--store", str(store), "--format", "json"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert list(printed) == REPORT_KEYS and printed["scaffold"] == EMPTY_SCAFFOLD
    assert cli_main(["stores", "build", "--store", str(store)]) == 0
    assert capsys.readouterr().out.strip() == "built: links: 0, models: 0, tracked: 0, generated: 0, undeclared: 0, missing: 0"


def test_a_declaration_without_scaffold_keys_is_written_as_before(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    written = yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))
    assert "folders" not in written and "seeds" not in written
    declaration = load_declaration(store)
    declaration.folders, declaration.seeds = ["inbox"], [Seed(path="inbox/.keep", text="keep")]
    save_declaration(store, declaration)
    written = yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))
    assert written["folders"] == ["inbox"] and written["seeds"] == [{"path": "inbox/.keep", "mode": "if_missing", "text": "keep"}]


def test_build_applies_the_declaration_and_then_scaffolds(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    declaration.folders, declaration.seeds = ["inbox"], [Seed(path="inbox/.keep", text="keep"), Seed(path="NOTES.md", mode="managed", text="# Notes\n")]
    save_declaration(store, declaration)
    report = api_build_store(store)
    assert list(report) == REPORT_KEYS and report["tracked"] == []
    assert report["scaffold"] == {"created": ["inbox", "inbox/.keep", "NOTES.md"], "rewritten": [], "present": [], "conflicts": []}
    assert (root / "inbox" / ".keep").read_bytes() == b"keep"
    (root / "NOTES.md").write_text("edited", encoding="utf-8")
    assert build_store(store, root)["scaffold"] == {"created": [], "rewritten": ["NOTES.md"], "present": ["inbox", "inbox/.keep"], "conflicts": []}
    assert (root / "NOTES.md").read_text(encoding="utf-8") == "# Notes\n"


def test_build_without_apply_writes_nothing_and_says_what_is_pending(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    declaration.folders = ["inbox"]
    declaration.include[0]["paths"].append("gone.md")
    save_declaration(store, declaration)
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}
    report = api_build_store(store, apply=False)
    assert report == {"links": [], "models": [], "predicates_changed": False, "tracked": [], "generated": [], "undeclared": [], "missing": ["gone.md"], "scaffold": {"created": ["inbox"], "rewritten": [], "present": [], "conflicts": []}}
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()} == before


def test_build_runs_the_generators_the_caller_hands_in(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    seen = []
    report = api_build_store(store, generate=lambda s, r, d: seen.append((s, r)) or ["noop"])
    assert report["generated"] == ["noop"] and seen == [(store.resolve(), root.resolve())]


def test_a_tracked_document_no_rule_names_is_reported(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    declaration = load_declaration(store)
    declaration.include = []
    assert undeclared(store, root, declaration) == ["task.md"]


def test_the_check_rebuilds_a_scratch_copy_and_compares(tmp_path, capsys):
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    report = check_build(store, root, tmp_path / "scratch")
    assert report == {"ok": True, "integrity_exit": 0, "undeclared": [], "missing": [], "differences": [], "errors": [], "alerts": []}
    assert yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))["include"]


def test_build_finds_a_store_that_is_only_declared(tmp_path, capsys, monkeypatch):
    """A fresh clone has `.sldb/store.yaml` and no index: the usual discovery, which looks for
    the index, missed it and fell back to the global store."""
    store, root = _declared(tmp_path, capsys)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    invalidate_index_cache()
    monkeypatch.chdir(root)
    assert cli_main(["stores", "build"]) == 0
    assert cli_main(["stores", "check", "--store", str(store), "--quiet"]) == 0


def test_a_model_outside_the_project_is_declared_by_reference_only(tmp_path, capsys):
    """deskops and spec2viz register sldb's relation models from the installed package: their
    absolute path would pin the declaration to one checkout."""
    from sldb.api import add_model

    store, root = _build_tracked_store(tmp_path, capsys)
    add_model(store, "sldb.models.relation_doc:RelationDoc")
    models = {m["name"]: m for m in declare_store(store, root).models}
    assert models["RelationDoc"] == {"name": "RelationDoc", "model_ref": "sldb.models.relation_doc:RelationDoc"}
    assert models["TaskDoc"]["path"] == "tmpdocs/models.py"


def test_a_folder_with_one_tracked_file_is_listed_not_globbed(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)
    (root / "boards").mkdir()
    (root / "boards" / "board.md").write_text("# Board\n\n## Overview\n\nBody\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "boards" / "board.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    rules = [r for r in declare_store(store, root).include if "boards/board.md" in str(r)]
    assert rules == [{"model": "TaskDoc", "paths": ["boards/board.md"]}]


def test_untracking_a_document_takes_it_out_of_the_declaration(tmp_path, capsys):
    """deskops retire untracks a note; the declaration kept listing it, so a clean clone
    could not rebuild (CI run 39274588896)."""
    store, root = _declared(tmp_path, capsys)
    assert cli_main(["docs", "untrack", "task", "--store", str(store)]) == 0
    assert load_declaration(store).include == []


def test_tracking_a_document_no_rule_covers_adds_it_to_the_declaration(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    (root / "second.md").write_text("# Beta\n\n## Overview\n\nMore\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "second.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    assert load_declaration(store).include == [{"model": "TaskDoc", "paths": ["task.md", "second.md"]}]
    assert undeclared(store, root, load_declaration(store)) == []


def test_a_declared_file_that_is_gone_is_reported_not_raised(tmp_path, capsys):
    """The clean-clone failure: the declaration names a file git no longer has."""
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    declaration = load_declaration(store)
    declaration.include[0]["paths"].append("gone.md")
    save_declaration(store, declaration)
    (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    report = check_build(store, root, tmp_path / "scratch")
    assert report["ok"] is False and report["missing"] == ["gone.md"]
    assert report["integrity_exit"] == 0


def test_a_document_outside_the_project_does_not_break_the_declaration(tmp_path, capsys):
    """spec2viz synced a repo spec into a tmp store: create_document raised pathlib's raw
    ValueError from the declaration sync. A file outside the project cannot be declared."""
    from sldb.api import create_document

    (tmp_path / "project").mkdir()
    store, root = _declared(tmp_path / "project", capsys)
    outside = tmp_path / "elsewhere" / "far.md"
    create_document(store, "TaskDoc", outside, {"title": "Far", "body": "Away"}, pythonpath=str(root))
    assert load_declaration(store).include == [{"model": "TaskDoc", "paths": ["task.md"]}]


def test_the_check_reaches_a_link_that_climbs_more_than_one_level(tmp_path, capsys):
    """Governance links deskops through `../../../...`: a copy one level under the scratch
    resolved that link outside it (Permission denied on /tmp's parent, or a symlink left there)."""
    project = tmp_path / "a" / "b" / "project"
    project.mkdir(parents=True)
    store, root = _declared(project, capsys)
    owner = tmp_path / "owner"
    owner.mkdir()
    assert cli_main(["stores", "init", "--path", str(owner)]) == 0
    assert cli_main(["stores", "add", str(owner / ".sldb"), "--name", "owner", "--store", str(store)]) == 0
    save_declaration(store, declare_store(store, root))
    assert load_declaration(store).links[0]["path"] == "../../../owner/.sldb"
    (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    assert check_build(store, root, tmp_path / "scratch")["ok"]
    assert not (tmp_path.parent / "owner").exists()


def test_a_declared_store_that_was_not_built_fails_the_check(tmp_path, capsys):
    """`stores check` passed on it with 0 documents in 0 models (inbox 20261020-024137)."""
    store, root = _declared(tmp_path, capsys)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    invalidate_index_cache()
    capsys.readouterr()
    assert cli_main(["stores", "check", "--store", str(store)]) == 1
    assert "error: [store/unbuilt]" in capsys.readouterr().out


def test_a_declared_store_left_empty_by_a_failed_build_fails_the_check(tmp_path, capsys):
    """Governance's case: the build stopped on a broken link after writing an empty index."""
    from sldb.api.stores.store_skeleton import write_empty_store

    store, root = _declared(tmp_path, capsys)
    for derived in (store / "core", store.parent / ".sldb_cache"):
        shutil.rmtree(derived, ignore_errors=True)
    write_empty_store(store)
    invalidate_index_cache()
    capsys.readouterr()
    assert cli_main(["stores", "check", "--store", str(store)]) == 1
    assert "error: [store/unbuilt]" in capsys.readouterr().out


def test_declare_write_keeps_an_authored_glob_and_adds_only_what_is_missing(tmp_path, capsys):
    """`declare --write` turned `glob: notes/*.md` into the list of its matches (93 lines in
    deskops). The glob is the owner's intent: it stays, and a new link is added beside it."""
    store, root = _declared(tmp_path, capsys)
    (root / "notes").mkdir()
    for stem in ("a", "b"):
        (root / "notes" / f"{stem}.md").write_text(f"# {stem}\n\n## Overview\n\nBody\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(root / "notes" / f"{stem}.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    authored = load_declaration(store)
    authored.include = [{"model": "TaskDoc", "glob": "notes/*.md"}, {"model": "TaskDoc", "paths": ["task.md"]}]
    save_declaration(store, authored)
    owner = tmp_path / "owner"
    owner.mkdir()
    assert cli_main(["stores", "init", "--path", str(owner)]) == 0
    assert cli_main(["stores", "add", str(owner / ".sldb"), "--name", "owner", "--store", str(store)]) == 0
    (root / "late.md").write_text("# Late\n\n## Overview\n\nBody\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(root / "late.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    assert cli_main(["stores", "declare", "--store", str(store), "--write"]) == 0
    written = load_declaration(store)
    assert written.include[0] == {"model": "TaskDoc", "glob": "notes/*.md"}
    assert written.include == [{"model": "TaskDoc", "glob": "notes/*.md"}, {"model": "TaskDoc", "paths": ["task.md", "late.md"]}]
    assert [link["name"] for link in written.links] == ["owner"]
    assert undeclared(store, root, written) == []


def test_declare_write_is_stable_on_a_declaration_it_already_completed(tmp_path, capsys):
    store, root = _declared(tmp_path, capsys)
    before = (store / "store.yaml").read_text(encoding="utf-8")
    assert cli_main(["stores", "declare", "--store", str(store), "--write"]) == 0
    assert (store / "store.yaml").read_text(encoding="utf-8") == before


def _model_package(project, package, name="NoteDoc"):
    (project / package).mkdir()
    (project / package / "__init__.py").write_text("", encoding="utf-8")
    (project / package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        f"class {name}(StructuredNLDoc):\n"
        "    __template__ = '# ⸢rev•title⸥'\n"
        "    title: str = Field(description='Title')\n",
        encoding="utf-8",
    )
    return f"{package}.models:{name}"


def test_registering_a_model_declares_it_so_a_clean_clone_rebuilds(tmp_path, capsys):
    """`deskops desk update --apply` registered the new task types in the index but not in
    store.yaml: the CI rebuild said `Model 'TaskCodeDoc' not registered.` (sldb 8b60e889)."""
    project = tmp_path / "project"
    project.mkdir()
    store, root = _declared(project, capsys)
    ref = _model_package(root, "tmpnotes")
    try:
        assert cli_main(["models", "add", ref, "--store", str(store), "--pythonpath", str(root)]) == 0
        (root / "note.md").write_text("# A note\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(root / "note.md"), "--model", "NoteDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
        declared = {m["name"]: m for m in load_declaration(store).models}
        assert declared["NoteDoc"] == {"name": "NoteDoc", "model_ref": ref, "path": "tmpnotes/models.py"}
        (root / ".gitignore").write_text(".sldb_cache/\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        assert check_build(store, root, tmp_path / "scratch")["ok"] is True
    finally:
        for name in [m for m in sys.modules if m.startswith("tmpnotes")]:
            del sys.modules[name]


def test_inheriting_a_model_declares_it_with_its_origin(tmp_path, capsys):
    (tmp_path / "project").mkdir()
    store, root = _declared(tmp_path / "project", capsys)
    owner = tmp_path / "owner"
    owner.mkdir()
    ref = _model_package(owner, "ownernotes")
    try:
        assert cli_main(["stores", "init", "--path", str(owner)]) == 0
        assert cli_main(["models", "add", ref, "--store", str(owner / ".sldb"), "--pythonpath", str(owner)]) == 0
        assert cli_main(["stores", "add", str(owner / ".sldb"), "--name", "owner", "--store", str(store)]) == 0
        assert cli_main(["models", "inherit", "owner:NoteDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
        declared = {m["name"]: m for m in load_declaration(store).models}
        assert declared["NoteDoc"] == {"name": "NoteDoc", "model_ref": ref, "origin": "owner"}
        before = (store / "store.yaml").read_text(encoding="utf-8")
        assert cli_main(["models", "inherit", "owner:NoteDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
        assert (store / "store.yaml").read_text(encoding="utf-8") == before
    finally:
        for name in [m for m in sys.modules if m.startswith("ownernotes")]:
            del sys.modules[name]


def test_declare_keeps_a_glob_whose_generated_files_are_not_on_disk_yet(tmp_path, capsys):
    """In a clean clone the generator has not run: `declare --write` listed the 2561 symbol
    docs `knowledge/symbols/*.md` already covers. A glob covers by its pattern."""
    store, root = _declared(tmp_path, capsys)
    (root / "gen").mkdir()
    for stem in ("a", "b"):
        (root / "gen" / f"{stem}.md").write_text(f"# {stem}\n\n## Overview\n\nBody\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(root / "gen" / f"{stem}.md"), "--model", "TaskDoc", "--store", str(store), "--pythonpath", str(root)]) == 0
    authored = load_declaration(store)
    authored.include = [{"model": "TaskDoc", "glob": "gen/*.md"}, {"model": "TaskDoc", "paths": ["task.md"]}]
    save_declaration(store, authored)
    shutil.rmtree(root / "gen")
    assert cli_main(["stores", "declare", "--store", str(store), "--write"]) == 0
    assert load_declaration(store).include == [{"model": "TaskDoc", "glob": "gen/*.md"}, {"model": "TaskDoc", "paths": ["task.md"]}]
