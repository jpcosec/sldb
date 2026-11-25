PASA

# Tester deskops-t-3581f6784df9: resultado

Task: `task-propose-changes-rechaza-antes-de-escribir-una-relacion-que-viola-los-tipos-la-cardinalidad-o-la-cond`
Commit revisado: `560e5a1e02fdcadda82224428df3826405bc1045` — `feat: propose_changes rechaza relaciones invalidas antes de escribir`
Archivos del commit: `src/sldb/api/documents/{apply_batch,batch_edges,batch_report}.py`, `src/sldb/mcp/write/{apply,findings,pending,pendings,tools}.py`, `src/sldb/store/edge_index/{doc_kinds,resolve}.py`, `tests/mcp/test_write_tools.py`, `tests/test_mcp_propose_rejects_invalid_edges.py`.

## Veredicto

**PASA.** `propose_changes` y `apply_changes` rechazan con `rejected="edges"` un lote que crea o cambia relaciones que violan los tipos, la cardinalidad o la condición de su `RelationTypeDoc`, antes de escribir, con una entrada por violación (`code`, `message`, `relation {source,type,target}`, `relation_doc`). `apply_batch(dry_run=True)` devuelve las mismas violaciones en `report.rejections`. El lote se simula completo sobre una copia en memoria del índice de aristas, en el orden del lote, y se valida con `validate_edge_index_by_store`, la misma función que usa `check_edges`; no hay un segundo validador. Un lote válido conserva el comportamiento anterior y `pendings` ya no declara la validación de relaciones como faltante.

## Validación ejecutada

Se corrieron de a un archivo, con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-3581f6784df9`:

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q tests/test_mcp_propose_rejects_invalid_edges.py` | 0 | 7 passed |
| `python -m pytest -q tests/mcp/test_write_tools.py` | 0 | 13 passed |
| `python -m pytest -q tests/mcp/test_dry_run.py` | 0 | 1 passed |
| `python -m pytest -q tests/api/test_apply_batch_dry_run.py` | 0 | 4 passed |
| `python -m pytest -q tests/api/test_apply_batch_lock.py` | 0 | 4 passed |
| `python -m pytest -q tests/api/test_api_edges.py` | 0 | 17 passed |
| `python -m pytest -q tests/api/test_composition_edges.py` | 0 | 7 passed |
| `python -m pytest -q tests/api/test_write_paths_validate.py` | 0 | 5 passed |
| `python -m pytest -q tests/api/test_unresolved_references.py` | 0 | 6 passed |
| `python -m pytest -q tests/store/test_resolver.py` | 0 | 7 passed |
| `python -m pytest -q tests/security/test_guard_edges.py` | 0 | 3 passed |
| `python -m pytest -q tests/mcp/test_read_tools.py` | 0 | 14 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No existe `tests/test_batch_edges.py`, `tests/test_apply_batch.py` ni `tests/test_resolve.py`; los tests de módulo tocado existentes son los `tests/api/test_apply_batch_*.py` y `tests/store/test_resolver.py`, corridos arriba. No se corrió la suite completa.

## Cobertura del Done When

- **Tipos:** `test_a_relation_between_models_its_type_does_not_admit_is_refused` — relación cuyo origen no está en `source_types`; rechazo `code="types"` con la relación nombrada y el archivo no escrito.
- **Cardinalidad:** `test_a_relation_over_the_cardinality_is_refused` — dos destinos bajo `one_to_one`; dos entradas `cardinality`.
- **Condición:** `test_a_relation_that_breaks_the_condition_is_refused` — condición que no parsea; `code="condition"`.
- **Sin escritura:** cada `refused` del test nuevo compara `store_fingerprint.store_hash` y el digest del árbol antes/después; iguales en todos los rechazos.
- **Lote entero:** `test_a_valid_relation_and_an_invalid_one_are_refused_together` — relación válida + inválida; se rechaza todo y no se escribe la válida.
- **Lote válido igual que antes:** `test_a_valid_batch_is_proposed_and_applied_as_before` — se propone, se aplica y `edge_findings == []`.
- **Relación que se apoya en otra del mismo lote:** `test_a_relation_may_lean_on_another_of_the_same_batch` — `RelationTypeDoc` + relación en el mismo lote se aceptan.
- **`apply_batch(dry_run=True)`:** `test_apply_batch_dry_run_reports_the_same_rejections` — mismas tuplas `(code, relation)` que `propose_changes`, sin cambiar el hash.
- **pendings:** la entrada `edge_validation_before_write` se eliminó de `PENDING` y ningún pendiente del dry run menciona la validación de aristas.

## Observaciones no bloqueantes

- Al correr la validación agregada del enunciado (`pytest -q tests -k "mcp or apply_batch or check_edges"`) falla `tests/mcp/test_no_writes.py::test_every_read_tool_leaves_the_store_untouched`: su lista `TOOLS` no incluye `anchors_resolve`, herramienta de lectura preexistente. Verifiqué el mismo fallo en un worktree del commit padre `560e5a1e0^`, así que es deuda previa y ajena a este cambio; el resto de esa selección (127) pasa. No afecta el veredicto.
- El commit no incluye `Task-Id`, como pedía el encargo.
- Entorno: `/tmp/ws-venv` no existía en el contenedor; lo creé con `uv venv /tmp/ws-venv --python 3.12` e instalé `sldb[dev,mcp]` en modo editable, porque los tests MCP requieren el extra `mcp` (no instalado en el `.venv` del repo).
