"""A document's edges are rebuilt when its model's contract moves, even if its text does not.

deskops added `__reference_models__` to TaskDoc and ran `stores update`: the models index took
the new contract, but every TaskDoc shard was reused (its document's hashes had not moved, and
no document was dirty), so the `depends_on` edges the declaration resolves never appeared and
`edges rebuild` walked nothing. Only deleting the shards by hand brought them.
"""

from __future__ import annotations

import sys

from sldb import api
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_edges_contract_test_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Task(StructuredNLDoc):
    __references__ = ["depends_on"]
    {declaration}
    __template__ = "---\\ndepends_on: ⸢rev,list•depends_on⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    depends_on: list = Field(default_factory=list, description="Tasks this one waits for.")
'''


def test_a_new_reference_declaration_reaches_the_edges_on_update(tmp_path):
    module, py = tmp_path / f"{MODULE}.py", str(tmp_path)
    module.write_text(_MODELS.format(declaration=""), encoding="utf-8")
    sys.path.insert(0, py)
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp = api.init_store(root).store_path
        api.add_model(sp, f"{MODULE}:Task", py)
        api.create_document(sp, "Task", root / "b.md", {"title": "b"}, "b", py)
        api.create_document(sp, "Task", root / "a.md", {"title": "a", "depends_on": ["b"]}, "a", py)
        assert api.edges_from(sp, "Task:a", "references") == []        # a bare id in a free field

        module.write_text(_MODELS.format(declaration='__reference_models__ = {"depends_on": ["Task"]}'), encoding="utf-8")
        sys.modules.pop(MODULE, None)
        invalidate_runtime_cache()
        api.update_store_indexes(sp, root, py)
        assert [e.target for e in api.edges_from(sp, "Task:a", "references")] == ["sldb://document/Task:b"]
        assert api.rebuild_edges(sp, py).docs_written == 0, "and the next rebuild has nothing left to do"
    finally:
        sys.path.remove(py)
        sys.modules.pop(MODULE, None)
