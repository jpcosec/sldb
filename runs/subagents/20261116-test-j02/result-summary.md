# Tester deskops-t-1324db7bbee4: merge de dos .sldb sin detenerse

**Veredicto: PASA.** Hay dos hallazgos menores que no bloquean (ver al final).

La salida completa está en `validation.log`. Los scripts de las pruebas están en `scripts/` y corrieron en `/dev/shm/t02/`. Todos los comandos usaron `TMPDIR=/dev/shm` y `uv run --frozen --extra code --extra dev`. `uv` funcionó sin fallas.

Para las pruebas a mano usé un shim, `/dev/shm/t02/bin/sldb`, que ejecuta `/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/sldb`. Ese binario importa `src/sldb` del checkout. Puse el shim primero en el `PATH`, así que git invoca el driver de ESTE checkout y no la instalación de herramientas (`~/.local/bin/sldb`).

## Validation

| Comando | Resultado |
|---|---|
| pytest tests/store/test_update_fault_tolerance.py | PASA (rc 0, 8 passed) |
| pytest tests/store/test_merkle_shards.py | PASA (rc 0, 6 passed) |
| pytest tests/store/test_stores_build.py | PASA (rc 0, 27 passed) |
| pytest tests/test_clean_code_rules.py (siempre) | PASA (rc 0, 1190 passed) |
| bash tools/check.sh --fast (siempre) | PASA (rc 0, "TODAS LAS PUERTAS PASAN") |

No corrí la suite completa ni `stores build --check`: Validation no los nombra y quedan delegados al integrador.

## Done When, punto por punto

- **Los tres comandos de Validation pasan con los tests nuevos: PASA.** Los 5 tests nuevos existen y pasan: `test_rebuild_index_turns_conflicted_indexes_into_the_clean_ones`, `test_merge_driver_joins_the_include_rules_of_store_yaml`, `test_a_conflicted_derived_index_says_which_command_to_run`, `test_merge_driver_install_is_idempotent` y `test_stores_init_alerts_when_another_branch_already_has_a_store`.
- **Prueba a mano de dos ramas, con y sin driver: PASA, repetida por mí.** Repo de prueba: modelo `Note`, documento base `n0`. `rama-a` agrega `a1` y `a2`, y `rama-b` agrega `b`. Las dos tocan el MISMO modelo con documentos distintos. Corrí 4 combinaciones:
  - **driver + merge:** merge sin conflicto, rc 0. `check` da PASS con la alerta `roster-stale`. Después de `rebuild-index`, `check` da PASS limpio. `include` tiene las 4 rutas y `documents_count: 4`.
  - **driver + rebase:** `Successfully rebased`, rc 0. Después pasa lo mismo que con merge: PASS limpio y las 4 rutas.
  - **sin driver + merge:** quedan 3 archivos en conflicto (UU). `check` sale con rc 1 y el error exacto sobre `store_index.yaml`. `rebuild-index` repara `store.yaml`, `store_index.yaml` y `Note.yaml`, y `check` da PASS.
  - **sin driver + rebase:** mismo resultado que el merge. Además `git add .sldb` y `rebase --continue` terminan con rc 0 y `check` da PASS.
  - En los 4 casos, `diff -r .sldb/core` contra una copia a la que le corrí `stores update && stores build` no muestra diferencias ("SAME").
- **AGENTS.md y docs/versionado-y-colaboracion.md tienen la sección "Merge de .sldb": PASA.** Está en `AGENTS.md:6` y en `docs/versionado-y-colaboracion.md:173`. `check.sh --fast` verifica las afirmaciones y pasa.
- **`sldb stores --help` lista rebuild-index y merge-driver: PASA.** Lo comprobé con el sldb del checkout. `rebuild-index --help` y `merge-driver --help` tienen su description.
- **CHANGELOG y commit:** la entrada de 0.1.13 está, así que el CHANGELOG PASA. El commit lo hace el closeout o el integrador: no es una falla del ejecutor y tampoco es mi rol.
- **Nota respondida a mepu:** es parte del closeout. No la mandó nadie todavía. El ejecutor dejó un texto sugerido.
- **Selfdoc de los comandos nuevos (`knowledge/commands`):** la regenera el integrador. Aclaración 5: no la cuento como falla.

## Aclaraciones del coordinador

1. **Alcance del diff: PASA.** El diff completo pertenece a la tarea. Fuera de los archivos de la tarea solo están cambiados `.sldb/` (RunDoc y los índices del coordinador), `desk/runtimes/`, `.herdr-coordination.md` y `runs/`, que son ajenos. No toqué nada del repo salvo este directorio de evidencia. No hice stash, add ni commit.
2. **Dos ramas con ESTE sldb, mismo modelo y rebase: PASA.** Está descrito arriba. Además probé un caso borde que el ejecutor no cubrió: `rama-a` agrega un MODELO nuevo (`Task`, con un documento) y `rama-b` un documento de `Note`, con `merge.conflictStyle=diff3` (los hunks traen la base `|||||||`).
   - Sin driver: `rebuild-index` une los dos lados, descarta la base diff3 y deja `Note` y `Task` en `store_index.yaml` y en `store.yaml` (models e include).
   - Con driver: el merge es limpio y deja la alerta `root-stale`; `rebuild-index` la limpia.
   - En los dos casos `check` da PASS y el resultado es igual a `update+build`.
3. **Cargas como en HEAD, error exacto y costo del guard: PASA.**
   - **Índices sanos:** cargué `load_store_index` y los 43 `load_models_index` del store real del repo con el árbol de trabajo y con HEAD (`git archive HEAD src`, por `PYTHONPATH`). Los dumps JSON son idénticos según `cmp`.
   - **Error exacto (comparación de strings, EXACT-OK):** lo da en tres casos: `models/Note.yaml` con marcadores, `store_index.yaml` con YAML inválido sin marcadores y `models/Note.yaml` que parsea pero no es un mapping. `docs list` también falla en ese estado. En los tres casos `rebuild-index` repara el archivo (el YAML inválido lo toma de `HEAD`) y `check` da PASS.
   - **Archivo faltante:** el error es el mismo que en HEAD (no hay regresión).
   - **Costo del guard:** agrega una lectura más y un escaneo de líneas, y solo cuando el cache no tiene el índice. En el store real (44 archivos, 36 KiB) cuesta unos 0,83 ms por carga en frío completa, entre 5 y 6 % de 15 a 18 ms. En una carga que sale del cache no corre. No es apreciable.
4. **`--install` idempotente y sin tocar otras líneas: PASA.** La segunda corrida da "0 lines added, 0 keys set". Un `.gitattributes` previo (`*.png binary`, `# keep me`) se conserva y las 3 líneas se agregan al final. El último renglón sin newline final también se conserva y se le agrega el salto.
5. **Selfdoc: queda para el integrador**, como indica la aclaración.

## Regresiones vecinas

Los módulos de `src/` cambiados son `store/io/__init__.py`, `cli/commands/store_init.py`, `cli/commands/stores.py` y `cli/parsers/stores.py`. Con `grep -rl` encontré 44 archivos de `tests/` que los importan. Los corrí uno por uno y **los 44 dan rc 0, sin fallas.** No hizo falta comparar contra HEAD. La lista y las salidas están en `validation.log`.

## Casos negativos extra

- `merge-driver` sobre un archivo ajeno (`docs/n0.md`) sale con rc 1 y deja `%A` intacto.
- Con un número de argumentos que no es 4, sale con rc 2 y muestra el usage.

## Hallazgos menores (no bloquean)

1. **`--install` con un `.gitattributes` que tiene finales CRLF lo reescribe con LF.** `_add_lines` hace `splitlines` y después `"\n".join`, así que `*.png binary\r\n` pasa a `*.png binary\n`. La semántica de git no cambia, pero el diff muestra como modificadas líneas ajenas. Es raro en este repo (Linux).
2. **Una línea equivalente con espacios extra (`.sldb/store.yaml  merge=sldb`) no se reconoce y se agrega otra.** El atributo queda duplicado, lo cual es inocuo.

Por diseño, después de un merge con el driver los hashes quedan viejos (`check` da PASS con una alerta) hasta que se corre `rebuild-index`. Así está documentado en el procedimiento.
