# Task: add `sldb serve` — the CLI as an HTTP transport over the REAL store methods

## Thesis
The server is the CLI. Same core methods, different transport. `sldb serve`
must call the EXACT functions the CLI already uses to read and write the store —
NO reimplementation, NO mocks, NO parallel logic. A browser client (graph_ui)
will consume it, but this task only adds the server to sldb.

## Environment
- Worktree: `/home/jp/proyectos/hum-ecosystem/tools/iso-lab/worktrees/sldb`, branch `iso-lab/sldb` (already has the Codec refactor at 49b9d49). Edit ONLY here.
- Validation runs in the sealed image via host `tools/iso-lab/bin/lab-test.sh`.
  Baselines that MUST stay green: **sldb 414 (Codec added 3), kgdb 23, deskops 140**.
- Use ONLY the Python standard library (`http.server`, `json`, `urllib`). Do NOT
  add any dependency (no flask/fastapi). The sealed image has no extra web deps.

## Non-negotiable constraints
- NO mocks/stubs/fake/placeholder/TODO as deliverable. Real store calls only.
- Do NOT modify existing CLI command behavior. `serve` is ADDITIVE.
- Do NOT change the store's public functions. Call them as-is.
- Keep it minimal and readable. Respect the repo's clean-code gate
  (max 1 class per file; short functions — the existing `test_clean_code_rules`
  suite enforces this and is part of the 414).

## The REAL methods to expose (verified signatures — call these, don't reinvent)
- READ all docs:
  `from sldb.store.query import load_runtime_documents`
  `load_runtime_documents(store_path: Path, resolve_model_ref, pythonpath: str|None=None) -> list[RuntimeDocument]`
- Resolve a model type:
  `from sldb.cli.model_utils import resolve_model_ref`
  `resolve_model_ref(model_ref: str, pythonpath: str|None=None) -> type`
- Store context (path resolution exactly like the CLI):
  `from sldb.cli.store_context import get_store_context`
  `get_store_context(store_arg: str|None, mode="default") -> tuple[Path, Path]  # (store_path, project_root)`
- WRITE a doc's fields (the CLI's `fields save`):
  `from sldb.cli.commands.fields_save import save_payload`
  `save_payload(runtime_doc: RuntimeDocument, payload: dict, store_arg: str|None, pythonpath: str|None) -> int`
  NOTE: save_payload needs a RuntimeDocument. To obtain it for a given doc name,
  call load_runtime_documents and pick the record whose `.name == doc_name`.
- KGDB assembler snapshot (optional endpoint):
  `from sldb.store.export import export_kgdb_semantic_payload`
  `export_kgdb_semantic_payload(store_path: Path, project_root: Path, resolve_model_ref, pythonpath) -> dict`

`RuntimeDocument` fields (dataclass): store_name, store_path, model_name,
model_type, name, path, payload(dict), semantic_tags(list).

## How the CLI is structured (mirror this pattern exactly)
- Handlers registered in `src/sldb/cli/dispatcher.py` (`CLI.__init__` -> `_load_1/2/3`), each `Xxx CLI().run` keyed by command name.
- Subcommand parsers added under `src/sldb/cli/parsers/` and wired in
  `src/sldb/cli/parsers/core.py::_add_commands(s)` via an `add_<name>_commands(s)` function that mirrors `parsers/find.py`.
- Command implementation classes live in `src/sldb/cli/commands/`.

## Implementation

### 1. Parser: `src/sldb/cli/parsers/serve.py`
```python
from __future__ import annotations
import argparse

def add_serve_commands(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("serve", help="Serve the store over HTTP using the same methods as the CLI.")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8787)
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")
    p.add_argument("--cors", action="store_true", help="Send permissive CORS headers (for browser clients)")
```
Wire it in `parsers/core.py`: import `add_serve_commands` and call it inside `_add_commands`.

### 2. HTTP server module: `src/sldb/cli/serve/http_server.py`
- A function `build_handler(store_arg, pythonpath, cors)` returning an
  `http.server.BaseHTTPRequestHandler` subclass (one class per file — keep the
  subclass in this file; put helpers as module functions).
- Endpoints (all JSON):
  - `GET /health` -> `{"status":"ok"}`.
  - `GET /schema` -> the registered models projected to a UI-friendly field
    descriptor. Derive from the store index + each model type. For each model:
    `{ id: model_name, model_ref, fields: [ {name, kind, required, enum?} ] }`.
    Get fields by resolving the model type and reading its pydantic fields
    (`model_type.model_fields` -> for each: name, `field.is_required()`, and if
    the annotation is an Enum, list its values; map python types to a coarse
    `kind` string: str->"string", enum->"enum", list->"stringlist", etc.).
    This is REAL schema introspection from the sldb model — not a hand table.
  - `GET /graph` -> `{ documents: [ {id, model_name, path, payload, semantic_tags} ] }`
    built from `load_runtime_documents(...)`. Serialize `path` as str.
  - `POST /save` with body `{ "doc": "<doc name>", "payload": { ... } }` ->
    load runtime docs, find the one whose `.name == doc`, call
    `save_payload(that_doc, payload, str(store_path), effective_pythonpath)`,
    return `{"ok": true, "doc": "<name>"}`. On unknown doc -> 404 JSON error. On
    validation failure (save_payload raises SystemExit with the idempotency
    message) -> 400 JSON `{"ok": false, "error": "<message>"}`.

    CRITICAL (verified by comprehension gate): `save_payload` internally calls
    `get_store_context(store_arg)` AGAIN and `resolve_model_ref(..., pythonpath)`.
    If you pass `store_arg=None` it re-resolves from CWD and may hit a DIFFERENT
    store than the one you read from -> reads and writes diverge. Therefore the
    server MUST pass the EXPLICIT resolved values: `store_arg = str(store_path)`
    (the same store_path from the one-time `get_store_context(cli_store_arg)`) and
    `pythonpath = effective_pythonpath` (never None). Same rule everywhere:
    reads via `load_runtime_documents(store_path, resolve_model_ref, effective_pythonpath)`,
    writes via `save_payload(doc, payload, str(store_path), effective_pythonpath)`.
    This guarantees read and write hit the SAME store and the SAME import base.
  - `GET /kgdb/snapshot` -> `export_kgdb_semantic_payload(store_path, project_root, resolve_model_ref, pythonpath)`.
  - Unknown route -> 404 JSON.
- If `cors` is true, add `Access-Control-Allow-Origin: *` and handle `OPTIONS`
  preflight (return 204 with the CORS headers).
- Resolve `store_path, project_root = get_store_context(store_arg)` ONCE at
  handler-build time. Compute `effective_pythonpath = pythonpath or str(project_root)`.
  Use `store_path` and `effective_pythonpath` EXPLICITLY for BOTH reads and writes
  (see the CRITICAL note under POST /save). Never let save_payload re-resolve from
  a None store_arg.
- Catch exceptions per-request and return a JSON 500 `{"ok": false, "error": str(e)}`
  so the server never crashes on a bad request.

### 3. Command class: `src/sldb/cli/commands/serve.py`
```python
class ServeCLI:
    def run(self, args) -> int:
        from http.server import ThreadingHTTPServer
        from sldb.cli.serve.http_server import build_handler
        handler = build_handler(args.store, args.pythonpath, getattr(args, "cors", False))
        httpd = ThreadingHTTPServer((args.host, args.port), handler)
        print(f"sldb serve on http://{args.host}:{args.port} (store={args.store or 'auto'})")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()
        return 0
```
(Keep to the 1-class-per-file rule.)

### 4. Register in dispatcher
In `src/sldb/cli/dispatcher.py`, add to one of the `_load_*` methods:
`from sldb.cli.commands.serve import ServeCLI` and
`self.handlers.update({"serve": ServeCLI().run})`.

## Tests (add REAL tests; they raise the sldb count above 414 — that's expected & fine)
Create `tests/test_serve.py` that:
- Build a REAL store by reusing the existing CLI-driven helpers in
  `tests/store/test_cli_store.py` (verified by the gate): `_init`, `_model_add`,
  `_doc_track` (and the `SimpleBook` model / `_STORE_ARGS` / `_PY_ARGS` if useful).
  These drive the actual CLI against a real store + real StructuredNLDoc model.
  Do NOT use the hand-made `populated_store` from test_queries_expanded.py and do
  NOT fabricate a store by hand.
- Starts the handler via `http.server` on an ephemeral port in a background thread
  (or better: instantiate the handler and drive it with a real socket using
  `ThreadingHTTPServer(("127.0.0.1", 0), handler)` then read `.server_address[1]`).
- Asserts:
  - `GET /health` -> 200 `{"status":"ok"}`.
  - `GET /schema` -> contains the registered model with a `fields` list.
  - `GET /graph` -> returns the tracked document(s) with resolved `payload`.
  - `POST /save` with a valid payload -> 200 `{"ok": true}` AND re-reading `/graph`
    shows the change persisted (prove the write hit the real store).
  - `POST /save` to a non-existent doc -> 404.
- Shut the server down in a finally.
Use only stdlib (`urllib.request`, `threading`, `json`).

## Validation (run from host, paste output)
```
cd /home/jp/proyectos/hum-ecosystem/tools/iso-lab
bin/lab-test.sh          # sldb >=414 with ZERO failures, kgdb 23, deskops 140
```
Manual smoke inside the sealed image (prove it actually serves), using a store the
tests create or the repo's own .sldb:
```
docker run --rm -v <worktree>:/w iso-lab:base bash -c '
  pip install --no-deps -e /w >/dev/null 2>&1
  cd /w
  python -m sldb serve --port 8787 & SRV=$!; sleep 2
  curl -s localhost:8787/health
  curl -s localhost:8787/schema | head -c 400
  kill $SRV'
```

## Done when
- `sldb serve` starts and answers /health, /schema, /graph, /save, /kgdb/snapshot.
- /save actually persists via save_payload (verified by re-reading /graph).
- /schema fields come from REAL model introspection (model_fields), not a hand table.
- sldb >=414 (0 failures), kgdb 23, deskops 140 — via lab-test.sh.
- Only stdlib used; no existing CLI behavior changed.

## Commit
When green, commit on the branch:
`git add -A && git commit -m "feat(cli): add 'sldb serve' — HTTP transport over the real store read/write methods"`
Do NOT touch primary main. Do NOT promote. Report: files created/edited, lab-test.sh output (3 lines), the smoke curl output, commit hash. If blocked, STOP and report — no fake data, no reimplementation of store logic.
