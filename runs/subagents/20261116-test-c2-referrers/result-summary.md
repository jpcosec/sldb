# Tester deskops-t-0ae57425b2b3: task-clean-code-tras-referrers-…

**Veredicto: PASA** (salida completa en `validation.log`)

## Validation (corrida propia)
| Comando | Resultado | Veredicto |
|---|---|---|
| `pytest -q tests/api/test_referrers.py` | 12 passed, rc=0 | PASA |
| `pytest -q tests/api/test_rewrite_references.py` | 21 passed, rc=0 | PASA |
| `pytest -q tests/test_clean_code_rules.py` | rc=1: 5 failed / 1163 passed | PASA para el alcance (ver abajo) |
| `bash tools/check.sh --fast` | TODAS LAS PUERTAS PASAN, rc=0 | PASA |

`test_clean_code_rules.py`: las 5 fallas son ajenas al contrato. Comparado con HEAD (`git archive HEAD` en `/dev/shm/t0ae57-base`, corrido con el `.venv` del checkout y `PYTHONPATH=src` de la base porque `uv run --extra code` falla en la base: "Extra `code` is not defined"):
- HEAD: 6 fallas = `rewrite_references.py` (15 líneas de lógica), `referrers.py` (97 líneas efectivas) **[las de esta tarea]** + `section_sync.py`, `package_version.py`, `mcp/write/tools.py`, `create_document.py` (preexistentes).
- Actual: desaparecen las 2 de la tarea; quedan las 4 preexistentes + `sldb/store/io/lock.py` (`_acquire_outer` 13 líneas), que **no falla en HEAD** y viene del cambio ajeno sin commitear `src/sldb/store/io/lock.py` (no es de este ejecutor; se anota, no se toca).
- Archivos tocados/nuevos, uno por uno (`-k "referrer or rewrite" -v`): `referrers.py`, `rewrite_references.py`, `referrer_frontmatter.py`, `rewrite_plan.py` PASSED (y el resto de `edges/` también).

## Done When
- Validation pasa (con la salvedad de arriba, que el Scope deja fuera): **PASA**.
- `git diff -- tests` vacío: no se tocó ningún test de comportamiento: **PASA**.
- CHANGELOG: una línea bajo `## 0.1.13 — not released yet` que dice "Arreglo de clean code … sin cambio de comportamiento": **PASA**.
- Commit: no hecho (prohibido al ejecutor; queda para el cierre del coordinador). No evaluable por el tester.

## Scope / archivos
- Cambios del ejecutor: `referrers.py`, `rewrite_references.py`, `CHANGELOG.md` (los del contrato) + nuevos `referrer_frontmatter.py` (pedido explícitamente por el Scope) y `rewrite_plan.py` (el Scope permite "o en un módulo vecino"; justificado porque `rewrite_references.py` pasaba a 98 líneas efectivas). Nada más en `src/` ni `tests/`.
- Reexport: `document_paths` y `frontmatter_lines` se siguen importando desde `sldb.api.edges.referrers` (comprobado). `_planned_payload`/`_planned_text` pasaron a `planned_payload`/`planned_text` en `rewrite_plan.py`; grep en `src/` y `tests/`: nadie los importaba desde `rewrite_references`, así que no se rompe API usada.
- `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml` y `.sldb/core/documents/RunDoc/run-deskops-{e-ee569fb2ae23,t-0ae57425b2b3}.yaml`: registro de los RunDoc del ejecutor y de este tester (despacho de deskops), no código del ejecutor. Se anota por si el cierre debe incluirlos o no.

## Caso propio (no cubierto por el ejecutor)
`/dev/shm/t0ae57-edge/diff_edge.py`: diferencial del mismo mundo de `tests/api/test_referrers.py` corrido con `src` de HEAD y con `src` actual (verificado que la base carga su propio `rewrite_references.py`, con `_planned_text`):
1. `excluded_sources` como **generador de un solo uso** con nombres por `Model:name`, ruta y nombre, con duplicado (card-c dos veces) — `_included_hits` lo consume una sola vez, igual que antes.
2. Fuente inválida con target que no tiene referrers (`card-a2`, `excluded_sources=["nope"]`) → sigue lanzando `SLDBDocumentTargetError` (el orden excluded_paths→find_hits se mantiene).
3. Excluir una nota no trackeada (`notes/d.md`) → `SLDBDocumentTargetError`, igual que HEAD.
4. `excluded_sources=[]` explícito == sin exclusión.
5. Escritura real con exclusión de `Review:r1` + textos/digests resultantes + `referrers` posterior.
6. `frontmatter_lines` en bordes: sin cierre, vacío, binario no UTF-8, inexistente, `---` con espacios, `---` fuera de la primera línea.
Resultado: JSON **idéntico** HEAD vs actual salvo los timestamps `at:` del bloque `sldb` (y los sha256 de archivos que los contienen). Sin cambio de comportamiento.

## Regresiones vecinas
Módulos del contrato cambiados: `sldb.api.edges.referrers`, `sldb.api.edges.rewrite_references` (+ nuevos). Tests que los importan (grep en `tests/`): `tests/api/test_referrers.py` (12 passed), `tests/api/test_rewrite_references.py` (21 passed), `tests/security/test_guard_edges.py` (3 passed), `tests/test_serve.py` (61 passed). Sin fallas. No se corrieron los tests de `apply_batch.py`/`lock.py` (cambios ajenos, fuera de lo que el brief manda revisar).

## Notas
- `uv run --frozen --extra code --extra dev` funcionó en el checkout; solo falló en la base de HEAD (extra `code` no existe en el `pyproject.toml` de HEAD — el árbol tiene `uv.lock` modificado por un cambio ajeno; anotado).
