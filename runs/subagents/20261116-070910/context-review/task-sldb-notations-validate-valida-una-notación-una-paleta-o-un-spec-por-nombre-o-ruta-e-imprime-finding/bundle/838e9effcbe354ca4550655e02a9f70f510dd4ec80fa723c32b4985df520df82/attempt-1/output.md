## REFORMULACION

**Propósito:** exponer desde la CLI las validaciones de notaciones, paletas (incluido contraste WCAG) y specs que sldb ya implementa, sin reimplementar reglas. **Resultado:** `sldb notations validate <nombre|ruta>` que detecta el tipo de objetivo, ejecuta el validador correspondiente, imprime findings y devuelve exit 0/1 (2 si el nombre es desconocido). **Repo:** sldb; superficie `src/sldb/cli/parsers/notations.py`, `src/sldb/cli/commands/notations.py`, `tests/notations/test_notations_sync_spec_cli.py`, `CHANGELOG.md`. **Límites:** no portar pruebas de spec2viz, no validar catálogos `vistas.yml`, no alterar reglas de validación existentes.

## AMBIGUEDADES

1. «Salida con --format text|json como el resto de la CLI». Los archivos mostrados no tienen `--format`: usan `--json` (sync) o imprimen JSON siempre (list/view/resolve). Obliga a inventar el nombre/forma del flag y su comportamiento por defecto.
2. «Valida el primero y se avisa con una alerta» y «exit 0 si no hay errores y 1 si los hay». No se define si una alerta cuenta como error para el exit code. Obliga a inventar el mapeo severidad→código.
3. «Si el contenido no cuadra con ningún loader, exit 1 con el error del último loader». No se especifica el orden de intentos (paleta/spec/notación). Obliga a inventar la secuencia y, con ella, qué error se reporta.
4. «Con clave "type" de diagrama (la que lee load_spec) es spec». No se enumera qué valores de `type` son válidos. Obliga a inventar el conjunto de valores o a leerlo del loader.
5. «Primero el store (si --store se pasa), después las builtin». No aclara si, sin `--store`, se usa `.` como en el resto de handlers y en qué orden respecto a builtin. Obliga a inventar la precedencia efectiva.
6. «Bajo el encabezado "## 0.1.13 — not released yet"». No dice qué hacer si ese encabezado no existe. Obliga a inventar crear-o-fallar.

## DRY-RUN

**Lecturas:** los cuatro archivos citados, `notation_files.load_notation`, `palette_files.load_palette`, `palette_checks.check_palette`, `wcag_contrast`, `spec_models.load_spec/validate_spec`, `sldb.core.finding` y el comando `stores check` como patrón de `alert_sink`. **Cambios previstos:** `_add_validate` registrado en `add_notations_group`; handler `_validate` en `NotationsCLI` con detección por ruta/nombre, conversión de excepciones y findings, y exit codes; cuatro tests en el archivo indicado; línea en CHANGELOG. **Dependencias:** `builtin_notations()` para el caso builtin; helpers existentes del test o `sldb.api` en `tmp_path` para el store. **Validaciones futuras:** `TMPDIR=/dev/shm pytest -q tests/notations/test_notations_sync_spec_cli.py`, `sldb notations --help` listando `validate`, y `sldb notations validate <builtin>` con exit 0. Nada de esto se ejecuta aquí.

## FUTURO

Deciden fuera de este nodo: el coordinador ejecuta `deskops closeout commit` y no hace push; el ejecutor produce `runs/subagents/<run-dir>/result-summary.md`; el aviso a `<repo>` se resuelve como mensaje o como línea en el informe. Si el gate de ejecución considera las ambigüedades bloqueantes, corresponde crear contexto antes de implementar.
