# Executor deskops-e-ee569fb2ae23 — task-clean-code-tras-referrers-referrers-py-bajo-80-líneas-y-rewrite-references-con-10-líneas-de-lógica-c

## Cambios
- `src/sldb/api/edges/referrer_frontmatter.py` (NUEVO, autorizado por Scope): `document_paths`, `frontmatter_lines`, `_in_frontmatter` movidas tal cual desde `referrers.py` (a `_in_frontmatter` solo se le agregó docstring).
- `src/sldb/api/edges/referrers.py`: se quitan esas tres funciones y se importan desde `referrer_frontmatter` (reexport: `from sldb.api.edges.referrers import document_paths, frontmatter_lines` sigue funcionando; `find_hits` las usa). 97 → bajo 80 líneas efectivas.
- `src/sldb/api/edges/rewrite_references.py`: `rewrite_references` partida en pasos con nombre: resolver grafo/target/replacement (inline), `_included_hits` (nueva: resuelve exclusiones, agrupa hits y filtra excluidos, en el mismo orden que antes: `excluded_paths` antes de `find_hits`), planificar (`planned_payload`/`planned_text`), escribir (`_write`, sin cambios). 15 → 10 líneas de lógica.
- `src/sldb/api/edges/rewrite_plan.py` (NUEVO, "módulo vecino" que autoriza el Scope): `Plan`, `TextPlan`, `planned_payload`, `planned_text` (antes `_planned_payload`/`_planned_text`, ahora públicas porque se importan desde `rewrite_references.py`), `_model_type`, `_check`, movidas sin cambio de lógica.
- `CHANGELOG.md`: una línea bajo `## 0.1.13 — not released yet` que dice que es un arreglo de clean code sin cambio de comportamiento.

## Desvío anotado
Al bajar `rewrite_references` a 10 líneas, el archivo `rewrite_references.py` daba 98 líneas efectivas (> 80; antes la violación de función ocultaba la de archivo, el test corta en la primera). Por eso la planificación salió a `rewrite_plan.py`, dentro de lo que el Scope permite ("o en un módulo vecino"). Ningún otro módulo importaba `Plan`, `TextPlan`, `_planned_*` desde `rewrite_references` (grep en src/ y tests/), así que no hay API pública que reexportar.

## Done When
- tests/api/test_referrers.py: 12 passed, rc=0.
- tests/api/test_rewrite_references.py: 21 passed, rc=0.
- tests/test_clean_code_rules.py: rc=1, 5 failed / 1163 passed. **Ninguna falla es de archivos tocados**: `referrers.py` y `rewrite_references.py` (y los dos nuevos) pasan. Las 5 restantes ya fallaban antes de mis cambios (primera corrida, 7 fallas incluidas las 2 de esta tarea) y quedan fuera de Scope:
  - `sldb/mcp/write/tools.py` `propose_changes` 11 líneas
  - `sldb/api/documents/create_document.py` `create_document` 12 líneas
  - `sldb/store/package_version.py` `source_revision` 12 líneas
  - `sldb/store/section_sync.py` `process_model_sections` 13 líneas
  - `sldb/store/io/lock.py` `_acquire_outer` 13 líneas (cambio ajeno sin commitear del árbol compartido)
- bash tools/check.sh --fast: TODAS LAS PUERTAS PASAN, rc=0 (en --fast omite afirmaciones, pruebas y selfdoc).
- `git diff -- tests` vacío: no se tocó ningún test.
- Commit: prohibido por el brief al ejecutor; queda para el cierre del coordinador.

## Comandos (salida completa en validation.log)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py` rc=0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py` rc=0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` rc=1 (solo violaciones ajenas, ver arriba)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` rc=0
- (ruff no está en el entorno `uv run`: "Failed to spawn: ruff"; no se corrió lint aparte, check.sh pasó.)

## Archivos tocados
- src/sldb/api/edges/referrers.py
- src/sldb/api/edges/rewrite_references.py
- src/sldb/api/edges/referrer_frontmatter.py (nuevo)
- src/sldb/api/edges/rewrite_plan.py (nuevo)
- CHANGELOG.md
- runs/subagents/20261116-exec-c2-referrers/{validation.log,result-summary.md}
