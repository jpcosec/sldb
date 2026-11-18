# BLOQUEADO — main de sldb en verde (job store): hace falta una decisión de diseño (p6)

No se commiteó código. Árbol sin cambios míos (solo evidencia en este run dir).

## (a) Causa confirmada en el código
- `.github/workflows/ci.yml:65-67` paso "Rebuild sldb's store": `sldb stores build --check`; `ci.yml:68-71` paso "Check generated CLI reference": `sldb stores build && sldb selfdoc check`.
- `src/sldb/cli/commands/stores_build.py:41-44`: `--check` delega en `check_command`. `stores_build_check.py:38-41`: crea un `TemporaryDirectory` y lo borra al terminar; `:45-56` `check_build`: copia las fuentes (`_copy_sources`, :90-97, sin `.sldb/core/`, `.sldb_cache/` ni los `derived`), corre `build_store` completo (con generadores, incl. `selfdoc python-sync`) EN LA COPIA (:51), `stores check` sobre la copia (:52) y compara filas rastreadas (:53, `_differences` :109-115). No escribe nada en el store local.
- Luego `stores build` (sin --check, `stores_build.py:45-46`) hace el segundo build completo, en sitio. Confirmado: 2 builds completos en el job; la hipótesis del integrador se cumple.

## (b) Por qué la opción (a) de p2 NO es equivalente
`--check` verifica (stores_build_check.py:53-56): (1) `stores check` de la copia == 0; (2) `undeclared` vacío; (3) `missing` vacío; (4) sin "only local": filas rastreadas por el store local (menos las de `derived`) que las fuentes NO reconstruyen; además alertas (only rebuilt, link ausente, unread_declared).
Un build en sitio + `git diff --exit-code`:
- (2) y (3): sí, el rc de `stores build` es 1 con undeclared/missing/include_conflicts (stores_build.py:48).
- (1): se cubre añadiendo `sldb stores check`.
- (4): NO. `build_store._built` (api/stores/build_store.py:49-57) solo añade/actualiza filas (`apply_includes`); no elimina las filas locales que ya no salen de las fuentes, y `.sldb/core/` está versionado, así que el build en sitio parte de ellas. Una fila obsoleta commiteada pasaría en verde, y `git diff` no la ve. La copia scratch las excluye justo para detectarlo. Por la resolución (2) no puedo mostrar equivalencia lista por lista → (b).

## Por qué (b) requiere decisión de diseño
Hay que "verificar y dejar el store escrito" en un solo build, pero el build de `--check` vive en una copia sin `.sldb/core/` y bajo una ruta absoluta de scratch. Opciones:
1. `--check --keep[=DIR]`: conserva la copia scratch y el paso siguiente corre `sldb selfdoc check --store <copia>/.sldb` con cwd en la copia. Riesgo: `selfdoc check` usa `documentation_store`/`find_local_store` (cli/commands/selfdoc.py:28,36,70-71) y el parser/`--pythonpath` relativos a la raíz del proyecto; habría que comprobar que da el mismo resultado desde la copia (la copia es un checkout limpio, así que debería). Cambio mínimo; el job store pasa a: `stores build --check --keep` + `selfdoc check` sobre la copia. 1 build.
2. `--check --write`: tras un check OK, mover/copiar el `.sldb` de la copia al store local. Cambia la semántica de lo que se escribe (el local conserva `.sldb/core/` versionado y rutas relativas; la copia no lo tiene) → riesgo de reescribir historia versionada. No recomendada.
3. Hacer que `selfdoc check` no necesite el store construido (comparar contra los .md versionados, `knowledge/`). Cambia selfdoc; fuera del alcance indicado.
4. (c) cachear `knowledge/symbols`: reduce ~110→~55 min por build pero con 2 builds en CI sigue sin holgura; complemento, no solución.

Recomendación: opción 1, con test en `tests/store/test_stores_build.py` (el check conservado deja un store en el que `stores check` y `selfdoc check` pasan; falla antes porque la opción no existe). Necesito que el supervisor confirme 1 (o elija otra) antes de implementar.

## Validación / medición
No se corrió nada de p3 (resolución 1). Comando para el integrador cuando haya cambio: ver p3 con `/usr/bin/time -f '%e s'` por cada paso de ci.yml desde "Build deskops' store" y un `sldb stores build` de referencia sin knowledge/symbols.

Nota: por error lancé `deskops advance task` al escribir este informe, aunque la tarea está BLOQUEADA; quedó en segundo plano sin terminar (>120 s, posiblemente por hooks). El supervisor debe revisar el estado de la tarea.
