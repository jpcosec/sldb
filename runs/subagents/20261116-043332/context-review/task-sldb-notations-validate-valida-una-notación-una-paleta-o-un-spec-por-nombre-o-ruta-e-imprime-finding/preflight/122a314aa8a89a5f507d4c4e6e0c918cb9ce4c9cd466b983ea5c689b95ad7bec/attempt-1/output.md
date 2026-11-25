## REFORMULACION

Propósito: exponer en la CLI de sldb la validación que ya existe internamente, para que spec2viz pueda delegar en `sldb` la validación de notaciones, paletas (incluido contraste WCAG) y specs. Resultado: un subcomando `sldb notations validate <nombre|ruta>` que detecta el tipo de objetivo, ejecuta el validador correspondiente y emite findings en el formato de findings de sldb, con `--format text|json`, exit 0 sin errores, 1 con errores y 2 si el nombre es desconocido. Repo: `SLDB_1`, tocando `src/sldb/cli/parsers/notations.py`, `src/sldb/cli/commands/notations.py`, `tests/notations/test_notations_sync_spec_cli.py` y `CHANGELOG.md`. Límites: no portar pruebas de spec2viz, no validar catálogos `vistas.yml`, no cambiar reglas de validación; reutilizar `load_notation`, `load_palette`/`check_palette`, `load_spec`/`validate_spec`.

## AMBIGUEDADES

1. "una ruta existente se carga por extensión y contenido" — no se define qué extensión ni qué prioridad si el contenido contradice la extensión; obligaría a inventar el algoritmo de detección.
2. "un nombre se busca entre las notaciones y paletas builtin y del store" — no fija orden de precedencia ni qué ocurre si el nombre existe en ambos; obligaría a inventar la política de colisión.
3. "devuelve findings en el formato de findings de sldb" — remite a "buscar el tipo Finding que usan otros comandos"; obligaría a inventar campos y serialización si no se localiza uno canónico.
4. "una notación builtin válida (exit 0)" — no nombra la notación concreta; obligaría a elegir una y asumir que sigue siendo válida.
5. Exit 2 "y mensaje unknown notation, palette or spec: <nombre>" — no aclara si aplica también a rutas inexistentes; obligaría a decidir ese caso.

## DRY-RUN

Lecturas: parsers/commands de notations, `notation_files.py`, `palette_files.py`, `palette_checks.py`, `wcag_contrast.py`, `spec_models.py`, un comando con `--format`/`--store` como `stores check`, y el test existente. Cambios previstos: `_add_validate` + registro en `add_notations_group`; comando con detección de tipo, conversión de excepciones/resultados a findings y salida text/json; cuatro tests con `tmp_path`; entrada de CHANGELOG. Dependencias: tipos Finding y patrones de exit code ya existentes. Validación futura: `TMPDIR=/dev/shm pytest -q tests/notations/test_notations_sync_spec_cli.py`, `sldb notations --help` y `sldb notations validate default`.

## FUTURO

Un nodo ejecutor implementará código y tests; un humano decidirá nombres concretos de fixtures, formato exacto de findings si hay que fijarlo y revisión del CHANGELOG.
