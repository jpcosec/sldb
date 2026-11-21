FALLA

# Testing — Limpieza de cáscaras vacías de la API y residuos de kgdb

Task: `task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest`
Commit verificado: `5f5eed9d8a1f0073a04f6679853e5bdda68bad6b` — *Remove empty API shells and unused re-exports (api.schema field_descriptor/field_kinds)*, con el trailer `Task-Id` de la tarea.

## Veredicto

**FALLA por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1**:
la puerta `identidad` rechaza el directorio versionado `workbench_demo` («directorio versionado sin
clasificar en la raíz»). La regla del rol de testing es explícita: rc distinto de 0 en
`check.sh --fast` ⇒ FALLA. Las demás puertas (`núcleo aislado`, `capas`, `ejes`, `superficie`)
pasan.

La roja es **preexistente y ajena al commit**: `workbench_demo` ya está versionado en el padre
`b2843fdc` y `contracts/identity.toml` no lo clasifica; el commit del ejecutor no toca ni ese
directorio ni `contracts/identity.toml`. El preflight/bundle de la tarea la registra como excepción
autorizada (`f055723d`). Si el coordinador acepta formalmente esa excepción, **el veredicto funcional
del commit es PASA**: los tests de validación y los de la vecindad de los módulos tocados pasan.

## Alcance verificado

El commit no toca archivos de `tests/` y no existe `tests/test_<modulo>.py` para ninguno de los
módulos de código tocados, así que además de las validaciones de la tarea corrí los tests existentes
que ejercitan esos módulos o sus importadores directos:

| Archivo | Resultado |
|---|---|
| `tests/test_cli_v2.py` (Validation) | **50 passed**, rc 0 |
| `tests/test_store_seams.py` (Validation) | **2 passed**, rc 0 |
| `tests/store/test_graph_backend.py` (Validation) | **9 passed**, rc 0 |
| `tests/test_clean_code_rules.py` (Validation) | **1235 passed**, rc 0 |
| `tests/test_relation_models.py` (usa `sldb.cli.serve.schema.field_descriptors`) | **4 passed**, rc 0 |
| `tests/api/test_api_models.py`, `test_api_model_drafts.py`, `test_model_metadata_drafts.py`, `test_store_ast_unimportable_model.py` (`describe_model`) | **25 passed**, rc 0 |
| `tests/segments/test_field_transclusion_and_diagram_segments.py`, `tests/test_document_segments.py`, `tests/test_extraction_segments.py`, `tests/test_segment_structure.py`, `tests/api/test_field_blocks.py` (`segments`, `payload_values`) | **22 passed**, rc 0 |
| `tests/api/test_machine_editor_schema.py` (schema) | **7 skipped**, rc 0 |
| `tests/security/test_guard_segments.py` | **3 passed**, rc 0 |
| `tests/test_serve.py` | **62 passed, 1 failed** — fallo preexistente ajeno (ver abajo) |

No se corrió la suite completa, según la instrucción del rol.

## Fallo preexistente ajeno a este commit

`tests/test_serve.py::test_batch_save_partial_failure_rolls_back` falla con `HTTPError: HTTP Error
409: Conflict` (esperaba 500). Reproduje el mismo fallo sobre el padre `b2843fdc` en un árbol limpio
(`git archive b2843fdc`), sin los cambios del ejecutor: **1 failed**. No lo introduce este commit.

## Comprobaciones de la limpieza

- `src/sldb/api/schema/field_descriptor.py` y `field_kinds.py` ya no existen; `git grep` no encuentra
  imports suyos en `src/`, `tests/`, `tools/`, `docs/` ni en los entry points.
- Los imports repuntados a `sldb.models.field_schema.{descriptor,kinds}` se ejercitan en los tests de
  `describe_model`, `segments`, `records` y `cli/serve/schema` listados arriba.
- `src/sldb/cli/serve/schema.py` conserva `field_descriptor` y `field_descriptors` (usados por
  `routes.py` y `tests/test_relation_models.py`).
- Los cuatro archivos nombrados en la tarea (`cli/parsers/graph.py`, `cli/commands/help_texts_graph.py`,
  `store/graph/ingest_sldb.py`, `selfdoc/python_source_graph.py`) tienen lógica y usuarios vigentes;
  el ejecutor los conserva y no retira subcomandos del CLI. No encontré una regresión funcional en
  ellos en los tests ejecutados.

## Gate rápido

    PATH=/tmp/ws-venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast   -> rc 1
    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

`/tmp/ws-venv` no existía en el contenedor; lo creé como symlink a `/workspace/sldb/.venv`
(Python 3.13.18). El detalle de comandos y salidas está en `validation.log`.
