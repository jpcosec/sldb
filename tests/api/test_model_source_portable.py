"""`models template show` finds a model's source through `model_ref` when the recorded path is
no file here (a store copied without its models, an absolute path from another machine, an
inherited model), and says which model and store when neither works.

The issue (issue-sldb-model-source-path-not-portable): the recorded path was tried alone, and
failed with a bare `No such file or directory` (or `Is a directory` for an inherited model).
"""

from __future__ import annotations

import sys

import pytest

from sldb.api import add_model, init_store, locate_model_source
from sldb.core.exceptions import SLDBModelError
from sldb.store.io import invalidate_index_cache, load_store_index, save_store_index

MODULE = "sldb_portable_source_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


@pytest.fixture
def store(tmp_path):
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root = tmp_path / "world"
    root.mkdir()
    sp = init_store(root).store_path
    add_model(sp, f"{MODULE}:Note", str(tmp_path))
    yield sp, tmp_path
    sys.path.remove(str(tmp_path))
    sys.modules.pop(MODULE, None)


def _record(sp, **fields) -> None:
    idx = load_store_index(sp)
    for m in idx.models:
        for key, value in fields.items():
            setattr(m, key, value)
    save_store_index(sp, idx)
    invalidate_index_cache()


@pytest.mark.parametrize("recorded", ["models/gone.py", "/elsewhere/on/another/machine.py", ""])
def test_a_recorded_path_that_is_no_file_here_falls_back_to_the_ref(store, recorded):
    sp, tmp_path = store
    _record(sp, path=recorded)
    assert locate_model_source(sp, "Note", str(tmp_path)).path == (tmp_path / f"{MODULE}.py").resolve()


def test_neither_path_nor_ref_names_the_model_and_the_store(store):
    sp, tmp_path = store
    _record(sp, path="models/gone.py", model_ref="no_such_package.models:Note")
    with pytest.raises(SLDBModelError, match=r"Model 'Note' of store .*--pythonpath"):
        locate_model_source(sp, "Note", str(tmp_path))
