---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-06-14T00:00:02'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T13:10:29'
---

# Add store health-check API

_Describe the incoming message with enough evidence to triage._

Deskops needs to validate `.sldb/` store integrity to implement `deskops doctor` or `deskops health` commands. Currently there is no programmatic way to check whether a store is intact.

## Scope

- `sldb stores check --path <dir>` — validate that `.sldb/` has all required index files, documents index is loadable, models index is loadable, store index is readable
- Exit 0 if healthy, non-zero with specific diagnostics if not
- Optionally expose a Python function: `check_store(path: Path) -> StoreHealth` with structured result
- Clear messages for: missing index, corrupt index, missing document dir, permission error

## Motivation

Deskops health/recovery commands need to detect broken stores without guessing. SLDB is the only authority on what a valid store looks like.

## Existing pills

- `desk/pills/pill-001-sldb-vs-deskops-boundary.md`

## Done When

- `sldb stores check` on a healthy store exits 0 with a summary line
- Missing/corrupt index produces clear diagnostic per broken item
- Python API returns structured health data (not just exit codes)

## Resolución

Resuelto (2026-10-18, sldb-04). `sldb stores check` valida el store y sale 0 con su línea de resumen; cada hallazgo trae su categoría y su `fix`. La API es `sldb.api.check_store(store_path, project_root, pythonpath=None)` (src/sldb/api/stores/store_check.py), que devuelve un dict estructurado: `ok`, `valid`, `damaged`, `reformatted`, `roster_only`, `moved_contracts`, `structural_noise`, `shadowed_models` y `broken_links`. No hay clase `StoreHealth`; el dict cumple el mismo papel.
