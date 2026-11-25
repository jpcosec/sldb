REFORMULACION
Nodo ejecutable, no agregado. Encargo: cambiar el scan de enlaces de sldb para que `parse_links` deje de interpretar Markdown con reglas propias y derive los enlaces del árbol de tokens de markdown-it-py, con `MarkdownIt("gfm-like")` y `front_matter_plugin`, igual que `markdown_ast_handler.py`. Resultado: `fence`, `code_block` y `code_inline` no aportan enlaces; el resto se recorre en orden, conservando saltos y los dos regex actuales; `ParsedLink` y su orden no cambian; una instancia de parser por proceso; recorrido en módulo nuevo de `sldb.links`; tests, CHANGELOG y `result-summary.md` con tiempos del corpus. Repo: el de las rutas indicadas (`src/sldb/links/parser.py`, etc.). Límites: fuera HTML `<code>`, `sldb docs compose`, otras referencias y dependencias nuevas; commit y aviso a sldb-ui corresponden al coordinador.

AMBIGUEDADES
1. “La lógica de recorrer tokens va a un módulo nuevo del paquete sldb.links”: no fija nombre, API ni ubicación exacta; obligaría a inventar el módulo y su interfaz.
2. “medir el tiempo de parse_links sobre el corpus antes y después”: no define métrica, calentamiento ni repeticiones; obligaría a inventar el protocolo de medición.
3. “Los tests del intento anterior […] se pueden reutilizar; su código de enmascarado propio (code_mask, code_blocks) no se usa”: no delimita qué partes reutilizar; obligaría a inventar el criterio de reutilización.
4. “todos los bordes de los tres informes de tester anteriores”: los informes no están incluidos; sin leerlos habría que inventar casos y expectativas.

DRY-RUN
Lecturas futuras: `parser.py`, `markdown_ast_handler.py`, `section_rebuild.py`, tests, informes y patch citados, `pyproject.toml`, CHANGELOG. Cambios previstos: módulo de recorrido de tokens; `parse_links` usándolo con parser único; tests; CHANGELOG; `result-summary.md`. Dependencias: markdown-it-py ya declarada; corpus mediante `git ls-files '*.md'` y `git archive HEAD src` en `/dev/shm`. Validaciones futuras: los cuatro comandos de Validation, comparación de corpus contra HEAD y medición antes/después. Nada ejecutado.

FUTURO
El coordinador hará commit y avisará a sldb-ui. Un humano o supervisor revisará diffs del corpus, tiempos y aceptación final; otro nodo podría ejecutar validaciones o benchmark, pero no decide alcance.
