## REFORMULACION
Encargo ejecutable (no agregado ni paquete): hacer que `docs/architecture/current-cli-tree.md` documente todos los grupos y subcomandos definidos por el parser de `sldb`, y que `sldb selfdoc check` detecte omisiones y entradas obsoletas. Resultado: la doc sigue escrita a mano, con un bloque de árbol ```text; el chequeo extrae rutas por indentación, las compara con argparse sin contar alias ni `help`, emite hallazgos de severidad error con el formato existente y hace `report.ok` falso. Incluye tests en `tests/selfdoc/test_parser.py` (borrar una línea y agregar un comando inexistente), `CHANGELOG.md` y commit. Repo: `sldb`; rutas relevantes: `src/sldb/cli/commands/selfdoc.py`, `src/sldb/cli/parsers/`, `docs/architecture/current-cli-tree.md`. Límites: no generar la doc; no reescribir descripciones más allá de una línea; los alias son válidos y no deben listarse.

## AMBIGUEDADES
1. “El chequeo lee el bloque de árbol ```text de current-cli-tree.md” — no define qué hacer si hay varios bloques ```text o líneas de árbol fuera de bloque; obligaría a inventar la regla de selección.
2. “arma el conjunto de rutas grupo/subcomando por indentación” — no fija profundidades, raíz `sldb` ni subcomandos anidados; obligaría a inventar la gramática del árbol.
3. “sin contar alias ni 'help'” — no aclara si excluye solo el subcomando `help` o también `-h/--help`; obligaría a inventar el criterio.
4. “cada grupo o subcomando del parser que la doc no menciona” frente a “lee el bloque de árbol” — no aclara si menciones en prosa fuera del bloque cuentan; obligaría a inventar el alcance.

## DRY-RUN
Un ejecutor leería `selfdoc.py`, `current-cli-tree.md` y `src/sldb/cli/parsers/`; implementaría el parser del bloque ```text, la comparación con argparse y los hallazgos; actualizaría la doc, añadiría los dos tests y `CHANGELOG.md`. Dependencias: formato de hallazgos y `report.ok` existentes, árbol argparse real, pytest/uv. Validaciones futuras: los cuatro comandos de Validation y la comprobación manual de borrar una línea.

## FUTURO
El ejecutor implementa y ejecuta las validaciones; un humano revisa el diff, `CHANGELOG` y commit. No hay nodos hijos ni decisión humana pendiente antes de implementar.
