## REFORMULACION
**Propósito:** que `docs/architecture/current-cli-tree.md` refleje todo el árbol argparse de sldb y que `sldb selfdoc check` detecte desajustes en ambas direcciones, fallando con rc≠0 y hallazgos accionables.
**Resultado:** chequeo parser-vs-doc; doc completada a mano; tests en `tests/selfdoc/test_parser.py`; CHANGELOG.
**Repo:** SLDB_1. Superficies: `docs/architecture/current-cli-tree.md`, `src/sldb/cli/commands/selfdoc.py`, parser en `src/sldb/cli/parsers/`, `CHANGELOG.md`.
**Límites:** doc escrita a mano (no generada); una línea de descripción por comando; alias registrados válidos sin listar; extracción desde spans de código con forma `sldb <grupo> [<subcomando>]`.

## AMBIGUEDADES
1. «El chequeo extrae de current-cli-tree.md los comandos que aparecen como `sldb <grupo> [<subcomando>]` en spans de código» — la doc real usa un bloque ` ```text ` con árbol (`├── selfdoc` / `└── scan / sync / check`), no spans de esa forma. Inventar notación canónica o reformatear la doc.
2. «si es generable desde el parser, generarlo y que el chequeo compare con lo generado» frente a «la doc sigue escrita a mano, no se genera». Contradicción; inventar cuál prevalece (las Precisiones, presumiblemente).
3. «Cada hallazgo usa el formato de hallazgos que selfdoc check ya emite y hace que el comando salga con rc distinto de 0» — no fija severidad/kind ni cómo afecta a `report.ok`. Inventar nivel (error/warning) y código de hallazgo.
4. «omite unos 45 subcomandos y 11 grupos» — cifras aproximadas y sin lista. Inventar el conjunto exacto y el criterio de conteo.
5. «los alias registrados en el parser cuentan como válidos y no hace falta listarlos» — no aclara si alias singulares, `help`, `legacy` o rutas solo de ayuda entran en la comparación. Inventar su tratamiento.
6. «CHANGELOG» — sin sección ni formato. Inventar entrada.

## DRY-RUN
**Lecturas:** `selfdoc.py`, `selfdoc_context.load_parser`, `selfdoc_inspect`, `sldb/selfdoc/report_findings.py`, `sldb/selfdoc/parser.py`, árbol `src/sldb/cli/parsers/`, `current-cli-tree.md`, `tests/selfdoc/test_parser.py`, `CHANGELOG.md`, `tools/check.sh`.
**Cambios previstos:** extraer rutas del árbol argparse vía `ParserScanner`; parsear spans de la doc; módulo/función de comparación bidireccional; integrar hallazgos en el reporte existente y en `report.ok`; completar la doc; tests (borrar línea / añadir comando inexistente); CHANGELOG.
**Dependencias:** modelo de registros del scanner, `alert_sink`, resolución de `documentation_store`/factory, ruta de salida del chequeo.
**Validaciones futuras:** las cuatro del TaskDoc, sin ejecutarlas aquí.

## FUTURO
Un ejecutor implementa el chequeo y la doc; un humano decide las ambigüedades 1–3 y 5 antes de empezar; el closeout aporta commit y CHANGELOG; el revisor valida el resultado conjunto.
