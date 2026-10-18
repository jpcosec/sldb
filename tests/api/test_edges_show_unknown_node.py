"""`edges show` with a document's name, not its node id, says so instead of printing `[]`.

The issue (issue-sldb-edges-show-silent-empty-on-document-name): `edges show pill-008-x`
answered `[]` with exit 0, the same as a real node without edges.
"""

from __future__ import annotations

import pytest

from sldb.cli import main
from tests.api.test_unresolved_references import store  # noqa: F401 - the fixture


def test_a_bare_document_name_is_refused_with_its_export_id(store, capsys):  # noqa: F811
    with pytest.raises(SystemExit, match=r"Did you mean Task:b\?"):
        main(["edges", "show", "b", "--store", str(store)])


def test_a_name_no_document_has_is_refused_with_the_id_forms(store):  # noqa: F811
    with pytest.raises(SystemExit, match="export id"):
        main(["edges", "show", "nothing-here", "--store", str(store)])


def test_a_node_with_no_edges_of_that_relation_is_still_an_empty_list(store, capsys):  # noqa: F811
    assert main(["edges", "show", "Task:b", "--relation", "references", "--store", str(store)]) == 0
    assert capsys.readouterr().out.strip() == "[]"
