"""Document ids of Python symbols that differ only by case (GD24: `transaction` and `Transaction`
in `sldb.api.documents.transaction`) no longer collide; every other id stays as it was."""
from __future__ import annotations

from sldb.selfdoc.python_materialize import plan_python_documents
from sldb.selfdoc.python_scanner import PythonScanner

SOURCE = (
    "class Transaction:\n    \"\"\"The operations.\"\"\"\n\n"
    "def transaction():\n    \"\"\"Open one.\"\"\"\n\n"
    "class Box:\n    \"\"\"A box.\"\"\"\n    def open(self):\n        \"\"\"Open it.\"\"\"\n"
)


def _ids(tmp_path):
    source = tmp_path / "src" / "demo"
    source.mkdir(parents=True)
    (source / "mod.py").write_text(SOURCE, encoding="utf-8")
    records = PythonScanner().scan(tmp_path / "src", "demo")
    return sorted(plan.payload.id for plan in plan_python_documents(records, "demo", tmp_path / "out"))


def test_symbols_that_differ_only_by_case_get_the_kind_as_suffix(tmp_path):
    ids = _ids(tmp_path)
    assert "python-demo-demo-demo-mod-transaction--class" in ids
    assert "python-demo-demo-demo-mod-transaction--function" in ids


def test_ids_without_collision_are_unchanged(tmp_path):
    ids = _ids(tmp_path)
    assert "python-demo-demo-demo-mod-box" in ids
    assert "python-demo-demo-demo-mod-box-open" in ids
    assert len(ids) == len(set(ids)) == 4
