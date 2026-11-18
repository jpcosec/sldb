# main de sldb en verde (job store) — intento 2: `stores build --check --keep DIR` implementado

run_id: exec-deskops-e-e3d8122ff046-a2 · commit: 7cf254f6 (local, sin push) · session: no hay sesión hija (ejecución directa) · session_sha256: n/a

## Decisión implementada (opción 1 del coordinador)
El job store pasa de 2 builds completos a 1: `--check --keep` verifica y deja la copia reconstruida; `selfdoc check` corre dentro de ella.

## Cambios (archivo:línea)
- `src/sldb/cli/parsers/stores.py:90` — argumento `--keep DIR`.
- `src/sldb/cli/commands/stores_build.py:42-44` — `--keep` sin `--check`: "Error: --keep only works with --check", rc 2. Docstring l.7.
- `src/sldb/cli/commands/stores_build_check.py:43-52` (`check_command`: con `--keep` el scratch es DIR y no se borra; el reporte suma `kept`), `:57-64` (`_keep_directory`: DIR nuevo o vacío; si no, error claro y rc 2, sin tocar DIR), `_copy_path` (ruta de la copia = DIR + ruta absoluta del proyecto), `_summary` (línea `kept:`), docstring. El veredicto (`check_build`) no cambió.
- `.github/workflows/ci.yml` (pasos finales del job store): "Rebuild" = `sldb stores build --check --keep "$RUNNER_TEMP/sldb-built"`; "Check generated CLI reference" = `cd "$RUNNER_TEMP/sldb-built$PWD" && sldb selfdoc check` (la copia vive en DIR + ruta absoluta del proyecto; `$PWD` es el checkout `sldb`). Ya no hay `stores build`.
- `tests/store/test_stores_build.py:~440-end` — 7 tests nuevos (escritos primero: 7 failed).
- `CHANGELOG.md` — una viñeta en 0.1.13 sin publicar.
- Regenerado por `sldb selfdoc sync`: `knowledge/commands/cmd-sldb-stores-build.md`, `cmd-sldb-stores-merge-driver.md` (ya estaba desactualizado en HEAD: `required` de `files`), `.sldb/core/documents/CliCommandDoc/cmd-sldb-stores-{build,merge-driver}.yaml`, `.sldb/core/models/CliCommandDoc.yaml`.

## Equivalencia de selfdoc (condición de la decisión)
`test_selfdoc_check_on_the_kept_copy_equals_the_one_after_an_in_place_build[clean|stale-reference]`: proyecto fixture git con docs de referencia CLI de selfdoc; compara (rc, JSON completo de hallazgos) de `selfdoc check` tras `stores build` en sitio vs. dentro de la copia de `--keep`. Igual en los dos casos. Nota: con una referencia desactualizada (default 3→9) selfdoc check da rc 0 + `changed` no vacío + alerta `selfdoc/changed` (así lo define selfdoc, ver tests/selfdoc/test_sync.py); no "falla" con rc≠0, pero ambos caminos dan exactamente lo mismo, y el test exige `changed != []`. Selfdoc no se tocó.

## Salidas
Ver `validation.log`: check.sh --fast rc 0; test_stores_build.py 35 passed; tests/selfdoc/test_sync.py 5 passed, test_preflight.py 4 passed; `selfdoc check` del repo ok.

## Para el supervisor
- No se corrió ningún build del sldb real ni p3. Medición para el integrador (en el host, clones en /dev/shm/sci, sin knowledge/symbols): cronometrar cada paso del job store desde "Build deskops' store" con `/usr/bin/time -f '%e s'`, en el orden de ci.yml; antes con el ci.yml de origin/main; después con el del commit. El "después" ejecuta, en el clon sldb: `sldb stores build --check --keep "$TMP/sldb-built"` y luego `cd "$TMP/sldb-built$PWD" && sldb selfdoc check`. Referencia: `sldb stores build` sin --check, sin knowledge/symbols. Criterio: un solo build y total ≤ 1,2 × referencia.
- Riesgo a vigilar en CI real: `selfdoc check` en la copia importa el parser `sldb.cli...` del sldb instalado (editable del checkout), no el de la copia; son el mismo código. El push de ci.yml requiere scope workflow (integrador).
- No corrí `deskops advance` (la tarea ya está en ritual-testing). Árbol: archivos ajenos sin commitear (.deskops.log, .sldb/store.yaml, store_index.yaml, RunDoc.yaml, sldb/surface, desk/runtimes) intactos y sin stagear.
