## REFORMULACION

**Propósito:** que la documentación del árbol del CLI refleje el parser real de sldb y que `selfdoc check` detecte desajustes. **Resultado:** `docs/architecture/current-cli-tree.md` enumera todos los grupos y subcomandos definidos por el parser; `selfdoc check` falla nombrando cada grupo/subcomando del parser ausente en la doc y cada uno documentado que ya no existe. **Repo:** SLDB_1 (`/mnt/ssd/proyectos/SLDB_1`). **Límites:** entra el chequeo en `src/sldb/cli/commands/selfdoc.py`, completar o generar `current-cli-tree.md`, tests en `tests/selfdoc/` y `CHANGELOG`; no entra reescribir descripciones más allá de una línea.

## AMBIGUEDADES

1. «si es generable desde el parser, generarlo y que el chequeo compare con lo generado»: no define cuándo es “generable”, ni formato, ni si el archivo se versiona o se genera en runtime. Obligaría a inventar el mecanismo de generación.
2. «con hallazgos accionables»: no fija formato, severidad, código de salida ni texto de los mensajes. Obligaría a inventar el contrato de salida.
3. «cada uno que la doc nombra y ya no existe»: no indica cómo extraer comandos nombrados de la doc (¿encabezados, bloques de código, prosa?). Obligaría a inventar reglas de parseo del Markdown.
4. «tests en tests/selfdoc/»: no nombra archivo; Validation cita `tests/selfdoc/test_parser.py`, que no figura en `files`. Obligaría a inventar nombre y estructura del test.
5. «borrar una línea de current-cli-tree.md hace fallar selfdoc check nombrando el comando»: no especifica qué línea ni que cualquier línea sea comprobable. Obligaría a inventar el fixture exacto.
6. «unos 45 subcomandos y 11 grupos»: cifras aproximadas; usarlas como meta exacta sería inventar el inventario.

## DRY-RUN

**Lecturas:** `docs/architecture/current-cli-tree.md`, `src/sldb/cli/commands/selfdoc.py`, `src/sldb/cli/parsers/`, `CHANGELOG.md` y `tests/selfdoc/`. **Cambios previstos:** añadir comparación parser↔doc en `selfdoc.py`; completar o generar `current-cli-tree.md`; crear o ajustar test en `tests/selfdoc/test_parser.py`; entrada en `CHANGELOG`. **Dependencias:** construcción de `argparse`, formato actual de `selfdoc check` y extracción de nombres desde la doc. **Validaciones futuras:** los cuatro comandos de Validation (`pytest tests/selfdoc/test_parser.py`, `python -m sldb selfdoc check`, `tests/test_clean_code_rules.py`, `tools/check.sh --fast`). Sin ejecutar.

## FUTURO

Otro nodo ejecutará las validaciones y el commit; un humano decidirá rama, mensaje y merge. La generación efectiva de la doc y el inventario exacto dependen del parser y los materializa el nodo de implementación; la revisión del resultado conjunto corresponde a validación/revisión posterior.
