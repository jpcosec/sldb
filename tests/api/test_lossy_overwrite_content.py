"""`refuse_lossy_overwrite` lets an undeclared heading go when its text survives in the new text."""

from __future__ import annotations

import pytest

import sldb.api as api
from sldb.core.exceptions import SLDBValidationError

from .conftest import PAYLOAD


def _with_extra(api_store, body: str):
    path = api_store.root / "login.md"
    path.write_text(path.read_text(encoding="utf-8") + f"\n## Extra\n\n{body}\n", encoding="utf-8")


def test_an_undeclared_heading_whose_text_stays_in_a_field_does_not_block_the_write(api_store):
    _with_extra(api_store, "auth")
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Kept"}, api_store.pythonpath)
    text = (api_store.root / "login.md").read_text(encoding="utf-8")
    assert "# Kept" in text and "## Extra" not in text and "- auth" in text


def test_an_undeclared_heading_whose_text_is_lost_still_blocks_the_write(api_store):
    _with_extra(api_store, "something only the heading carries")
    with pytest.raises(SLDBValidationError, match="Extra"):
        api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Lost"}, api_store.pythonpath)
