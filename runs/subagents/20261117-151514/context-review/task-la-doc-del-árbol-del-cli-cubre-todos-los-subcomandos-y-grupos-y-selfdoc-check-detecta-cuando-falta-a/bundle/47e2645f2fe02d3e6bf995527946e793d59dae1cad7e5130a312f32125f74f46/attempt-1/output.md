## REFORMULACION

**Propósito:** que `docs/architecture/current-cli-tree.md` refleje todo el árbol argparse de sldb y que `sldb selfdoc check` detecte divergencias.

**Resultado:** (1) chequeo nuevo en selfdoc que lee el bloque ```text de la doc, arma rutas grupo/subcomando por indentación y las compara con el árbol argparse sin alias ni `help`; cada diferencia es hallazgo severidad error con el formato existente y hace `report.ok` falso (rc≠0); (2) doc completada a mano; (3) tests en `tests/selfdoc/test_parser.py` (borrar línea / añadir comando inexistente, ambos fallan nombrando el comando); CHANGELOG.

**Repo:** `/mnt/ssd/proyectos/SLDB_1`. Superficie: `src/sldb/cli/commands/selfdoc.py`, `src/sldb/cli/selfdoc_inspect.py`, `src/sldb/cli/parsers/`, la doc y los tests.

**Límites:** no generar la doc (prevalece bundle-2); no reescribir descripciones de comandos; no listar alias.

## AMBIGUEDADES

1. **`help` en la doc.** «lo compara con el árbol argparse sin contar alias ni 'help'» frente a `├── help [topic]` en la doc. Obliga a inventar si esa línea debe existir, ignorarse o eliminarse.
2. **Líneas con varios comandos.** «líneas con ├──, └── o │» frente a `├── extract / render / validate`. No dice si se parte por `/` ni cómo derivar rutas anidadas de `│   ├── add / update / …`.
3. **Punto de inserción.** «usa el formato de hallazgos que selfdoc check ya emite» y «hace que report.ok sea falso»: no fija si el chequeo se integra en `inspect_documents`/`report_findings` o en un módulo nuevo.
4. **Alcance del rc.** «selfdoc check falla» vs «report.ok sea falso»: no aclara si `sync`/`python-sync` también deben fallar por esta comprobación.

## DRY-RUN (hipotético, sin ejecutar)

**Lecturas:** `selfdoc.py`, `selfdoc_inspect.py`, `report_findings`, `selfdoc_context.load_parser`, `src/sldb/cli/parsers/`, la doc y `tests/selfdoc/test_parser.py`.

**Cambios previstos:** función que extrae rutas del bloque ```text; recorrido del árbol argparse (excluyendo alias/`help`); conversión de diferencias simétricas en hallazgos error; completar la doc; dos tests con `tmp_path`.

**Dependencias:** formato de hallazgo y `report.ok` existentes; `ParserScanner`/`load_parser`; bloque ```text estable.

**Validaciones futuras:** las cuatro del TaskDoc más el caso manual «borrar una línea hace fallar check nombrando el comando».

## FUTURO

Decide el ejecutor/humano dónde vive el chequeo y si `help` permanece. Closeout aporta CHANGELOG y commit atómico; el coordinador valida el conjunto exacto contra el parser.
