#!/usr/bin/env python3
"""Servidor local de anotaciones para las vistas UML (planning-only).

Uso:
    python3 scripts/annotate_server.py

Abrir:  http://localhost:8765/docs/architecture/sldb_Kernel_Vistas_UML.html
Las marcas se persisten en desk/contexts/vistas-uml.annotations.json
"""
import json
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANNOTATIONS = ROOT / "desk" / "contexts" / "vistas-uml.annotations.json"
PORT = 8765


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_annotations(self):
        if ANNOTATIONS.exists():
            return json.loads(ANNOTATIONS.read_text())
        return []

    def _write_annotations(self, data):
        ANNOTATIONS.parent.mkdir(parents=True, exist_ok=True)
        ANNOTATIONS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    def do_GET(self):
        if self.path == "/annotations":
            self._send_json(self._read_annotations())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != "/annotate":
            self._send_json({"error": "not found"}, 404)
            return
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if not {"vista", "label", "comentario"} <= payload.keys():
            self._send_json({"error": "faltan campos: vista, label, comentario"}, 400)
            return
        data = self._read_annotations()
        data.append({
            "vista": payload["vista"],
            "label": payload["label"],
            "comentario": payload["comentario"],
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        })
        self._write_annotations(data)
        self._send_json({"ok": True, "total": len(data)})

    def do_DELETE(self):
        if self.path != "/annotate":
            self._send_json({"error": "not found"}, 404)
            return
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        data = [a for a in self._read_annotations()
                if not (a.get("vista") == payload.get("vista")
                        and a.get("label") == payload.get("label"))]
        self._write_annotations(data)
        self._send_json({"ok": True, "total": len(data)})

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    print(f"→ http://localhost:{PORT}/docs/architecture/sldb_Kernel_Vistas_UML.html")
    print(f"→ anotaciones: {ANNOTATIONS.relative_to(ROOT)}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
