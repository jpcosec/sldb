# result-summary — deskops-e-2edd3c6307c2

Task: `task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo` (rol sldb-executor). Pills: ninguno.

## Cambios
- `src/sldb/api/matching/atom_keys.py`, función `label_key`: el regex interno pasa de `[^\w\s]+` a exactamente `[\W_]+`; se conserva el resto del pipeline (strip + lower antes, `\s+` → " " y strip después). Docstring ampliado con el porqué. `normalize_key` y `_title_aliases` sin tocar.
- `tests/matching/test_matching_explicit.py`: tests nuevos `test_label_key_underscore_is_a_separator` (`label_key("post_published") == "post published"`) y `test_label_key_matches_normkey` parametrizado con los cuatro pares exactos del Scope.
- `CHANGELOG.md`: una línea en español bajo `## 0.1.13 — not released yet (no tag, not on PyPI)`, al principio de la sección, con el estilo de las vecinas.

## Done When
- `pytest -q tests/matching/` pasa: 31 passed, rc 0 (incluye el test nuevo `post_published`). Ver `validation.log`.
- CHANGELOG.md tiene la entrada.
- Commit: lo hace el coordinador con `deskops closeout commit` (el ejecutor no commitea, por brief).

## Goldens
No hay goldens en `tests/matching/`; ninguno cambió. Usos de `label_key` en src: `spec_view_elements.py` (claves del mapa explícito por label e id), que es justo lo que se corrige.

## Comandos
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/matching/` → rc 0 (31 passed, 1 warning de config de pytest preexistente).

## Archivos tocados
- src/sldb/api/matching/atom_keys.py
- tests/matching/test_matching_explicit.py
- CHANGELOG.md
- runs/subagents/20261116-exec-label-key/validation.log, result-summary.md (entrega)

## Desvíos / dudas
Ninguno. `uv.lock` ya figuraba modificado (cambio ajeno) antes de correr; `uv run --frozen` no lo toca.
