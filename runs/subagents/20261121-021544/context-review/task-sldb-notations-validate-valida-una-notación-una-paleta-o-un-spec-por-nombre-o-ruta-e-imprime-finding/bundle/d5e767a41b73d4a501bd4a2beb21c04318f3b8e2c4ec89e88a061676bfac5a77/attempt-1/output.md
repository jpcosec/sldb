## REFORMULACION

Nodo ejecutable, no agregado. Propósito: añadir `sldb notations validate <nombre|ruta>` en el repo `sldb` para detectar si el objetivo es notación, paleta o spec, reutilizar los validadores existentes y emitir `Finding`s. Resultado: subcomando registrado en `src/sldb/cli/parsers/notations.py`, handler en `src/sldb/cli/commands/notations.py`, salida texto/`--json`, exit 0/1/2 según contrato, tests, CHANGELOG y referencia CLI regenerada. Límites: no portar pruebas de spec2viz, no validar catálogos `vistas.yml`, no cambiar reglas de validación.

## AMBIGUEDADES

1. Ubicación/alcance de tests: el Scope dice “Tests en tests/notations/test_notations_sync_spec_cli.py”, pero Implementation Path pide “tests nuevos en tests/notations/test_notations_validate_cli.py” y Validation solo ejecuta el primero. Obliga a inventar dónde crear los tests y qué archivo valida el cierre.
2. Número de casos: Done When exige “los cuatro casos de test pasan”, mientras Implementation Path enumera más casos (“válidos”, “inválido de cada tipo”, “--json”, “nombre en dos tipos”). Obliga a inventar el conjunto mínimo de tests.
3. Store por defecto: Scope dice “un nombre se busca entre las notaciones y paletas builtin y del store”, pero la precisión dice “primero el store (si --store se pasa), después las builtin” y el pill: “Sin --store se usan solo las builtin”. Obliga a inventar si sin `--store` se consulta `.` o solo builtins.
4. Validez de notación: se indica “load_notation para notaciones; cada excepción o problema es un finding”, pero también “uno inválido de cada tipo”. Obliga a inventar qué convierte una notación en inválida y qué mensaje/código produce.
5. Detección por `type`: “clave 'type' de diagrama (la que lee load_spec)” no define si cualquier `type` basta o solo valores aceptados. Obliga a inventar la regla o depender de leer `load_spec`.

## DRY-RUN

Lecturas: Board, rituales execution/testing/closeout, pill, átomo, task doc, parsers/commands de notations, loaders de notación/paleta/spec, `sldb.core.finding`, CLI/alert_sink, tests citados, CHANGELOG y git HEAD. Cambios previstos: `_add_validate`, registro en `add_notations_group`, handler de detección/carga/validación, findings texto/JSON, tests, entrada CHANGELOG y selfdoc. Dependencias: loaders existentes, `check_palette`, `load_spec`/`validate_spec`, `builtin_notations`/`builtin_palettes`, store y argparse. Validaciones futuras: pytest del archivo que se resuelva, `sldb notations --help`, caso builtin con exit 0, `selfdoc check`, `tools/check.sh --fast`.

## FUTURO

El coordinador o un nodo de corrección debe resolver la contradicción de tests, fijar el store por defecto y aclarar la validez de notaciones. El ejecutor implementará, ejecutará pruebas y commiteará; el coordinador hará closeout y avisará al repo.
