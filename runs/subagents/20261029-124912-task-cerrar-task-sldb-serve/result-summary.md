# Result: verify TASK-sldb-serve.md against src/sldb/cli/serve/

Task: task-cerrar-task-sldb-serve-sldb-serve-ya-existe. Verification only. No code edited, no desk/ documents touched, TASK-sldb-serve.md still on disk, no `deskops closeout` run.

## Endpoint requested -> implementation -> test

| Requested | Route / code (src/sldb/cli/) | Test |
|---|---|---|
| `GET /health` -> `{"status":"ok"}` | `serve/routes.py::dispatch_get` -> `serve/health.py::health_payload` (superset: `status`, `findings`, `action`) | `tests/test_serve.py::test_serve_endpoints_use_real_store` (asserts `{"status":"ok","findings":[],"action":None}`) |
| `GET /schema` (models with `fields`, from `model_fields`) | `routes.py` -> `serve/schema.py::store_schema`/`schema_model`/`field_descriptors` (uses `model_type.model_fields`, `resolve_model_ref`) | `test_serve_endpoints_use_real_store`; `test_schema_includes_model_graph_dunders`; `test_schema_declares_models_that_cannot_load`; `test_schema_degrades_per_model_instead_of_losing_the_response` |
| `GET /graph` (documents with resolved payload) | `routes.py` -> `serve/graph_payload.py::graph_payload` (reads via `load_runtime_documents`) | `test_serve_endpoints_use_real_store`; `test_graph_declares_models_whose_documents_are_missing`; `test_graph_endpoints_use_real_api` (/graph/*) |
| `POST /save` `{doc,payload}` -> `{"ok":true,"doc":...}` | `routes.py::dispatch_post` -> `serve/save_routes.py::save_request` -> `serve/save_single.py::save_single` (explicit `store_path` + `pythonpath`) | `test_serve_endpoints_use_real_store` (200, `/graph` re-read shows change, Markdown file rewritten) |
| `POST /save` unknown doc -> 404 JSON | `serve/save_single.py` | `test_serve_endpoints_use_real_store` (404, `{"ok":false,"error":"Unknown doc: missing"}`) |
| `POST /save` validation failure -> 400 `{"ok":false,"error"}` | `serve/http_server.py::_dispatch_and_send` maps `SystemExit` -> 400; `save_single` / `save_plan.py` | `test_batch_save_invalid_payload_422` (the batch path returns 422). **No dedicated single-save 400 test found.** |
| `GET /kgdb/snapshot` (optional) | **Not present under that name.** Equivalent: `GET /semantic-export` in `routes.py::dispatch_get` -> `sldb.store.export.export_semantic_payload(store_path, project_root, resolve_model_ref, pythonpath)` | **None.** No test in tests/test_serve*.py references `/semantic-export` |
| Unknown route -> 404 JSON | `routes.py::_dispatch_reader` / `dispatch_post` | `test_edges_endpoints_use_real_api` and others cover 404s on specific routes. No test for an arbitrary unknown path. |
| `--cors`: `Access-Control-Allow-Origin: *`, OPTIONS -> 204 | `routes.py::handle_options`, `serve/responses.py` (also sends Allow-Methods and Allow-Headers: Content-Type) | `tests/test_serve_auth.py` (`cors=True`, `OPTIONS /save` == 204) |
| Resolve store once, explicit `store_path` + `effective_pythonpath` for reads and writes | `serve/http_server.py::build_handler` (`pythonpath or str(project_root)`) | implicit in the save/graph test (the write is visible on re-read) |
| Per-request exceptions -> JSON 500 | `http_server.py::_dispatch_and_send` (`# pragma: no cover`, untested) | none |
| Parser `--host --port --store --pythonpath --cors` | `parsers/serve.py::add_serve_commands`, wired in `parsers/core.py:29`. Also adds `--token`. | `tests/test_cli_every_command_has_a_handler.py` (in the `-k serve` selection or the full suite) |
| `ServeCLI.run` (ThreadingHTTPServer, KeyboardInterrupt, server_close) | `commands/serve.py::ServeCLI` | no direct test (needs a blocking server). Handler is exercised through `build_handler` |
| Dispatcher registration | `dispatcher.py:43,47` (`"serve": ServeCLI().run`) | `test_cli_every_command_has_a_handler.py` |
| stdlib only, 1 class per file | `http.server`, `json`, `urllib`. `http_server.py` holds one class. | `tests/test_clean_code_rules.py` is included in the `-k serve` run and passed |

## Validation

The task's command is `python -m pytest -q tests -k serve`. The bare command is unusable in this container: there is no `python`, system python3 is 3.11 with no pytest, and `.venv/bin/python` points at a missing host path (`/home/jp/anaconda3`). I ran it with the uv tool interpreter (Python 3.13) and the pure-Python pytest from the repo's `.venv/lib/python3.13/site-packages`:

```
PYTHONPATH=/workspace/sldb/.venv/lib/python3.13/site-packages /home/scion/.local/share/uv/tools/structuredlanguagedb/bin/python -m pytest -q tests -k serve -p no:cacheprovider
```

Result: `106 passed, 1509 deselected, 2 warnings in 71.72s`. Exit code: **0**. Log: `validation.log` in this directory. The first attempt, bare `python -m pytest ...`, exited 127 (`python: command not found`) and is the first line of validation.log.

The `src` path comes from `pyproject.toml` `pythonpath = ["src", "."]`, so the tests ran against the repo source and not the installed copy of sldb. The two warnings are an unknown `asyncio_default_fixture_loop_scope` option and a parametrize deprecation.

## Missing / for supervisor review

1. **`/kgdb/snapshot` does not exist.** It was marked optional in the task file. The function `export_kgdb_semantic_payload` is gone and the capability is served as `GET /semantic-export` via `export_semantic_payload`. It has no HTTP-level test. Decide whether to accept the rename or open a follow-up for a test.
2. The single-document `POST /save` 400 path (the `SystemExit` mapping) and the generic unknown-route 404 have no dedicated test. The batch invalid-payload case is tested (422).
3. The task file's lab-test.sh baselines (sldb 414, kgdb 23, deskops 140) and the docker smoke test refer to the iso-lab host (`/home/jp/...`). They were not run, because they are unavailable here. This run covers only `-k serve`.
4. The original request's `/health` shape (`{"status":"ok"}`) is now a superset, with `findings` and `action` added. `/schema` carries extra fields (`containment`, `references`, `semantics`, `template`, `unavailable`). `/graph` documents carry extra `version` and `provenance`. These are additive and the tests pin them.
5. Auth (`--token`) goes beyond the task file and is covered by `tests/test_serve_auth.py`.
6. `TASK-sldb-serve.md` is untouched. The supervisor does the `git rm` at closeout.

Working tree: only this run directory was added by me. `.deskops.log` and the two desk task files were already modified before I started.
