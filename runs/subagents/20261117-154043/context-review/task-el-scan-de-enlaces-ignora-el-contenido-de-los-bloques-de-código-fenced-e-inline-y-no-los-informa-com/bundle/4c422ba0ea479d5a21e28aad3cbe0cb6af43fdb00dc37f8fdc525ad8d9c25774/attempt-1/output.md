REFORMULACION
Propósito: corregir el scan de enlaces de SLDB_1 para que no cuente `[[...]]` ni `[pred:: [[...]]]` dentro de código Markdown. Resultado: `parse_links` usa markdown-it-py (`MarkdownIt("gfm-like")` + `front_matter_plugin`) y el árbol de tokens decide qué es código; fence/code_block y code_inline no aportan enlaces; se conservan regex, `ParsedLink` y orden de salida; la lógica de recorrido va a un módulo nuevo de `sldb.links`; parser único por proceso; tests, comparación de corpus contra HEAD, medición antes/después y CHANGELOG. Repo: `/mnt/ssd/proyectos/SLDB_1`; archivos: `src/sldb/links/parser.py`, `tests/test_links.py`, `CHANGELOG.md` y módulo nuevo. Límites: no HTML `<code>`, no `sldb docs compose`, no otros tipos de referencia, no nuevas dependencias; commit y aviso a sldb-ui no son del nodo. Es tarea de código ejecutable, no agregado.

AMBIGUEDADES
1. “La lógica de recorrer tokens va a un módulo nuevo del paquete sldb.links”: no fija nombre ni API; obliga a inventar archivo y contrato interno.
2. “el resto de los hijos se recorre en orden” frente a “El orden de salida y la forma de ParsedLink no cambian”: el orden actual es predicados primero y luego estándar, no necesariamente documental; obliga a inventar si se preserva el orden actual o el del árbol.
3. “No entra: wikilinks dentro de HTML <code>” frente a “html_inline ... se escanea como hoy”: obliga a inventar si `<code>[[x]]</code>` se ignora o se detecta.
4. “todos los bordes de los tres informes de tester anteriores”: los informes y el patch citados no están en el bundle; obliga a inventar los casos exactos si no se leen.

DRY-RUN
Leería `parser.py`, `markdown_ast_handler.py`, `section_rebuild.py`, tests y los informes/patch citados. Crearía el módulo de recorrido, haría que `parse_links` parsee y recorra tokens, y añadiría tests. Dependencias: markdown-it-py/front_matter_plugin ya presentes; regex y `ParsedLink` existentes. Validaría con los cuatro comandos y compararía el corpus `git ls-files '*.md'` contra HEAD en `/dev/shm`, midiendo tiempo. Sin ejecutar.

FUTURO
El coordinador hace commit y avisa a sldb-ui; deskops cierra la tarea. Un humano/supervisor debe resolver las ambigüedades 1–3 antes de ejecutar.
