## REFORMULACION

**Propósito:** que un documento con frontmatter existente, al que le falta una clave nueva, tome el default del modelo al re-extraer y no quede en `store/doc-invalid`.

**Resultado:** test `tests/test_campo_con_default.py` en verde y arreglo en la extracción que aplique el default de un campo ausente.

**Repo:** `SLDB_1/sldb` (workspace sldb). Nodo ejecutable (`task_type: task.code`), no agregado; `current_node: ritual-execution`.

**Límites:** solo extracción + test. Fuera: fields update (tarea hermana `task-fields-update-...`) y migraciones sin default. Caso origen: nota 20261121-204955.

## AMBIGUEDADES

1. «se agrega al modelo el campo espera_segundos: int = 4 **con su marcador rev**» — no se define qué es el marcador `rev` ni su API; obligaría a inventar el mecanismo.
2. «Un StructuredNLDoc **minimo registrado en un store temporal**» — sin módulo, imports ni helper; obligaría a inventar dónde y cómo se registra.
3. «Arreglo **en la extraccion**» — no nombra archivo, módulo ni función; obligaría a inventar el punto exacto del cambio.
4. Título: «**fields update los puede reparar**» frente a Scope: «**Fuera: fields update**» y rationale: «fields update ... **falla igual**»; obligaría a decidir si el arreglo toca o no fields update.
5. «**Correr solo ese test**» frente a ritual-testing («then the full suite when shared behavior changed»); obligaría a decidir el alcance de validación.

## DRY-RUN

- **Lecturas:** Board, este TaskDoc, rituales execution/testing/closeout, nota de inbox referenciada, código de extracción y de registro de `StructuredNLDoc`, `conftest`/tests existentes, tarea hermana si existe.
- **Cambios previstos:** crear `tests/test_campo_con_default.py`; modificar la extracción para aplicar defaults de campos ausentes.
- **Dependencias:** pytest del venv, store temporal, marcador `rev`.
- **Validaciones futuras:** el comando pytest indicado con `TMPDIR=/mnt/ssd/tmp/sldb1`; después, suite/`tools/check.sh` según rituales. Sin ejecutar.

## FUTURO

La tarea hermana produce el arreglo de `fields update`; closeout hace el commit atómico y retira del Board; un humano decide si se corre la suite completa y resuelve la contradicción título/scope.
