# Executor deskops-e-e5a2089b9d3b-a2: resultado (corrección 1)

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`
Estado: **LISTO**, con rc 0 en los cuatro comandos de Validation. Sin commit ni aviso a sldb-ui, como pide la instrucción del coordinador.

Parto del diff del intento 1, que está en el árbol (parser.py, code_mask.py, tests/test_links.py y CHANGELOG). Corrijo las tres FALLAS del tester (`runs/subagents/20261116-test-lk/result-summary.md`).

## Cambios
- `src/sldb/links/code_mask.py`:
  - (a) Listas. `_line_kind` lleva una pila `cols` con las columnas de contenido de los ítems abiertos; la arma `_open_item` según CommonMark: sangría + marcador + 1 a 4 espacios, o + 1 si son 5 o más o si el ítem está vacío. Una línea después de una línea en blanco (o de una línea de código) es código si su sangría es ≥ `cols[-1] + 4`, o ≥ 4 fuera de una lista. Antes, después de una línea en blanco, se cierran los ítems cuya columna supera la sangría. Los tabs se expanden a 4 columnas para medir. Un ítem solo abre si su sangría es menor que base + 4. Esto reemplaza `INDENTED` y el estado `in_list`/`nested` del intento 1.
  - (b) Backticks escapados. `_mask_inline` recorre `INLINE_TOKEN = \\[\s\S]|`+`: un `\x` se consume como escape, así que `` \` `` no abre código y `\\` deja abrir el backtick que sigue. `_inline_close` (nuevo) devuelve `None` para un escape. Dentro de un span, el cierre no mira escapes, como en CommonMark.
  - (c) CRLF. El cierre del fence acepta `[ \t\r]*$` y `BLANK_LINE` es `\n[ \t\r]*\n`. Las líneas con `\r` siguen pasando por `strip()`. Ningún offset se mueve.
  - El archivo tiene 1 módulo, ninguna clase y ninguna función con más de 10 líneas de lógica. `test_clean_code_rules` pasa.
- `tests/test_links.py`: helpers `_commonmark_targets` y `_assert_targets`, y tres tests nuevos, uno por caso:
  - `test_parse_links_indented_code_in_list_item`
  - `test_parse_links_escaped_backtick_is_text`
  - `test_parse_links_crlf_line_ends`

  Cada caso compara con el valor esperado y, si `markdown_it` se puede importar, también con markdown-it-py en modo `commonmark`: los `[[...]]` del HTML fuera de `<code ...>`, con CRLF normalizado. markdown-it-py 4.2.0 ya está en el entorno como dependencia transitiva. **No lo agregué** como dependencia; sin él, se compara solo contra lo esperado.
- `CHANGELOG.md`: completé la entrada del intento 1 (línea 7) con las reglas de lista, de escape y de CRLF, la comparación con markdown-it-py y los tests nuevos.

## Evidencia
- Los tres tests nuevos **fallan** con el `code_mask.py` del intento 1, que inyecté en `parse_links` desde `/dev/shm/lk2/old_mask.py`, y pasan con el nuevo. `test_parse_links_skips_code` y `test_parse_links_fence_rules` pasan con los dos.
- Corpus: `/dev/shm/lk2/cmp.py` compara `parse_links` con markdown-it-py commonmark.
  - En los 13 bordes (los del tester y otros) da 0 diferencias.
  - En los **2355 `.md` versionados** (`git ls-files '*.md'`) da **0 archivos distintos**. La primera corrida dio 3 diferencias, y el error estaba en mi script: el regex no cubría `<code class=...>`.

## Done When
- Validation pasa con los tests nuevos: **sí**, todos con rc 0 (ver `validation.log`).
  - `pytest -q tests/test_links.py`: rc 0, 14 passed
  - `pytest -q tests/test_links_batch_cli.py`: rc 0, 5 passed
  - `pytest -q tests/test_clean_code_rules.py`: rc 0, 1207 passed
  - `bash tools/check.sh --fast`: rc 0 (TODAS LAS PUERTAS PASAN)

  Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`; `uv` funcionó.
- CHANGELOG: **sí**.
- Commit y aviso a sldb-ui: **no hechos**, por orden del coordinador. Los hace el coordinador o el integrador.
- No corrí la suite completa ni `sldb stores build --check`; quedan delegados al integrador.

## Archivos tocados (este intento)
- `src/sldb/links/code_mask.py` (nuevo desde el intento 1, sin trackear)
- `tests/test_links.py`
- `CHANGELOG.md`
- `src/sldb/links/parser.py` no cambia respecto del intento 1.
- Entrega: `runs/subagents/20261116-exec-lk-c1/{validation.log,result-summary.md}`.
- Archivos temporales en `/dev/shm/lk2/`.
- No toqué `.sldb/`, `desk/` ni los cambios ajenos.

## Desvíos y dudas
- `python3 tools/check_claims.py CHANGELOG.md` da rc 1 por 2 errores (`docs/missing`, `docs/ambiguous`). Vienen de una entrada anterior que ya está en HEAD, y el intento 1 ya los había anotado. La entrada de esta task no da errores. `check.sh --fast` no corre esa puerta.
- Siguen fuera de alcance, sin cambios: blockquotes (`>` con código indentado adentro), HTML `<code>` y `sldb docs compose`, que expande `[[...]]` dentro de código.
- Las reglas de cuándo una lista puede interrumpir un párrafo (un ordenado que no empieza en 1, un ítem vacío) quedan aproximadas. En el corpus no producen ninguna diferencia con markdown-it-py.
