## REFORMULACION

**Propósito:** cerrar huecos de UX del CLI detectados por la matriz de sldb-ui. **Resultado:** `fields update/append` aceptan `--string` (valor literal, sin YAML) y `--format json|text|yaml`; `inbox --show` de nota inexistente escribe error por stderr con exit ≠ 0; `inbox --store` sin `.sldb` falla, lo explica y no escribe nada. **Repo:** `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`). **Límites:** solo parsers/comandos de fields e inbox, su ayuda, tests en `tests/test_cli_v2.py` y `CHANGELOG.md`; fuera: promote del inbox y otros comandos.

## AMBIGUEDADES

1. “`src/sldb/cli/commands/inbox_create.py, inbox_parse.py y los de fields`”: no nombra los archivos de fields; obligaría a inventar rutas/módulos concretos.
2. “`su ayuda`”: no fija texto ni formato de ayuda; obligaría a inventar redacción y ubicación exacta.
3. “`con exit distinto de 0`”: no fija el código; obligaría a elegir 1, 2 u otro.
4. “`no escribe nada`”: no aclara si prohíbe solo archivos o también crear `desk/inbox`; obligaría a definir el alcance de la comprobación previa.
5. “`commitear la referencia CLI que regenere`”: no indica ruta ni artefacto generado por `selfdoc sync`; obligaría a inventar qué archivo queda versionado.
6. “`aviso a sldb-ui`”: no define canal ni formato; obligaría a inventar el mecanismo de notificación.

## DRY-RUN

No es agregado: es una tarea ejecutable (`task.code`). Lecturas previstas: TaskDoc, rituales execution/testing/closeout/phase, `inbox_create.py`, `inbox_parse.py`, `tests/test_cli_v2.py`, `CHANGELOG.md`; habría que localizar los módulos de fields, no nombrados. Cambios previstos: añadir `--string` y `--format` en parsers de fields update/append; validar temprano el `--store` de inbox antes de crear directorios/escribir; enviar error de `--show` inexistente a stderr con exit no cero; actualizar ayuda y tests. Dependencias: parser CLI existente, resolución de campos, contexto de store y `selfdoc`. Validaciones futuras: los cuatro comandos de Validation, `selfdoc check` y `tools/check.sh --fast`; commit atómico con rutas y Task-Id. Nada se ejecuta aquí.

## FUTURO

sldb-ui recibe el aviso y valida la UX. Un humano o deskops actualiza el Board, ejecuta closeout y decide el commit final. `selfdoc sync` produce la referencia CLI regenerada.
