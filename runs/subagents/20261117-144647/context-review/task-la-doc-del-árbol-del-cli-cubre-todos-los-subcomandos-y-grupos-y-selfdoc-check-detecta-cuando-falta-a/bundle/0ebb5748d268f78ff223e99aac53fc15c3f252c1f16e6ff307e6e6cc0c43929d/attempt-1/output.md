REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: que `docs/architecture/current-cli-tree.md` cubra todos los subcomandos y grupos reales y que `sldb selfdoc check` detecte omisiones y comandos obsoletos. Resultado: chequeo accionable que recorre el árbol argparse y lo compara con la doc, doc completa, tests en `tests/selfdoc/` y CHANGELOG. Repo: SLDB_1. Límites: no reescribir descripciones más allá de una línea; superficie acotada a selfdoc, la doc, tests y CHANGELOG.

AMBIGUEDADES

1. «si es generable desde el parser, generarlo y que el chequeo compare con lo generado». Obliga a inventar si la doc pasa a ser artefacto generado, quién la regenera y cómo se versiona.
2. «borrar una línea de current-cli-tree.md hace fallar selfdoc check nombrando el comando». La doc mezcla bloques, grupos y alias en prosa; obliga a inventar qué cuenta como “línea” de comando y cómo tratar alias.
3. «cada uno que la doc nombra y ya no existe». Obliga a inventar si los alias de compatibilidad y comandos legacy cuentan como nombres válidos.
4. «tests en tests/selfdoc/» frente a la validación «tests/selfdoc/test_parser.py». Obliga a decidir si se crea archivo nuevo o se amplía el existente.
5. «No entra: reescribir las descripciones de cada comando más allá de una línea.» Obliga a inventar el formato exacto de esa línea.

DRY-RUN

Lecturas: `selfdoc.py`, `selfdoc_inspect`/`write`, `ParserScanner`, `src/sldb/cli/parsers/`, la doc, tests existentes y CHANGELOG. Cambios previstos: comparador árbol argparse vs nombres de la doc con hallazgos; completar la doc; tests positivos y negativos; CHANGELOG. Dependencias: parser factory, `ParserScanner` y el reporte de hallazgos. Validaciones futuras: los cuatro comandos del TaskDoc y prueba negativa borrando una entrada. Sin ejecutar nada.

FUTURO

Un humano decide las ambigüedades 1–5 antes de ejecutar. Otro nodo implementa y valida; closeout actualiza Board/deskops, commit atómico y CHANGELOG.
