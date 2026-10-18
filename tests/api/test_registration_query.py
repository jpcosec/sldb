"""Which models a store registers, asked through the API and `sldb models check`.

deskops (inbox 20260614-000003) parsed `store_index.yaml` itself to verify that its models were
registered.
"""

from __future__ import annotations

import json

from sldb.api import add_model, init_store, is_model_registered, registered_models
from sldb.cli import main

REF = "sldb.models.relation_doc:RelationDoc"


def test_registered_models_and_each_way_to_name_one(tmp_path, capsys):
    sp = init_store(tmp_path).store_path
    add_model(sp, REF)
    assert [m.name for m in registered_models(sp)] == ["RelationDoc"]
    assert all(is_model_registered(sp, name) for name in ("RelationDoc", REF, REF.replace(":", ".")))
    assert not is_model_registered(sp, "TaskDoc")


def test_models_check_names_each_and_fails_on_a_missing_one(tmp_path, capsys):
    sp = init_store(tmp_path).store_path
    add_model(sp, REF)
    assert main(["models", "check", "RelationDoc", "--store", str(sp)]) == 0
    capsys.readouterr()
    assert main(["models", "check", "RelationDoc", "TaskDoc", "--store", str(sp), "--format", "json"]) == 1
    assert json.loads(capsys.readouterr().out) == {"models": [{"model": "RelationDoc", "registered": True}, {"model": "TaskDoc", "registered": False}], "ok": False}
