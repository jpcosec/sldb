"""A model's `__family__` changed in the class reaches the store on `stores update` and `models update`.

AgentsKBs (2026-10-03): `family` was written only at `models add`, so changing the class's
`__family__` left the store declaring the old one, and no command said so.
"""

from __future__ import annotations

import sys

import pytest

from sldb import api
from sldb.cli import main
from sldb.store.io import invalidate_index_cache, load_models_index, load_store_index
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_family_follow_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Campaign(StructuredNLDoc):
    __family__ = "{family}"
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


@pytest.fixture
def store(tmp_path):
    module = tmp_path / f"{MODULE}.py"
    module.write_text(_MODELS.format(family="cobranza"), encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root = tmp_path / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:Campaign", str(tmp_path))
    api.create_document(sp, "Campaign", root / "c.md", {"title": "c"}, "c", str(tmp_path))
    module.write_text(_MODELS.format(family="outbound-calls"), encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_runtime_cache()
    yield sp, root, str(tmp_path)
    sys.path.remove(str(tmp_path))
    sys.modules.pop(MODULE, None)


def _families(sp, root) -> tuple[str | None, str | None]:
    invalidate_index_cache()
    entry = next(m for m in load_store_index(sp).models if m.name == "Campaign")
    return entry.family, load_models_index(root / entry.models_index).family


def test_stores_update_rereads_the_family(store):
    sp, root, py = store
    assert _families(sp, root) == ("cobranza", "cobranza")
    api.update_store_indexes(sp, root, py)
    assert _families(sp, root) == ("outbound-calls", "outbound-calls")
    assert api.check_store(sp, root, py)["valid"]


def test_models_update_rereads_the_family(store):
    sp, root, py = store
    assert main(["models", "update", "Campaign", "--store", str(sp), "--pythonpath", py]) == 0
    assert _families(sp, root) == ("outbound-calls", "outbound-calls")
