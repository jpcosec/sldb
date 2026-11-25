## REFORMULACION

Encargo: refactorizar `_check_store_document` en `src/sldb/cli/commands/notations_validate.py` para que `tests/test_clean_code_rules.py` deje de fallar por "14 lines of logic (max 10)", extrayendo auxiliares privadas en el mismo archivo (o módulo hermano si el archivo supera 80 líneas efectivas), sin cambiar comportamiento. Repo: sldb. Resultado observable: los tests de clean code y de la CLI de notations en verde, `tools/check.sh --fast` verde salvo la excepción de identidad, y commit con trailer `Task-Id`. Límites: solo ese archivo y eventual módulo hermano; fuera cambiar comportamiento, tests o límites. Propósito declarado: desbloquear el integrate de sldb y el retiro de spec2viz (IR13).

## AMBIGUEDADES

1. "o en un módulo hermano si el archivo pasa de 80 líneas efectivas": no se define "líneas efectivas" ni se da el conteo actual; obligaría a inventar la métrica y el umbral operativo.
2. "sin cambiar el comportamiento": el input no enumera invariantes (mensajes, códigos de salida); solo se infieren de los tests. Obligaría a inventar el contrato de comportamiento.
3. "Los tres archivos de tests pasan" frente a Validation, que lista solo dos (`tests/test_clean_code_rules.py tests/notations/test_notations_validate_cli.py`); p2 añade `test_notations_sync_spec_cli.py`. Obligaría a inventar cuál es el conjunto exigido.
4. "commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id": no se da el valor/formato del trailer. Obligaría a inventar el identificador.
5. "su intento 2 (5c1740d2, ya en main) funciona": se cita un commit y un `verificacion.log` que no vienen en el bundle; obligaría a asumir que main ya contiene la base correcta.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, `notations_validate.py`, los tests nombrados, `git log`/`show` de 5c1740d2, `tools/check.sh`. Cambios previstos: partir la función en auxiliares privadas, sin tocar tests. Dependencias: worktree, `TMPDIR=/tmp`, pytest, check.sh. Validaciones futuras: comando de Validation, tests de sync spec, check.sh --fast, commit con trailer, `deskops closeout verify`.

## FUTURO

El ejecutor implementa y commitea; deskops/humano confirma la excepción de identidad y el cierre; el nodo de verificación valida el integrate y el retiro de spec2viz.
