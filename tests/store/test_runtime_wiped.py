"""Deleting `.sldb/runtime/` and rebuilding brings every derived index back (graph-ui report).

The user cache (outside the store) and the in-process dirty set both vouched for shards that
were gone, so a rebuild wrote only the edges: no sections, no semantic shards, and a graph
snapshot without `has_section` or `semantic_parent`.
"""

from __future__ import annotations

import shutil
import sys

from sldb import api

MODULE = "sldb_runtime_wiped_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## What\\n\\n⸢rev•what⸥\\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
'''


def test_a_rebuild_after_wiping_runtime_restores_sections_and_semantic_shards(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp = api.init_store(root).store_path
        api.add_model(sp, f"{MODULE}:Note", str(tmp_path))
        api.create_document(sp, "Note", root / "n.md", {"title": "n", "what": "W."}, "n", str(tmp_path))
        api.rebuild_edges(sp, str(tmp_path))
        kinds = lambda: sorted(p.name for p in (sp / "runtime").iterdir() if p.is_dir())  # noqa: E731
        before = kinds()
        shutil.rmtree(sp / "runtime")
        api.rebuild_edges(sp, str(tmp_path))
        derived = {"sections", "semantic", "edges"}  # the journal is a write log, not derived
        assert derived <= set(before) and derived <= set(kinds())
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)
