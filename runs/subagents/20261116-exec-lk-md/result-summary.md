# Ejecutor deskops-e-2793fe94705d: resultado

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com` (contrato reescrito: extraer los enlaces del árbol de markdown-it). Pills: ninguno. Seguí la disposición de `review-...-bundle-3`: el orden de salida es el de hoy, `<code>` HTML se sigue detectando y el tiempo se da como mediana de 3 corridas en frío.

## Cambios
- **`src/sldb/links/scan_text.py` (nuevo, autorizado por Scope (3)).** `scannable_text(markdown)` devuelve el texto del documento sin su código.
  - `_parser()` arma una sola instancia por proceso, cacheada en `_PARSER` como en `store/section_rebuild.py`. Es el `md` de `sldb.core.ast.markdown_ast_handler.MarkdownASTHandler` ("gfm-like" con `front_matter_plugin`) con `text_join` y `linkify` apagados (ver Desvíos).
  - `_block_text`: un `inline` aporta sus hijos; `front_matter` y `html_block` aportan su contenido crudo; `fence`, `code_block` y los open/close no aportan nada. Los bloques se unen con `\n`.
  - `_inline_piece` / `_inline_text`: `code_inline` no aporta texto (deja `CODE_GAP` = `\x00]\x00`, que corta un `[[...]]` que cruza el código y no puede cerrar uno); `softbreak` y `hardbreak` aportan `\n`; `text_special` (escapes y entidades), em, strong y s aportan su `markup` (el texto fuente); un token con hijos (image) se recorre; el resto aporta su `content` (text, html_inline).
- **`src/sldb/links/parser.py`, `parse_links`.** Corre `LINK_PATTERN` e `INLINE_PREDICATE_LINK_PATTERN` (sin cambios) sobre `scannable_text(markdown)`. El orden (predicados y después estándar, cada grupo en orden del documento) y `ParsedLink` no cambian. Si el texto no tiene `[[`, devuelve `[]` sin parsear: los dos patrones lo necesitan.
- **`tests/test_links.py`.**
  - Se reusan los tests del patch `executor-diff-lk-c2.patch`: los dos `dedent`, `CODE_EXAMPLES_DOC` (enlaces reales y ejemplos en código cercado, indentado y en línea), `test_parse_links_skips_code`, `test_parse_links_fence_rules`, `test_docs_recover_ignores_links_in_code`, código indentado en ítem, backtick escapado, CRLF y los cinco de fence en el marcador de lista. `_commonmark_targets` ya no admite que markdown-it falte (es dependencia directa), así que cada `_assert_targets` compara siempre con el HTML de markdown-it en modo `commonmark`.
  - Tests nuevos:
    - `test_parse_links_code_span_stays_in_its_block`: las 6 filas de test-lk-c2.
    - `test_parse_links_keeps_the_source_text_and_the_order`: front matter, encabezado, tabla, html_block, `<code>` HTML, énfasis dentro de un destino, escape `\_` y predicado primero.
    - `test_parse_links_code_cut_inside_brackets_is_not_a_link`.
- **`CHANGELOG.md`.** Entrada al principio de 0.1.13.
- **`contracts/layers.toml`: desvío, ver abajo.**

## Desvíos y dudas
1. **`contracts/layers.toml` (fuera de los archivos del contrato).** La puerta `ejes` de `check.sh --fast` falla con cualquiera de las dos formas de usar markdown-it desde `sldb.links`:
   - **Importar `markdown_it` directo:** da `ERROR links/scan_text.py: el eje enlaces usa markdown-it-py, declarada de op_documentos, superficie`. La dependencia está confinada a esos dos ejes.
   - **Pedir el parser a `MarkdownASTHandler`, del eje superficie (lo que elegí):** da `la unidad nucleo declara ... necesitada por 58; el código dice 59` y `la unidad enlaces declara necesitar 4; el código dice 5`.

   Elegí la segunda porque es la dirección que el propio contrato de capas pide para `section_rebuild` ("debería pedírselo al analizador"). Hice el ajuste mecánico de las dos cifras (`needs = 5` en el non_unit `enlaces`, `needed_by = 59` en `nucleo`), con notas "medido 2026-11-17", como hacen los commits anteriores. Si el coordinador prefiere no tocar ese archivo, la alternativa es la primera forma, con `external = ["markdown-it-py"]` en el eje `enlaces`, que también toca `contracts/layers.toml`. Sin una de las dos, `check.sh --fast` sale con rc 1.
2. **Configuración del parser.** Los bloques son los de `sldb.core.ast`. Se apagan dos reglas de core que solo reescriben texto inline:
   - `text_join`, para que un escape quede como está escrito (con él, `\[\[x\]\]` pasaba a ser `[[x]]` y `[[a\_b]]` daba `a_b`). Así `raw` y `target` siguen siendo texto fuente, como en HEAD.
   - `linkify`, que reescribe URLs y partía el tiempo de parseo por dos (7.2 s a 3.8 s sobre el corpus antes del atajo de `[[`).
3. Lo que markdown-it pierde del fuente y no recupero: destino y título de un `[texto](url "título")`, y los corchetes de un enlace Markdown real (`[[x]](url)` con definición de referencia). Es fuera de alcance, y en el corpus no aparece (0 enlaces ganados o perdidos fuera de código).
4. No corrí los tests vecinos (`test_cli_reconciliation`, `test_composition_sections`, `store/test_semantic_rebuild`): el brief limita a Validation.

## Done When
- **Validation pasa con los tests nuevos: PASA.** `test_links.py` 22 passed, `test_links_batch_cli.py` 5 passed, `test_clean_code_rules.py` 1207 passed, `check.sh --fast` "TODAS LAS PUERTAS PASAN"; todos con rc 0.
- **Los bordes de los tres informes dan lo mismo que markdown-it: PASA.** Los cubren:
  - (test-lk) código indentado en un ítem de lista y backtick escapado;
  - (test-lk-c1) CRLF y fence en la línea del marcador;
  - (test-lk-c2) code span que cruza un límite de bloque.

  Cada caso afirma también que coincide con el HTML de markdown-it-py en modo `commonmark`.
- **En el corpus ningún enlace real que HEAD detecta se pierde: PASA.**
  - Método: `git ls-files '*.md'`, 1987 legibles. La base es `git archive HEAD src` en `/dev/shm/lkmd/base`. Scripts: `dump.py` y `cmp.py` en este directorio; salida en `corpus-diff.txt`.
  - Cambian 17 archivos y ninguno gana enlaces. Hay 320 enlaces en HEAD y 286 después.
  - Cada enlace perdido se cruzó con los `[[...]]` del HTML de markdown-it en modo `commonmark` fuera de `<code>`: 0 son reales. Son los mismos 17 archivos de los intentos anteriores (`CHANGELOG.md`, `docs/atoms/predicate-links.atom.md`, `docs/faq.md`, `docs/user-manual.md`, `knowledge/commands/*`, `propuesta/06` y `/09`, varios `runs/`).
- **Tiempo del corpus (mediana de 3 corridas en frío, un proceso por corrida, primer `parse_links` incluido): PASA.**
  - HEAD: 0.354 s (0.345, 0.354, 0.358).
  - Cambio: 0.646 s (0.631, 0.646, 0.650).
  - Sin `linkify` ni el atajo de `[[`, eran 7.6 s.
- **CHANGELOG: PASA.** `tools/check_claims.py`, que no está en `--fast`, da los mismos 12 errores que con el CHANGELOG de HEAD; ninguno sale de la entrada nueva.
- Commit y aviso a sldb-ui: no hechos, por orden del coordinador.

## Comandos (salida completa en `validation.log`)
| Comando (con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`) | rc |
|---|---|
| `pytest -q tests/test_links.py` | 0 |
| `pytest -q tests/test_links_batch_cli.py` | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 0 |
| `bash tools/check.sh --fast` | 0 |
| `python3 tools/check_claims.py` (extra) | 0, 12 FALSAS, preexistentes e idénticas a HEAD |

`uv` funcionó. No corrí la suite completa ni `sldb stores build --check`; Validation no los nombra.

## Archivos tocados
- `src/sldb/links/scan_text.py` (nuevo)
- `src/sldb/links/parser.py`
- `tests/test_links.py`
- `CHANGELOG.md`
- `contracts/layers.toml` (desvío 1)
- En `runs/subagents/20261116-exec-lk-md/`: `validation.log`, `result-summary.md`, `corpus-diff.txt`, `dump.py`, `cmp.py`.

No toqué `desk/`, `.sldb/` ni los cambios ajenos, no stageé nada y no hice commit.
