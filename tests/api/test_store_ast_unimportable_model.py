"""One registered model that does not import here does not take the store's AST down with it.

In a venv without `pron`, `models show TaskDoc` failed with "Failed to import module
'pron.models'": the store AST imports every model, and the first failure aborted it.
"""

from __future__ import annotations

from sldb.api import add_model, init_store
from sldb.cli.graph_ops import ast_for_target
from sldb.store.io import invalidate_index_cache, load_store_index, save_store_index


def test_a_model_that_does_not_import_is_listed_unresolved_and_the_rest_still_answers(tmp_path):
    sp = init_store(tmp_path).store_path
    add_model(sp, "sldb.models.relation_doc:RelationDoc")
    add_model(sp, "sldb.models.relation_type_doc:RelationTypeDoc")
    idx = load_store_index(sp)
    for m in idx.models:
        if m.name == "RelationTypeDoc":
            m.model_ref = "no_such_package.models:RelationTypeDoc"     # its package is not installed here
    save_store_index(sp, idx)
    invalidate_index_cache()

    shown = ast_for_target(str(sp), None, "models/RelationDoc")["model"]
    assert "resolved" not in shown and shown["fields"]          # a healthy model keeps describe_model's shape
    broken = ast_for_target(str(sp), None, "models/RelationTypeDoc")["model"]
    assert (broken["resolved"], broken["fields"]) == (False, []) and "no_such_package" in broken["error"]
