FALLA

# Testing — specs de docs/architecture/spec2viz con specir catalog build y sync por catálogo

## Veredicto

**FALLA por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1**: la puerta
`identidad` rechaza el directorio versionado `workbench_demo` («directorio versionado sin clasificar en
la raíz»). La regla del rol es explícita: rc distinto de 0 en `check.sh --fast` ⇒ FALLA.

La roja es **preexistente y ajena a este commit**: `workbench_demo` ya está versionado desde `562847e2`
y el commit del ejecutor (`9adfdbce`) no lo toca. Además, el bundle aceptado de esta tarea
(`desk/reviews/.../bundle-1.md`) registra esa puerta como «excepción autorizada f055723d» y dice que no
es falla de esta tarea. **Si el coordinador aplica formalmente esa excepción, el veredicto funcional es
PASA**: no encontré ningún defecto en el trabajo entregado.

## Dónde está el trabajo

- Commit: `9adfdbce11592d7ba51f703c7eb30caa059d8e96`
  («docs: build y sync del catálogo spec2viz sin spec2viz (specir catalog build, sldb notations sync --catalog)»)
  con trailer `Task-Id: task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con`.
- Archivos (3):
  - `contracts/identity.toml`: quita `"spec2viz"` de `[surface].consumers`.
  - `docs/architecture/spec2viz/python-ast.md`: reemplaza las invocaciones `spec2viz diagram ...` por
    `sldb notations from-graph`, `sldb notations validate` y `specir diagram render`; añade la
    instrucción de build/sync del catálogo con `specir catalog build --config ...` y
    `sldb notations sync --catalog ...`.
  - `docs/architecture/code-docstring-indexing-handoff.md`: `spec2viz diagram schema --type component`
    pasa a `specir diagram schema`.

## Comprobaciones funcionales

Validación exacta de la tarea, con el Python del venv del repo:

    .venv/bin/python -m sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml --check
    -> rc 0; Valid: current-components, current-onboarding-surface, current-runtime, current-store-lifecycle

Criterio de grep aceptado en el bundle, sin coincidencias:

    git grep -nE '^[[:space:]]*spec2viz (diagram|catalog|build|render)' -- docs contracts
    -> rc 1 (sin coincidencias)

Las únicas menciones de «spec2viz» que quedan en `docs/architecture/spec2viz` son etiquetas de nodo
(`spec2viz (diagram rendering, catalog build)`, `spec2viz catalog`) y prosa histórica; ninguna es una
invocación de build/sync, y el bundle aceptado las excluye expresamente.

También verifiqué que las invocaciones documentadas existen en las CLIs:
`sldb notations from-graph --help` acepta `--python/--module-prefix/--id/--title/--output`, y
`specir diagram render` acepta `--out/--renderer`; `specir catalog build` acepta `--config/--out`.

## Tests ejecutados

El commit no toca código ni añade archivos `tests/*.py`. Corrí los tests de notaciones más cercanos a la
superficie modificada, de a uno y con `TMPDIR=/tmp`:

| Archivo | Resultado |
|---|---|
| `tests/notations/test_spec_catalog_sync.py` | **8 passed**, rc 0 |
| `tests/notations/test_notations_sync_spec_cli.py` | **4 passed**, rc 0 |

## Gate rápido

`bash tools/check.sh --fast` → **rc 1**. Puertas:

- `núcleo aislado`, `capas`, `ejes`, `superficie`: PASS.
- `identidad`: FAIL por `workbench_demo` (preexistente; excepción registrada en el bundle aceptado).

## Recomendación

No hay cambios funcionales pendientes para el Goal. Para cerrar, el coordinador debe aceptar
explícitamente la excepción de `identidad`/`workbench_demo` ya documentada en el bundle de esta tarea;
bajo la regla literal del prompt de testing, el rc 1 obliga a FALLA.
