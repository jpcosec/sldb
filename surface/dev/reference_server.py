"""Servidor de referencia: `sldb serve` real + los endpoints del HANDOFF vía prototipo.

Existe solo hasta que SLDB implemente el HANDOFF. Todas las rutas que ya existen
(/graph, /document, /save, /find, ...) las atiende el handler real de `sldb serve`;
este archivo solo agrega:

  GET  /document/segments?id=<doc>     contrato DocumentSegments
  POST /extract/segments {model, markdown}  contrato ExtractionSegments
  GET  /schema                          igual al real, pero un modelo no importable
                                        no tumba la respuesta entera

Uso (desde la raíz del proyecto que contiene .sldb/):
  python dev/reference_server.py --store .sldb --pythonpath . --port 8787
"""

from __future__ import annotations

import argparse
import os
import sys
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

import segments_prototype as proto  # noqa: E402
from sldb.api.model_registry.load_registered_model import load_registered_model  # noqa: E402
from sldb.cli.model_utils import resolve_model_ref  # noqa: E402
from sldb.cli.serve.http_server import build_handler  # noqa: E402
from sldb.cli.serve.responses import read_json_body, send_json  # noqa: E402
from sldb.cli.serve.schema import schema_model  # noqa: E402
from sldb.store.io import load_store_index  # noqa: E402
from sldb.store.query import load_runtime_documents  # noqa: E402


def _docs(handler):
    return load_runtime_documents(handler.store_path, resolve_model_ref, handler.pythonpath)


def _path_index(handler, docs):
    root = handler.project_root.resolve()
    return {str((root / d.path).resolve()): d.name for d in docs}


def document_segments(handler, doc_id):
    docs = _docs(handler)
    doc = next((d for d in docs if d.name == doc_id), None)
    if doc is None:
        return {"ok": False, "error": f"Unknown doc: {doc_id}"}, 404
    root = handler.project_root.resolve()
    by_path = _path_index(handler, docs)
    resolve = lambda ref: by_path.get(str((root / str(ref).strip().strip("`")).resolve()))
    source_text = (root / doc.path).read_text(encoding="utf-8")
    result = proto.document_segments(doc.model_type, doc.payload, doc=doc.name,
                                     source_text=source_text, resolve_doc=resolve)
    return {**result, "id": doc.name, "path": doc.path, "payload": doc.payload}, 200


def extraction_segments(handler, body):
    model, markdown = body.get("model"), body.get("markdown")
    if not isinstance(model, str) or not isinstance(markdown, str):
        return {"ok": False, "error": "Se espera {model: str, markdown: str}."}, 400
    try:
        model_type = load_registered_model(handler.store_path, model, handler.pythonpath).model_type
        return proto.extraction_segments(model_type, markdown), 200
    except Exception as exc:  # el prototipo no distingue errores de extracción
        return {"ok": False, "error": str(exc)}, 422


def tolerant_schema(handler):
    models, errors = [], []
    for entry in load_store_index(handler.store_path).models:
        try:
            models.append(schema_model(entry, handler.pythonpath))
        except Exception as exc:
            errors.append({"model": entry.name, "error": str(exc)})
    return {"models": models, "errors": errors}, 200


def extend(base):
    class ReferenceHandler(base):
        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/document/segments":
                doc_id = parse_qs(url.query).get("id", [""])[0]
                return send_json(self, *reversed(document_segments(self, doc_id)), self.cors)
            if url.path == "/schema":
                return send_json(self, *reversed(tolerant_schema(self)), self.cors)
            return super().do_GET()

        def do_POST(self):
            if urlparse(self.path).path == "/extract/segments":
                body = read_json_body(self)
                return send_json(self, *reversed(extraction_segments(self, body)), self.cors)
            return super().do_POST()

        def log_message(self, fmt, *args):
            sys.stderr.write(f"{self.command} {self.path} -> {args[1] if len(args) > 1 else ''}\n")

    return ReferenceHandler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", default=".sldb")
    parser.add_argument("--pythonpath", default=".")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    handler = extend(build_handler(args.store, args.pythonpath, cors=True))
    os.chdir(handler.project_root)  # las composiciones resuelven rutas relativas al CWD
    sys.path.insert(0, str(Path(args.pythonpath).resolve()))
    print(f"reference server on http://{args.host}:{args.port} (store={handler.store_path})")
    ThreadingHTTPServer((args.host, args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
