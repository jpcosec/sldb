"""JSON projection of a document's IR: serialization lives here, not in the serve transport.

The IR itself is built by the CLI's real builder (``sldb.cli.graph_ops.build_ir``,
the same one ``sldb sections show`` uses); nothing here reimplements markdown
parsing or IR construction — only the pydantic models are projected to JSON.
"""

from __future__ import annotations

from typing import Any


def build_document_ir_json(
    runtime_doc: dict[str, Any],
    markdown: str,
    template: str | None = None,
) -> dict[str, Any]:
    """The IR of one runtime document, as the JSON the transport returns."""
    from sldb.cli.graph_ops.build_ir import build_document_ir

    return build_document_ir(
        runtime_doc, markdown, template=template
    ).model_dump(mode="json")