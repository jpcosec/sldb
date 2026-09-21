"""One document's normalized tree: the CLI `ast show docs/<doc>` surface, api-side.

The whole DocumentIR is exposed (parsed by ``build_document_ir``, the CLI's real
builder): ``structure`` holds the normalized meaning tree and ``surface`` the raw
parse nodes, so no single node representation is preferred. The raw section
records come from ``extract_sections``, the same helper the CLI ast command uses.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_payload import runtime_document


def document_ast(store_path: Path, project_root: Path, pythonpath: str | None, doc_ref: str) -> dict[str, Any]:
    """The CLI's `ast show docs/<doc>` payload: doc metadata, sections, full IR."""
    from sldb.cli.graph_ops import extract_sections

    doc = runtime_document(store_path, pythonpath, doc_ref)
    markdown = Path(project_root / doc.path).read_text(encoding="utf-8")
    runtime_dict = {"store": doc.store_name, "model": doc.model_name, "name": doc.name, "path": doc.path, "payload": doc.payload, "semantic_tags": doc.semantic_tags}
    ir = build_ir_json(runtime_dict, markdown, getattr(doc.model_type, "__template__", None))
    sections = [vars(section) for section in extract_sections(markdown)]
    return {"document": {"store": doc.store_name, "model": doc.model_name, "name": doc.name, "path": doc.path, "semantic_tags": list(doc.semantic_tags), "payload": doc.payload, "sections": sections, "ir": ir}}


def build_ir_json(runtime_doc: dict[str, Any], markdown: str, template: str | None) -> dict[str, Any]:
    from sldb.api import build_document_ir_json

    return build_document_ir_json(runtime_doc, markdown, template)