"""`extract_payload` and `render_markdown` live in `core/template_payload.py` (render axis)
and `sldb.runtime.validation` still exports them under the same names (deskops imports them there)."""

from sldb.core import template_payload
from sldb.runtime import validation
from tests.api.conftest import MODULE, PAYLOAD


def test_validation_reexports_the_same_functions():
    assert validation.extract_payload is template_payload.extract_payload
    assert validation.render_markdown is template_payload.render_markdown


def test_extract_payload_reads_a_document_from_its_template_alone(api_store):
    from sldb.api import resolve_model_ref

    model_type = resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    markdown = (api_store.root / "login.md").read_text(encoding="utf-8")
    assert template_payload.extract_payload(model_type.__template__, markdown)["title"] == PAYLOAD["title"]
