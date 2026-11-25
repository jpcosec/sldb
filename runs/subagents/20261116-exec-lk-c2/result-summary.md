# Ejecutor deskops-e-a86e76a3783d: corrección 2 (fence en la línea del marcador de lista)

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`.
Parto del diff de los intentos anteriores (parser.py, code_mask.py, tests/test_links.py y CHANGELOG.md) y no lo deshago. Corrijo el borde FALLA de `runs/subagents/20261116-test-lk-c1/result-summary.md` según la Precisión de corrección 2 del Scope. No hay pills atados.

## Cambios
- `src/sldb/links/code_blocks.py` (**nuevo**, sin trackear, 70 líneas): `mask_blocks(markdown)` reemplaza en una sola pasada por líneas a `_mask_fences` y `_mask_indented`. La pasada lleva la pila de columnas de contenido de los ítems de lista abiertos (`st["cols"]`), el tipo de la línea anterior (`prev`) y el fence abierto `(carácter, largo, columna)`. Funciones:
  - `_open_items`: abre los ítems cuyos marcadores empiezan la línea, aunque sean varios (`- 1. ```), y devuelve la columna de contenido. Una línea horizontal (`- - -`, `* * *`) no abre ítems.
  - `_open_fence`: abre un fence a 0-3 columnas del contenido de su contenedor. Eso incluye la línea del marcador (`- ```, `1. ```python`, `* ~~~`), donde la apertura se mide en la columna de contenido del ítem.
  - `_in_fence`: el cierre puede venir indentado hasta esa columna más 3. Una línea no vacía a la izquierda de la columna termina el ítem y el fence con él. Por eso un fence de ítem nunca se traga el resto del archivo, y el cierre indentado nunca se lee como apertura, porque la apertura ya se vio.
  - `_outside` y `_is_code`: código indentado (sin cambios de regla) y CRLF/tabs.
- `src/sldb/links/code_mask.py`: quité `FENCE_OPEN`, `LIST_ITEM`, `_fence_end`, `_mask_fences`, `_open_item`, `_line_kind` y `_mask_indented`. `mask_code` ahora es `_mask_inline(mask_blocks(markdown))`. El código en línea no cambia.
- `tests/test_links.py`: un test por cada caso de la tabla del tester, cada uno contrastado con markdown-it-py commonmark mediante `_assert_targets`. markdown-it-py 4.2.0 está en el `.venv` y no lo agregué como dependencia.
  - `test_parse_links_fence_on_numbered_item_line_keeps_links_after_it`
  - `test_parse_links_fence_on_bullet_item_line_keeps_links_after_it`
  - `test_parse_links_fence_on_item_line_skips_its_content_before_next_item`
  - `test_parse_links_fence_on_item_line_skips_its_content_before_text`
  - Además, `test_parse_links_fence_in_list_item_ends_with_the_item`: un fence sin cerrar dentro de un ítem termina con el ítem; incluye `* ~~~` y un subítem.
- `CHANGELOG.md`: la misma entrada, con estos ajustes:
  - Describe la regla del fence en un ítem y nombra `code_blocks.py` y los tests nuevos.
  - Precisa las cifras del corpus: 1955 `.md` legibles de los 2354 versionados.
- `parser.py` no cambia respecto de c1.

## Done When
- Validation pasa con los tests nuevos: **sí** (`validation.log`):
  - `pytest -q tests/test_links.py`: rc 0, 19 passed
  - `pytest -q tests/test_links_batch_cli.py`: rc 0, 5 passed
  - `pytest -q tests/test_clean_code_rules.py`: rc 0, 1208 passed
  - `bash tools/check.sh --fast`: rc 0, "TODAS LAS PUERTAS PASAN"
  - Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`, y `uv` funcionó.
- Los 5 tests nuevos **fallan** con el `code_mask.py` de c1 (copia en `/dev/shm/lk2/new_mask.py`, inyectada por `/dev/shm/lk3/old_vs_tests.py`) y pasan con el nuevo.
- CHANGELOG: **sí**.
- Commit y aviso a sldb-ui: **no hechos**, por orden del coordinador.
- La suite completa y `sldb stores build --check` quedan delegados al integrador; no los corrí.

## Corpus (`git ls-files '*.md'`: 2354 archivos, 1955 legibles)
Scripts en `/dev/shm/lk3/` (`corpus.py`, `compare.py`). Para HEAD usé `git archive HEAD src` en `/dev/shm/lk3/base`, sobre el mismo árbol de trabajo.
- Contra markdown-it-py commonmark (`[[...]]` fuera de `<code>`): **0 archivos distintos**.
- Contra HEAD: 0 archivos ganan enlaces y 17 pierden. Ningún enlace perdido es real: la intersección con commonmark es 0. Son los mismos 17 de los intentos anteriores.
- El script `cmp.py` de c1 da `corpus files 2355 differ 0` y 0 casos malos.
- Los scripts del tester (`edges.py`, `edges2.py`) dan diffs 0. Las cuatro filas de la tabla coinciden con commonmark.
- `edges3.py` prueba 13 bordes nuevos: marcadores anidados en una línea, línea horizontal, fence en un subítem, `1)` con tildes y cierre corto, línea en blanco dentro del fence de ítem, CRLF, `10.`, fence que interrumpe un ítem perezoso y apertura huérfana de primer nivel. Los 13 son ok.
- La primera corrida de `compare.py` dio 1 diferencia por un dump viejo. Un `.md` ajeno de `desk/tasks/`, que no toqué, cambió entre los dumps. Con los dos dumps hechos de nuevo sobre el mismo árbol, la diferencia es 0. Está en el log.

## Regresiones vecinas
`tests/test_cli_reconciliation.py` y `tests/test_composition_sections.py`: rc 0, 10 passed.

## Archivos tocados
- `src/sldb/links/code_blocks.py` (nuevo)
- `src/sldb/links/code_mask.py`
- `tests/test_links.py`
- `CHANGELOG.md`
- Entrega: `runs/subagents/20261116-exec-lk-c2/{validation.log,result-summary.md}`
- Temporales en `/dev/shm/lk3/`.
- No toqué `desk/`, `.sldb/` ni los cambios ajenos.

## Desvíos y dudas
- **Archivo nuevo `code_blocks.py`.** Para respetar el tope de 80 líneas efectivas, la pasada por líneas vive en un módulo aparte, junto a `code_mask.py` (también nuevo desde el intento 1). El Scope pide "encontrar el parser … y excluir"; los dos módulos son el parser de `sldb.links`.
- **Apertura huérfana de primer nivel.** Una línea `   ```` de primer nivel sin apertura previa sigue abriendo un bloque hasta el fin del archivo, porque así lo hace CommonMark y así lo confirma markdown-it-py (`'   ```\n[[x]]\n'` da `[]` en los dos). La Precisión se cumple en el caso de lista: el cierre indentado de un fence de ítem se reconoce como cierre, y un fence dentro de un ítem termina con el ítem.
- **`tools/check_claims.py CHANGELOG.md`** da rc 1 por `docs/missing` y `docs/ambiguous`. Los dos errores vienen de una entrada anterior que ya está en HEAD, igual que en c1. Esta entrada no da errores, y `check.sh --fast` pasa.
- **Siguen fuera de alcance:**
  - blockquotes (aunque los casos `> ```` de `edges2.py` coinciden)
  - HTML `<code>`
  - `sldb docs compose`
  - un ítem con 5 o más espacios tras el marcador (código indentado en la línea del marcador)
