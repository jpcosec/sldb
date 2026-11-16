# Resultado — tester deskops-t-addc5ecb8b8c

Tarea: task-la-puerta-de-afirmaciones-vuelve-a-verde-el-changelog-no-nombra-la-ruta-inexistente-docs-architectur
Veredicto: **PASA** (con una nota: Validation 1 falla en el árbol compartido solo por el cambio ajeno en `src/sldb/store/io/lock.py`).

Salida completa: `validation.log` (mismo directorio). Script del caso negativo y la base: `/dev/shm/c7-neg.sh`, HEAD extraído con `git archive` en `/dev/shm/c7-base`.

## Cambio revisado
`git diff -- CHANGELOG.md`: 1 línea (+1/−1), la que empieza con «Las pruebas de spec2viz de notaciones, paletas, vista resuelta y ViewDoc pasan a sldb». Diff por palabra: `` `docs/architecture/vistas.yml` `` → `` `tests/notations/fixtures/docs/architecture/vistas.yml` ``. Nada más. La ruta nueva existe; `docs/architecture/vistas.yml` no.

## Validation
| comando | árbol compartido | HEAD + CHANGELOG nuevo (aislado) | veredicto |
|---|---|---|---|
| `pytest -q tests/test_clean_code_rules.py` | rc=1: 1 failed, 1167 passed. Único fallo: `sldb/store/io/lock.py::_acquire_outer` con 13 líneas de lógica (cambio ajeno sin commitear; no existe en HEAD) | 1168 passed | PASA (el fallo es ajeno, anotado; no se toca) |
| `bash tools/check.sh --fast` | rc=0 | — | PASA |

## Done When
- Comandos de Validation pasan: **PASA** salvo el fallo ajeno de `lock.py` arriba (en HEAD con solo este CHANGELOG, 1168 passed).
- Sin la violación original: **PASA**. `tools/check_claims.py` en HEAD: 12 falsas, incluida `CHANGELOG.md: la ruta docs/architecture/vistas.yml no existe`; con el CHANGELOG nuevo: 11, sin esa. Ninguna nueva.
- `git diff` no toca tests de comportamiento: **PASA**. Lo único del contrato que cambia es `CHANGELOG.md`; el resto de `git status` son cambios ajenos listados en el brief (`apply_batch.py`, `lock.py`, `uv.lock`, `tests/api/test_apply_batch_lock.py`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/*`) más el estado de `.sldb/`/`desk/inbox` de la orquestación.
- CHANGELOG y commit: el arreglo es la línea misma del CHANGELOG (el Scope prohíbe otra línea); el commit es del closeout.

## Caso no cubierto por el ejecutor (en /dev/shm)
- Negativo: en la base HEAD, `check_claims.py` **sí** marca la ruta vieja (12 falsas) → la puerta detecta la regresión; con el CHANGELOG nuevo sobre la misma base baja a 11. Se confirma que el arreglo es la causa y no otro cambio del árbol.
- No quedan menciones de `vistas.yml` sin prefijo en CHANGELOG (única: la nueva).
- `test_clean_code_rules.py` en HEAD + CHANGELOG nuevo: 1168 passed → el CHANGELOG no introduce otra violación.

## Fuera de alcance / notas
1. `check.sh --fast` **omite** la puerta de afirmaciones (`omitidas (--fast): afirmaciones pruebas selfdoc`), así que pasaba también antes del arreglo; el brief y el Rationale suponen lo contrario. Comprobado aparte con `tools/check_claims.py`.
2. Quedan 11 afirmaciones falsas preexistentes en HEAD (no de esta línea): `docs/missing`, `docs/ambiguous`, `sldb query` en CHANGELOG/selectors/references/views, y `sldb models describe` en evidence-model-family. El `check.sh` completo seguirá rojo hasta otra tarea.
3. La frase arreglada queda algo redundante («specs del repo de spec2viz (`tests/notations/fixtures/docs/architecture/vistas.yml` …) se copian … en `tests/notations/fixtures/`»), pero es literalmente lo que pide el Scope.
4. `docs/architecture/spec2viz/` existe pero está vacío; `check_claims` no lo marca.

## Regresiones vecinas
`git diff --name-only` en `src/`: solo `src/sldb/api/documents/apply_batch.py` y `src/sldb/store/io/lock.py`, los dos ajenos (el brief prohíbe revisarlos). El ejecutor no cambió ningún módulo de `src/`, así que no hay tests vecinos que correr por esta tarea. No se corrió ninguna suite completa.
