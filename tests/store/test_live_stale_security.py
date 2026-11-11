"""SEGURIDAD (inbox 9c9dac6b): reading the edge index opens no file outside the project root,
follows no symlink, and does not read a file that has not changed since its shard was built.

Each read runs in a fresh process with an audit hook on `open`, as the coordinator's
reproduction did: the per-process hash cache of `live_stale` cannot help there, so what the
hook sees is what any new reader (a server starting, graph_ui, a CLI) would open.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from sldb import api
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.store_findings import diagnosis_findings
from sldb.store import built_cache
from sldb.store.diagnostics import diagnose_store
from sldb.store.edge_index.cache_keys import edge_cache_key
from sldb.store.io import load_models_index, load_store_index
from sldb.store.edge_index.compose import invalidate_composed_edge_indexes
from sldb.store.io.shards import invalidate_shard_cache
from sldb.store.layout import edges_shard_path
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_live_stale_security_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Memo(StructuredNLDoc):
    __references__ = ["title"]
    __template__ = """---
status: ⸢rev•status⸥
---

# ⸢rev•title⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
'''

_READER = r"""
import json, sys
store, roots = sys.argv[1], sys.argv[2:]
opened = []
def hook(event, args):
    if event == "open" and isinstance(args[0], (str, bytes)):
        opened.append(args[0] if isinstance(args[0], str) else args[0].decode())
from sldb.api.edges.edge_reading import load_edge_index
sys.addaudithook(hook)
index = load_edge_index(store, include_linked=False)
print(json.dumps({"opened": opened, "stale": index.stale}))
"""

_SRC = Path(__file__).resolve().parents[2] / "src"


@pytest.fixture
def world(tmp_path):
    py = str(tmp_path)
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_runtime_cache()
    sys.path.insert(0, py)
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp = api.init_store(root).store_path
        api.add_model(sp, f"{MODULE}:Memo", py)
        api.create_document(sp, "Memo", root / "a.md", {"title": "a", "status": "open"}, "a", py)
        api.create_document(sp, "Memo", root / "b.md", {"title": "b", "status": "open"}, "b", py)
        yield tmp_path, root, sp, py
    finally:
        sys.path.remove(py)
        sys.modules.pop(MODULE, None)


def _fresh_read(tmp_path: Path, sp: Path) -> dict:
    """`load_edge_index` in a new process: every `.md` it opens, and its `stale`."""
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(_SRC), str(tmp_path)])}
    done = subprocess.run([sys.executable, "-c", _READER, str(sp)], capture_output=True, text=True, env=env, cwd=tmp_path, check=True)
    result = json.loads(done.stdout.strip().splitlines()[-1])
    return {"md": [p for p in result["opened"] if p.endswith(".md")], "stale": result["stale"]}


def _findings(sp: Path, root: Path, py: str) -> dict[str, str]:
    diagnosis = diagnose_store(sp, resolve_model_ref, root, pythonpath=py)
    return {f.subject: (f.code, f.level) for f in diagnosis_findings(diagnosis) if f.subject.startswith("Memo:")}


def _secret(tmp_path: Path) -> Path:
    outside = tmp_path / "outside"
    outside.mkdir()
    secret = outside / "secret.md"
    secret.write_text("# not part of the project\n", encoding="utf-8")
    return secret


def test_a_store_just_built_opens_no_document_in_a_new_process(world):
    tmp_path, _, sp, _ = world
    read = _fresh_read(tmp_path, sp)
    assert read == {"md": [], "stale": []}


def test_a_tracked_symlink_out_of_the_root_is_not_opened_is_stale_and_is_named(world):
    tmp_path, root, sp, py = world
    secret = _secret(tmp_path)
    (root / "b.md").unlink()
    (root / "b.md").symlink_to(secret)

    read = _fresh_read(tmp_path, sp)

    assert not [p for p in read["md"] if Path(p).resolve() == secret.resolve() or p.endswith("b.md")]
    assert read["stale"] == ["Memo:b"]
    assert _findings(sp, root, py) == {"Memo:b": ("store/path-outside-root", "alert")}


def test_a_directory_on_the_way_that_escapes_the_root_is_not_followed(world):
    tmp_path, root, sp, py = world
    (root / "sub").mkdir()
    api.create_document(sp, "Memo", root / "sub" / "c.md", {"title": "c", "status": "open"}, "c", py)
    outside = tmp_path / "outside-sub"
    (root / "sub").rename(outside)
    (root / "sub").symlink_to(outside, target_is_directory=True)

    read = _fresh_read(tmp_path, sp)

    assert read == {"md": [], "stale": ["Memo:c"]}
    assert _findings(sp, root, py) == {"Memo:c": ("store/path-outside-root", "alert")}


def test_a_dangling_symlink_out_of_the_root_is_named_not_missing(world):
    tmp_path, root, sp, py = world
    (root / "b.md").unlink()
    (root / "b.md").symlink_to(tmp_path / "nowhere.md")
    assert _fresh_read(tmp_path, sp) == {"md": [], "stale": ["Memo:b"]}
    assert _findings(sp, root, py) == {"Memo:b": ("store/path-outside-root", "alert")}


def test_a_tracked_symlink_inside_the_root_is_not_followed_either(world):
    tmp_path, root, sp, py = world
    real = root / "real-b.md"
    (root / "b.md").rename(real)
    (root / "b.md").symlink_to(real)

    read = _fresh_read(tmp_path, sp)

    assert read == {"md": [], "stale": ["Memo:b"]}
    assert _findings(sp, root, py) == {"Memo:b": ("store/symlink-not-read", "alert")}


def test_an_edited_file_is_read_and_stale_and_only_that_one(world):
    tmp_path, root, sp, _ = world
    path = root / "a.md"
    path.write_text(path.read_text(encoding="utf-8").replace("status: open", "status: closed"), encoding="utf-8")

    read = _fresh_read(tmp_path, sp)

    assert [Path(p).name for p in read["md"]] == ["a.md"]
    assert read["stale"] == ["Memo:a"]


def test_a_touched_file_is_read_found_unchanged_and_not_stale(world):
    tmp_path, root, sp, _ = world
    path = root / "a.md"
    st = path.stat()
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))

    read = _fresh_read(tmp_path, sp)

    assert [Path(p).name for p in read["md"]] == ["a.md"] and read["stale"] == []


def test_a_shard_without_source_stat_is_hashed_as_before_and_filled_by_the_next_build(world):
    tmp_path, root, sp, py = world
    shard_path = edges_shard_path(sp, "Memo", "a")
    shard = yaml.safe_load(shard_path.read_text(encoding="utf-8"))
    assert shard["source_stat"] == [(root / "a.md").lstat().st_mtime_ns, (root / "a.md").lstat().st_size]
    shard.pop("source_stat")
    shard_path.write_text(yaml.safe_dump(shard, sort_keys=False, allow_unicode=True), encoding="utf-8")
    _as_walked_before_source_stat(sp, root)
    invalidate_composed_edge_indexes()
    invalidate_shard_cache()

    read = _fresh_read(tmp_path, sp)
    assert [Path(p).name for p in read["md"]] == ["a.md"] and read["stale"] == []

    api.rebuild_edges(sp, py)
    assert yaml.safe_load(shard_path.read_text(encoding="utf-8"))["source_stat"] is not None
    assert _fresh_read(tmp_path, sp) == {"md": [], "stale": []}


def _as_walked_before_source_stat(sp: Path, root: Path) -> None:
    """The model's walk cached as a build before `source_stat` existed left it: its contract alone."""
    m_entry = next(m for m in load_store_index(sp).models if m.name == "Memo")
    m_idx = load_models_index(root / m_entry.models_index)
    built_cache.put(sp, "edges_shards", "Memo", edge_cache_key(m_idx), m_idx.contract_hash)
