# Resultado — executor deskops-e-26e8a3105895

Tarea: task-la-puerta-de-afirmaciones-vuelve-a-verde-el-changelog-no-nombra-la-ruta-inexistente-docs-architectur

## Cambio
- `CHANGELOG.md`, línea 21 (la que empieza con «Las pruebas de spec2viz de notaciones, paletas, vista resuelta y ViewDoc pasan a sldb»):
  `` `docs/architecture/vistas.yml` `` → `` `tests/notations/fixtures/docs/architecture/vistas.yml` ``.
  Una sola sustitución; ninguna otra línea tocada ni agregada. `docs/architecture/spec2viz/*.yml` se deja: esa ruta existe en el repo (no la marca la puerta).

## Archivos tocados
- `CHANGELOG.md` (1 inserción, 1 borrado). Nada más; ningún test de comportamiento cambia (`git diff --stat` solo muestra CHANGELOG.md entre lo mío).

## Comandos (salida completa en validation.log)
| comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` | 1 (1 failed, 1167 passed) |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` | 0 |
| extra: `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev python3 tools/check_claims.py` | 1 (11 falsas; antes 12) |

## Done When
- Violación de la tarea original: **resuelta**. `check_claims.py` ya no reporta `CHANGELOG.md: la ruta docs/architecture/vistas.yml no existe` (12 → 11 falsas).
- `git diff` no toca tests de comportamiento: cumple.
- CHANGELOG y commit: el arreglo es en sí la línea del CHANGELOG (Scope prohíbe agregar otra); el commit queda para el closeout (prohibido al executor).

## Desvíos / dudas
1. **`tests/test_clean_code_rules.py` falla por un cambio ajeno**: `sldb/store/io/lock.py::_acquire_outer` tiene 13 líneas de lógica (máx 10). Esa función no existe en HEAD (`git show HEAD:src/sldb/store/io/lock.py | grep -c _acquire_outer` = 0); viene del cambio sin commitear ajeno en `src/sldb/store/io/lock.py` (+22/−1). No lo toqué, según el brief. Sin ese cambio ajeno el test pasa (1167 restantes en verde).
2. **`check.sh --fast` omite la puerta de afirmaciones** (`omitidas (--fast): afirmaciones pruebas selfdoc`; tools/check.sh:57-67), así que pasaba aun con la violación. La comprobé directamente con `tools/check_claims.py`. La premisa del Rationale/brief de que `--fast` la incluye no es exacta.
3. **Otras 11 afirmaciones falsas, fuera de alcance, no tocadas**:
   - docs/architecture/evidence-model-family.md: `sldb models` no acepta `describe`
   - docs/architecture/references.md: rutas `docs/missing`, `docs/ambiguous`
   - docs/architecture/selectors.md: rutas `docs/missing`, `docs/ambiguous`; comando `sldb query`
   - docs/architecture/views.md: ruta `docs/missing` (×2)
   - CHANGELOG.md: rutas `docs/missing`, `docs/ambiguous`; comando `sldb query`
