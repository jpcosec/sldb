"""GET /ast: one document's normalized tree, exactly as the CLI `ast show` sees it.

The whole DocumentIR is exposed, not a partial view: ``structure`` is the
normalized meaning tree, ``surface`` the raw parser nodes, and ``sections`` the
same section records the CLI ast command prints. Delegates to
``sldb.api.document_ast``, which composes the CLI's real IR builder.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import document_ast
from sldb.cli.serve.params import query_params, require_param


def dispatch_ast(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    doc, error = require_param(query_params(handler), "doc")
    if error is not None:
        return error, 400
    try:
        return document_ast(store_path, project_root, pythonpath, doc), 200
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 404
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 422