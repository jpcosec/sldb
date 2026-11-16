# Resultado — tester deskops-t-7ff569d1fb68

Task: `task-clean-code-tras-el-gancho-de-sldb-mcp-propose-changes-con-10-líneas-de-lógica-como-máximo`. Pills: ninguno.
Veredicto: **PASA**. Las 2 fallas que quedan en test_clean_code_rules están en archivos que este cambio no toca: una ya fallaba en HEAD y la otra viene de un cambio ajeno.

## Cambio revisado
- `src/sldb/mcp/write/tools.py`: el sellado (huella, `batch_change`, nivel, `Proposal` sellado) pasa a `WriteTools._seal(changes)`. `propose_changes` sigue en el mismo orden: `_require`, `_check_path`, validadores de dominio y rechazo, y después el sellado y el dry run. La API pública queda igual.
- `CHANGELOG.md`: una línea bajo `## 0.1.13 — not released yet` que lo declara arreglo de clean code.

## Validation (corrida propia, salida completa en validation.log)
| Comando | rc | Veredicto |
|---|---|---|
| uvx … pytest -q tests/mcp/test_extension.py | 0 (8 passed) | PASA |
| uvx … pytest -q tests/mcp/test_write_tools.py | 0 (8 passed, 1 xfailed) | PASA |
| uv run … pytest -q tests/test_clean_code_rules.py | 1 (2 failed, 1166 passed) | PASA para el alcance (ver abajo) |
| uv run … bash tools/check.sh --fast | 0 (TODAS LAS PUERTAS PASAN) | PASA |

test_clean_code_rules:
- `test_clean_code_rules[sldb/mcp/write/tools.py]` **pasa**. En la base HEAD (`git archive HEAD` en /dev/shm/c5-head) fallaba: `propose_changes` tenía 11 líneas de lógica.
- Sigue fallando `sldb/store/package_version.py::source_revision` (12 líneas). **También falla en HEAD**, así que no es una regresión de esta tarea. Hace falta una tarea de clean code propia.
- Sigue fallando `sldb/store/io/lock.py::_acquire_outer` (13 líneas). Viene del **cambio ajeno sin commitear** `src/sldb/store/io/lock.py`; en HEAD no falla. No lo revisé ni lo toqué.
- No hay violaciones en los archivos tocados (`tools.py`, `CHANGELOG.md`).

## Done When
- Comandos de Validation: PASA. Los únicos rc≠0 son los dos de arriba, fuera del alcance (Scope: "se anotan y no se tocan").
- No se tocaron tests de comportamiento: PASA. `git diff --stat -- tests/` sale vacío; `tests/api/test_apply_batch_lock.py` es ajeno y está sin trackear.
- CHANGELOG: PASA (la línea está bajo 0.1.13).
- Commit: todavía no hay. El brief lo prohíbe y queda para el closeout del coordinador.

## Caso no cubierto por el ejecutor
Escribí `/dev/shm/c5-edge/edge.py`. Carga `propose_changes` de HEAD y del árbol y les pone las mismas dependencias falsas: huella, `batch_change`, `model_level`, sealer y `_dry_run`. Compara el resultado y la secuencia de llamadas en 4 casos:
- rechazo de dominio: no sella ni pide huella (`calls=[]`);
- solo avisos (warning): se adjuntan `domain_alerts`;
- lista vacía: `ValueError` en las dos versiones;
- lote válido con niveles mezclados: el nivel máximo es 3, el sello y el orden `fp → bc… → seal` son los mismos.

Resultado: 4/4 IGUAL, rc=0. No cambia el comportamiento.

## Regresiones vecinas
Los módulos de `src/` cambiados por la tarea son solo `sldb/mcp/write/tools.py`; `apply_batch.py` y `lock.py` son ajenos. Los tests lo ejercen a través del servidor MCP. Los busqué con grep y corrí cada archivo por separado:
- test_cli_mcp (3 passed)
- test_mutability (7 passed)
- test_no_writes (2 passed)
- test_dry_run (1 passed)
- test_extension y test_write_tools, que ya estaban en Validation

Ninguna falla.

## Fuera del contrato
`git diff --name-only` muestra, además de los dos archivos del contrato, solo cambios que ya estaban en el árbol antes de la tarea: los ajenos listados, más `.sldb/…` y `desk/tasks/task-código-readers…`, que ya estaban en el snapshot inicial. El ejecutor no tocó nada más.

## Nota de entorno
En la base HEAD, `uv run --frozen --extra code` falla con "Extra `code` is not defined". Ahí corrí el test con el `.venv` del checkout.
