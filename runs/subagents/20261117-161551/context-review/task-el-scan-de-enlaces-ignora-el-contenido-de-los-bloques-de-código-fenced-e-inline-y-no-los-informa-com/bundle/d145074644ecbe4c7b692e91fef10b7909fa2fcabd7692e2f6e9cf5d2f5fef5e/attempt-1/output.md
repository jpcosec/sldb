## REFORMULACION
Encargo ejecutable de código en el repo `sldb`: hacer que `sldb links` y la API `parse_links` no cuenten enlaces dentro de código fenced, indentado ni inline. Resultado: `src/sldb/links/parser.py` usa `MarkdownIt("gfm-like")` con `front_matter_plugin`; el recorrido de tokens vive en un módulo nuevo de `sldb.links`; se conservan `LINK_PATTERN`, `INLINE_PREDICATE_LINK_PATTERN`, orden de salida y forma de `ParsedLink`; tests en `tests/test_links.py`; `CHANGELOG.md`. Límites: no HTML `<code>`, no `sldb docs compose`, no nuevas dependencias, no reutilizar el enmascarado anterior. Commit y aviso a `sldb-ui`: coordinador.

## AMBIGUEDADES
1. “va a un módulo nuevo del paquete `sldb.links`”: no se nombra archivo ni API interna; `files` solo lista `parser.py`. Obliga a inventar nombre, ubicación y qué se exporta.
2. “Una sola instancia de MarkdownIt por proceso (como `_PARSER` en `src/sldb/store/section_rebuild.py`)”: no aclara si se reutiliza `_PARSER`, se importa o se crea otra caché en `links`. Obliga a inventar dependencia y punto de caché.
3. “anotarlo en `result-summary.md`”: no indica directorio. Obliga a inventar la ruta de salida.
4. “El orden de salida y la forma de `ParsedLink` no cambian”, junto al test que exige `raw` como `[[a*b*]]`: no se especifica cómo reconstruir el texto fuente saltando `code_inline`. Obliga a inventar la estrategia de mapeo.

## DRY-RUN
Lecturas previstas: `parser.py`, `markdown_ast_handler.py`, `section_rebuild.py`, `parsed_link.py`, `scan_text.py`, `tests/test_links.py`, `pyproject.toml`, `CHANGELOG.md` y los tres `result-summary.md` citados. Cambios previstos: crear el módulo de recorrido, adaptar `parse_links`, ampliar tests y changelog. Dependencias: `markdown-it-py` y `front_matter_plugin` ya presentes; reglas de clean code. Validaciones futuras: los cuatro comandos de Validation, comparación de corpus contra `HEAD` con `git archive HEAD src` y medición antes/después. Nada se ejecuta aquí.

## FUTURO
El ejecutor implementará y medirá; el ritual de testing validará; closeout auditará commit, árbol y evidencia. El coordinador hará el commit y avisará a `sldb-ui`. Un humano debe resolver las ambigüedades 1–4 antes de ejecutar.
