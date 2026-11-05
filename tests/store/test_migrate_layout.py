"""`sldb stores migrate-layout`: a store from before 2026-11-04 moves its cache out of `.sldb/`.

The old layout kept the cache at `.sldb/runtime/` (edges, sections, semantic, graphs, locks,
and the journal) and ignored `.sldb/core/` and `.sldb/runtime/`. The migration moves the
content to `.sldb_cache/`, deletes the journal without archiving it, removes `.sldb/runtime/`
and rewrites the root `.gitignore`, keeping every line it does not own.
"""

from __future__ import annotations

import shutil
import subprocess
import sys

import pytest

from sldb import api
from sldb.api.stores.migrate_layout import migrate_layout
from sldb.cli import main
from sldb.store.io import invalidate_index_cache
from sldb.store.layout import cache_dir, runtime_dir

MODULE = "sldb_migrate_layout_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## What\\n\\n⸢rev•what⸥\\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
'''
OLD_GITIGNORE = """.venv/

.sldb/runtime/
.sldb/.config/
# Derived from .sldb/store.yaml: `sldb stores build` regenerates them.
/.sldb/core
knowledge/symbols/
.sldb_custom/runtime/

.DS_Store
"""
NEW_GITIGNORE = """.venv/

.sldb_cache/
.sldb/.config/
# Derived from .sldb/store.yaml: `sldb stores build` regenerates them.
knowledge/symbols/
.sldb_custom/runtime/

.DS_Store
"""


@pytest.fixture
def old_store(tmp_path, monkeypatch):
    """A built store rewritten into the old layout: cache under `.sldb/runtime/`, a journal in
    it, and the root `.gitignore` of a declared store from October 2026."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root = tmp_path / "world"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:Note", str(tmp_path))
    api.create_document(sp, "Note", root / "n.md", {"title": "n", "what": "W."}, "n", str(tmp_path))
    api.rebuild_edges(sp, str(tmp_path))
    shutil.move(str(cache_dir(sp)), str(sp / "runtime"))
    (sp / "runtime" / "journal").mkdir(exist_ok=True)
    (sp / "runtime" / "journal" / "0000000000.yaml").write_text("operation: create_document\n", encoding="utf-8")
    (sp / "runtime" / "locks" / "journal.lock").touch()
    (root / ".gitignore").write_text(OLD_GITIGNORE, encoding="utf-8")
    invalidate_index_cache()
    try:
        yield sp, root
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _dirs(path) -> set[str]:
    return {p.name for p in path.iterdir() if p.is_dir()}


def test_the_cache_moves_out_of_the_store_and_the_journal_goes(old_store, capsys):
    sp, root = old_store
    before = {p.name for p in (sp / "runtime").iterdir()} - {"journal"}
    assert main(["stores", "migrate-layout", "--store", str(sp)]) == 0
    out = capsys.readouterr().out
    assert not (sp / "runtime").exists()
    cache = root / ".sldb_cache"
    assert cache == runtime_dir(sp) and {p.name for p in cache.iterdir()} == before
    assert {"edges", "sections", "semantic"} <= _dirs(cache) and not (cache / "journal").exists()
    assert not (cache / "locks" / "journal.lock").exists()
    assert "journal removed" in out and "runtime removed" in out
    assert sorted(p.name for p in sp.iterdir()) == ["core"]  # init writes no declaration; a declared store keeps store.yaml too


def test_the_gitignore_loses_only_the_two_old_lines(old_store):
    sp, root = old_store
    report = migrate_layout(sp)
    assert (root / ".gitignore").read_text(encoding="utf-8") == NEW_GITIGNORE
    assert report["gitignore"] == {"path": str(root / ".gitignore"), "removed": [".sldb/runtime/", "/.sldb/core"], "added": True}


def test_the_migrated_store_checks_clean_and_rebuilds(old_store, capsys):
    sp, root = old_store
    assert main(["stores", "migrate-layout", "--store", str(sp)]) == 0
    capsys.readouterr()
    assert main(["stores", "check", "--store", str(sp), "--pythonpath", str(sp.parent.parent), "--quiet"]) == 0
    assert "alert:" not in capsys.readouterr().out
    shutil.rmtree(root / ".sldb_cache")
    api.rebuild_edges(sp, str(sp.parent.parent))
    assert {"edges", "sections", "semantic"} <= _dirs(root / ".sldb_cache")


def test_a_cache_with_content_is_refused_unless_forced(old_store, capsys):
    sp, root = old_store
    (root / ".sldb_cache" / "edges").mkdir(parents=True)
    (root / ".sldb_cache" / "stale.txt").write_text("old", encoding="utf-8")
    with pytest.raises(SystemExit) as refused:
        main(["stores", "migrate-layout", "--store", str(sp)])
    assert "--force" in str(refused.value)
    assert (sp / "runtime").is_dir() and (root / ".sldb_cache" / "stale.txt").exists()
    assert main(["stores", "migrate-layout", "--store", str(sp), "--force"]) == 0
    assert not (root / ".sldb_cache" / "stale.txt").exists() and (root / ".sldb_cache" / "edges").iterdir()
    assert not (sp / "runtime").exists()


def test_an_empty_cache_directory_is_used_as_is(old_store):
    sp, root = old_store
    (root / ".sldb_cache").mkdir()
    migrate_layout(sp)
    assert {"edges", "sections", "semantic"} <= _dirs(root / ".sldb_cache")


def test_running_it_twice_changes_nothing_more(old_store, capsys):
    sp, root = old_store
    assert main(["stores", "migrate-layout", "--store", str(sp)]) == 0
    capsys.readouterr()
    assert main(["stores", "migrate-layout", "--store", str(sp)]) == 0
    assert "nothing to move" in capsys.readouterr().out
    assert (root / ".gitignore").read_text(encoding="utf-8") == NEW_GITIGNORE


def test_the_store_may_be_named_by_its_project(old_store):
    sp, root = old_store
    assert migrate_layout(root)["store"] == str(sp)
    assert not (sp / "runtime").exists() and (root / ".sldb_cache" / "edges").is_dir()


def test_a_gitignore_that_never_existed_is_created(old_store):
    sp, root = old_store
    (root / ".gitignore").unlink()
    assert migrate_layout(sp)["gitignore"] == {"path": str(root / ".gitignore"), "removed": [], "added": True}
    assert (root / ".gitignore").read_text(encoding="utf-8") == ".sldb_cache/\n"
