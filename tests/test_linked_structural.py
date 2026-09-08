"""Store-qualified structural addresses: `B:st.{Model+}.doc` reads a linked store the way
`st.…` reads the local one, and results from a linked store carry the prefix back."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as sldb_main
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.query import find_structural, get_structural, glob_structural, list_structural

MODEL_SRC = (
    "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
    "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
    "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
)


def _store(root: Path, names: list[str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "linkfix_models.py").write_text(MODEL_SRC)
    assert sldb_main(["stores", "init", "--path", str(root)]) == 0
    assert sldb_main(["models", "add", "linkfix_models:NoteDoc", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    for name in names:
        (root / f"{name}.md").write_text(f"# {name}\n\nbody of {name}\n")
        assert sldb_main(["docs", "track", str(root / f"{name}.md"), "--model", "NoteDoc", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    return root


def test_a_linked_store_is_reached_by_prefix_and_answers_with_it(tmp_path: Path):
    a = _store(tmp_path / "a", ["alpha"])
    b = _store(tmp_path / "b", ["beta", "gamma"])
    assert sldb_main(["stores", "add", str(b / ".sldb"), "--name", "b", "--store", str(a / ".sldb")]) == 0
    sp = a / ".sldb"
    assert list_structural(sp, "st.{NoteDoc}", resolve_model_ref, str(a)) == ["alpha"]
    assert list_structural(sp, "b:st.{NoteDoc}", resolve_model_ref, str(a)) == ["beta", "gamma"]
    assert find_structural(sp, "b:st.{NoteDoc+}", 'body ~ "gamma"', resolve_model_ref, str(a)) == ["b:st.{NoteDoc+}.gamma"]
    assert find_structural(sp, "st.{NoteDoc+}", 'body ~ "gamma"', resolve_model_ref, str(a)) == []
    assert get_structural(sp, "b:st.{NoteDoc}.beta.body", resolve_model_ref, str(a)) == "body of beta"
    assert get_structural(sp, "local:st.{NoteDoc}.alpha.body", resolve_model_ref, str(a)) == "body of alpha"
    assert glob_structural(sp, "b:st.{NoteDoc}.*", resolve_model_ref, str(a)) == ["b:st.{NoteDoc}.beta", "b:st.{NoteDoc}.gamma"]
    assert find_structural(sp, "nope:st.{NoteDoc+}", "has(body)", resolve_model_ref, str(a)) == []
