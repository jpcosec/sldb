## REFORMULACION

**Propósito:** que el scan de enlaces de sldb deje de contar enlaces situados dentro de código Markdown (fenced e inline), sustituyendo las reglas propias por markdown-it-py. **Resultado:** `parse_links` (src/sldb/links/parser.py) parsea con `MarkdownIt("gfm-like")` + `front_matter_plugin`; los tokens de código no aportan enlaces; se conservan `LINK_PATTERN` e `INLINE_PREDICATE_LINK_PATTERN`, el orden de salida y la forma de `ParsedLink`. **Repo:** /mnt/ssd/proyectos/SLDB_1. **Límites:** fuera wikilinks en HTML `<code>`, `sldb docs compose`, otros tipos de referencia y dependencias nuevas; commit y aviso a sldb-ui son del coordinador.

## AMBIGUEDADES

1. «La lógica de recorrer tokens va a un módulo nuevo del paquete sldb.links» — no fija nombre, fichero ni API; obliga a inventar dónde vive y su firma.
2. «Una sola instancia de MarkdownIt por proceso (como _PARSER en src/sldb/store/section_rebuild.py)» — no dice en qué módulo se declara ni cómo se inicializa; obliga a inventar ubicación y patrón de caché.
3. «Los tests del intento anterior ... se pueden reutilizar» — permisivo: no aclara si reutilizarlos es obligatorio ni cuáles; obliga a decidir selección y adaptación.
4. «Medir el tiempo de parse_links sobre el corpus antes y después» — sin protocolo (repeticiones, calentamiento, máquina); obliga a inventar el método de medición.
5. «toda diferencia tiene que ser un [[...]] que está dentro de código según el mismo parser» — no define el chequeo automático de ese criterio; obliga a inventar cómo verificarlo.

## DRY-RUN

**Lecturas:** `src/sldb/links/parser.py`, `src/sldb/core/ast/markdown_ast_handler.py`, `src/sldb/store/section_rebuild.py`, `tests/test_links.py`, los tres `result-summary.md` de test-lk, el patch exec-lk-c2, `pyproject.toml` y `CHANGELOG.md`. **Cambios previstos:** módulo nuevo en `sldb.links` con el recorrido de tokens; `parser.py` usando el parser compartido; tests en `tests/test_links.py`; entrada en CHANGELOG. **Dependencias:** markdown-it-py ya declarada; corpus vía `git ls-files '*.md'` y `git archive HEAD src` en /dev/shm. **Validaciones futuras:** los cuatro comandos de Validation, diff de corpus contra HEAD y medición antes/después anotada en result-summary.md. Nada ejecutado.

## FUTURO

El ejecutor produce el diff y `result-summary.md` con los tiempos. El validador ejecuta Validation y el diff de corpus. El coordinador hace commit y avisa a sldb-ui. La decisión de usar markdown-it ya la fijó el supervisor; la aceptación de diferencias del corpus corresponde a quien valide.
