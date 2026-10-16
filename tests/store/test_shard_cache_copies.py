"""A loaded shard is the caller's own copy: editing it and saving it back writes the edit.

The cache used to hand out its own instance, so a caller that edited what it loaded was
compared against its own edit and the save was skipped. `fields update` did exactly that: the
Markdown and the roster moved, the document's record did not, and `stores check` failed on the
write sldb itself had just made.
"""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as sldb_main
from sldb.store.io.shards import load_document_shard, save_document_shard
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.io.utils import yaml_load

MODEL_SRC = (
    "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
    "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
    "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
)


def test_an_edited_shard_is_written(tmp_path: Path):
    path = tmp_path / "note.yaml"
    save_document_shard(path, DocumentEntry(name="note", path="note.md", source_hash="old"))
    entry = load_document_shard(path)
    entry.source_hash = "new"
    save_document_shard(path, entry)
    assert yaml_load(path.read_text(encoding="utf-8"))["source_hash"] == "new"
    assert load_document_shard(path).source_hash == "new"


def test_editing_a_loaded_shard_does_not_touch_the_cache(tmp_path: Path):
    path = tmp_path / "note.yaml"
    save_document_shard(path, DocumentEntry(name="note", path="note.md", source_hash="old"))
    load_document_shard(path).source_hash = "edited, never saved"
    assert load_document_shard(path).source_hash == "old"


def test_fields_update_leaves_the_store_passing(tmp_path: Path):
    (tmp_path / "shardcopy_models.py").write_text(MODEL_SRC)
    (tmp_path / "note.md").write_text("# hello\n\nold body\n")
    sp, pp = str(tmp_path / ".sldb"), str(tmp_path)
    assert sldb_main(["stores", "init", "--path", pp]) == 0
    assert sldb_main(["models", "add", "shardcopy_models:NoteDoc", "--store", sp, "--pythonpath", pp]) == 0
    assert sldb_main(["docs", "track", str(tmp_path / "note.md"), "--model", "NoteDoc", "--store", sp, "--pythonpath", pp]) == 0
    assert sldb_main(["fields", "update", "docs/NoteDoc/note/body", '"new body"', "--store", sp, "--pythonpath", pp]) == 0
    assert "new body" in (tmp_path / "note.md").read_text()
    assert sldb_main(["stores", "check", "--store", sp, "--pythonpath", pp, "--quiet"]) == 0
