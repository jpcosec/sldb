## REFORMULACION
Nodo `task.code` ejecutable (no agregado). Propósito: exponer en la CLI la validación que sldb ya tiene para notaciones, paletas y specs. Resultado: `sldb notations validate <nombre|ruta>` detecta el tipo, ejecuta `load_notation`, `check_palette` o `validate_spec`, imprime findings y sale 0/1/2. Repo: `/mnt/ssd/proyectos/SLDB_1`, tocando `src/sldb/cli/parsers/notations.py`, `src/sldb/cli/commands/notations.py`, `tests/notations/test_notations_sync_spec_cli.py` y `CHANGELOG.md`. Límites: no portar pruebas de spec2viz, no validar `vistas.yml`, no cambiar reglas de validación.

## AMBIGUEDADES
1. “Salida con `--format text|json` como el resto de la CLI” frente a la pill: “La salida usa el mismo flag que sync (`--json`); no se inventa `--format`.” Obliga a inventar/decidir la interfaz real.
2. “si el argumento es un archivo existente, `.json` o `.yml/.yaml`; un YAML con clave `"palette"` o `"colors"`…” solo define heurística para YAML. Obliga a inventar cómo distinguir paleta/spec/notación en JSON.
3. “un nombre se busca entre las notaciones y paletas builtin y del store” no nombra API para listar paletas builtin; solo se cita `builtin_notations()`. Obliga a inventar la búsqueda de paletas builtin.
4. “si el nombre existe en dos tipos, se valida el primero y se avisa con una alerta” no fija el exit code de ese aviso; la pill dice que las alertas no lo cambian. Obliga a conciliar contrato y pill.
5. Validación declarada: solo `pytest -q tests/notations/test_notations_sync_spec_cli.py`; “Done When” exige además `sldb notations --help` y CHANGELOG commiteado. Obliga a decidir si el pytest basta.

## DRY-RUN
Lecturas: parser/comando de notaciones, `stores check` para `Finding`/`alert_sink`, loaders citados, tests existentes y `CHANGELOG.md`. Cambios previstos: `_add_validate` registrado en `add_notations_group`; rama `validate` en `NotationsCLI`; detección ruta/nombre; conversión de errores a findings; tests de los cuatro casos; línea de changelog. Dependencias: `load_notation`, `load_palette`/`check_palette`, `load_spec`/`validate_spec`, `Finding`, fixtures de `tmp_path`. Validaciones futuras: ejecutar el pytest indicado, comprobar ayuda de CLI, probar los cuatro exit codes y revisar árbol limpio; sin ejecutar ahora.

## FUTURO
El ejecutor produce `runs/subagents/<run-dir>/result-summary.md`; el coordinador hace `deskops closeout commit`, no hay push; el aviso a repo depende de `deskops message send` o queda como línea en el informe. La validación de catálogos y el port de pruebas de spec2viz son tareas aparte.
