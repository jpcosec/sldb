## REFORMULACION

Nodo ejecutable, no agregado. **Propósito:** hacer que `_check_store_document`, en `src/sldb/cli/commands/notations_validate.py`, cumpla la regla de código limpio de máximo 10 líneas de lógica, extrayendo funciones auxiliares privadas sin cambiar comportamiento. **Resultado:** el archivo objetivo modificado y los tests indicados en verde. **Repo:** `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`). **Límites:** solo ese archivo y, si aplica, un módulo hermano en la misma carpeta; fuera de alcance cambiar comportamiento, tests o límites.

## AMBIGUEDADES

1. «10 líneas de lógica o menos» y «80 líneas efectivas»: no se define qué cuenta como línea de lógica ni cómo se miden las 80; obligaría a inventar la métrica y el umbral.
2. «Validation» lista «tests/test_clean_code_rules.py tests/notations/test_notations_validate_cli.py», pero «Done When» exige «Los tres archivos de tests pasan»; obligaría a inventar cuál es el tercero, aunque p2 sugiere `test_notations_sync_spec_cli.py`.
3. «commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id»: no fija formato, clave exacta ni valor del trailer, ni identifica el worktree; obligaría a inventarlos.
4. «si el archivo pasa de 80 líneas efectivas»: no da la longitud actual ni el criterio de cómputo; obligaría a inventar si procede el módulo hermano.

## DRY-RUN

**Lecturas:** TaskDoc, `notations_validate.py`, los tests nombrados, `tools/check.sh` y estado de git/worktree. **Cambios previstos:** extraer auxiliares privadas de `_check_store_document`, conservando llamadas y comportamiento; crear módulo hermano solo si se cumple el umbral. **Dependencias:** pytest, `TMPDIR`, bash, git y worktree disponible. **Validaciones futuras:** pytest de los tests listados —y del tercero si se aclara—, `bash tools/check.sh --fast` salvo `identidad` por `workbench_demo`, y commit con rutas y trailer `Task-Id`. Sin ejecutar nada.

## FUTURO

Un ejecutor futuro producirá el diff, los resultados de tests y el commit. Un humano o coordinador decidirá la métrica de líneas, el tercer test, el formato exacto del trailer `Task-Id` y la aceptación de la excepción de `identidad`.
