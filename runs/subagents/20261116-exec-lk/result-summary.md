# Executor deskops-e-e5a2089b9d3b: resultado

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`
Estado: LISTO (todos los comandos de Validation dan rc 0). Sin commit ni aviso a sldb-ui, por la decisión (5) del coordinador.

## Decisiones del coordinador aplicadas (llegaron a mitad de la ejecución)
1. El parser vive en `sldb.links`: el cambio está en `src/sldb/links/parser.py` y en el módulo nuevo `src/sldb/links/code_mask.py`. `src/sldb/cli/commands/links.py` no se tocó: solo llama a `recover_links`, que a su vez llama a `parse_links`.
2. Reglas de CommonMark: bloque cercado, bloque sin cerrar hasta el fin del archivo, líneas indentadas 4 espacios fuera de una lista, y código en línea con una racha de N backticks que cierra con otra de exactamente N.
3. Solo cambia el scan de enlaces de Markdown. No se tocaron las referencias de modelos, el project graph, `compose` ni el render de predicados.
4. El caso de sldb-ui está reproducido en `test_docs_recover_ignores_links_in_code`.
5. Sin commit y sin avisos.

## Cambios
- `src/sldb/links/code_mask.py` (nuevo): `mask_code(markdown)` cambia por espacios todo el código cercado, indentado y en línea, y conserva los saltos de línea, así que ningún offset se mueve. Funciones internas:
  - `_mask_fences` y `_fence_end`: el bloque abre con 3 o más `` ` `` o `~` y cierra con una línea del mismo carácter de largo igual o mayor. Si no cierra, llega al fin del archivo. Una apertura de backticks cuya línea tiene otro backtick no es un bloque cercado.
  - `_mask_indented` y `_line_kind`: una línea con 4 espacios o un tab de indentación es código si viene después de una línea en blanco o de otra línea de código y no está dentro de una lista. No es código dentro de un ítem de lista ni cuando continúa un párrafo.
  - `_mask_inline`: una racha de N backticks cierra con la siguiente racha de exactamente N en el mismo párrafo (no cruza una línea en blanco). Una racha sin cierre es texto.
- `src/sldb/links/parser.py` / `parse_links`: busca los patrones sobre `mask_code(markdown)`. `LINK_PATTERN` e `INLINE_PREDICATE_LINK_PATTERN` no cambian, y `composer` y `render` los siguen importando.
- `tests/test_links.py`: tres tests nuevos.
  - `test_parse_links_skips_code`: un documento con enlaces reales y ejemplos en bloques de backticks, en un bloque de tildes con un cierre más corto que la apertura, en un bloque indentado, en una lista, en código en línea con uno y con dos backticks, con un backtick suelto y con un bloque sin cerrar.
  - `test_parse_links_fence_rules`: casos borde de las reglas.
  - `test_docs_recover_ignores_links_in_code`: por CLI, `sldb docs recover --format json`. Da rc 0, `unresolved == []` y solo los enlaces reales.
  - Además `from textwrap import dedent` se aplica a la entrada de dos tests existentes (ver Desvíos).
- `CHANGELOG.md`: entrada nueva al principio de 0.1.13.

## Done When
- "Los comandos de Validation pasan con los tests nuevos": se cumple, con rc 0 en los cuatro (ver abajo).
- Con el parser de HEAD, el documento de los tests da `target` 8 veces y con el nuevo ninguna. Lo comprobé importando una copia del parser de HEAD.
- "CHANGELOG": se cumple.
- "commit; aviso a sldb-ui": no se hizo, por la decisión (5) del coordinador. Los hace el coordinador o el integrador.

## Comandos (salida completa en validation.log)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py`: rc 0 (11 passed)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py`: rc 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py`: rc 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast`: rc 0 (TODAS LAS PUERTAS PASAN). Nota: `--fast` omite la puerta "afirmaciones" aunque el brief dice que la incluye.
- Extra: `python3 tools/check_claims.py CHANGELOG.md` dio rc 1, con 3 errores en `CHANGELOG.md:164-165` (`docs/missing`, `docs/ambiguous`, `sldb query`). Son de una entrada anterior que ya está en HEAD. La entrada nueva (línea 7) no da errores.
- No corrí la suite completa ni `sldb stores build --check` (el contrato no los pide).

## Archivos tocados
- `src/sldb/links/parser.py` (modificado)
- `src/sldb/links/code_mask.py` (nuevo)
- `tests/test_links.py` (modificado)
- `CHANGELOG.md` (modificado)
- `runs/subagents/20261116-exec-lk/validation.log` y `result-summary.md` (entrega)

No toqué `.sldb/`, `desk/` ni los cambios ajenos. Las modificaciones de `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml` y `.sldb/store.yaml` ya estaban antes de empezar. Las pruebas temporales quedaron en `/dev/shm/lk-probe`.

## Desvíos y dudas
- **Cambio de comportamiento por la regla de indentación (decisión 2):** un texto indentado 4 espacios después de una línea en blanco ahora es código, y sus enlaces no se cuentan. `test_parse_predicate_links` y `test_parse_mixed_links_with_predicates` escribían su Markdown indentado dentro de `"""..."""` y fallaban (0 enlaces). A su entrada le apliqué `dedent`; las aserciones no cambiaron.
- **Impacto en el repo:** comparé el parser de HEAD con el nuevo sobre los 2354 `.md` versionados. Solo cambian 17, y todo lo que pierden son ejemplos dentro de código (`x`, `...`, `target`, `links`, `spec-001` en el bloque ```` ```markdown ```` de `docs/atoms/predicate-links.atom.md`, `[[task-repro-dos]]` entre backticks). Ninguno gana enlaces.
- **Fuera de alcance:** `sldb docs compose` todavía expande `[[...]]` dentro de bloques de código, porque `composer.py` usa `LINK_PATTERN.sub` sobre el texto completo. La decisión (3) lo deja fuera; si se quiere corregir, es otra tarea.
- La detección de listas es aproximada: un ítem `-`, `*`, `+` o `1.` abre la lista, y la cierra la primera línea no indentada después de una línea en blanco. No sigue los anchos de contenido de CommonMark.
