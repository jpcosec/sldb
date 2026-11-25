# Tester deskops-t-0e279e962a08: resultado de la corrección 2

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`

Cambio revisado:
- `src/sldb/links/parser.py` (modificado)
- `src/sldb/links/code_mask.py` y `src/sldb/links/code_blocks.py` (nuevos, sin trackear)
- `tests/test_links.py`
- `CHANGELOG.md`

**Veredicto: FALLA.** Se pierden enlaces reales que HEAD detecta cuando un backtick suelto en un párrafo se empareja con otro backtick de un bloque siguiente que no es un párrafo: un ítem de lista, un encabezado, una cita o una línea horizontal. Va contra el Goal ("los enlaces reales se siguen detectando igual") y contra el criterio del coordinador ("ningún enlace real que HEAD detecta puede perderse").

Lo demás pasa:
- Validation.
- Los bordes de las dos FALLAS anteriores, con variantes propias.
- El corpus contra HEAD.
- Clean code.
- Las regresiones vecinas.

## Borde que falla: el código en línea cruza límites de bloque
`_mask_inline` (`code_mask.py`) busca el cierre de un backtick hasta la siguiente línea en blanco (`BLANK_LINE`). En CommonMark, en cambio, un code span vive dentro de un solo bloque. Un ítem de lista, un encabezado ATX, un `>` o un `***` interrumpen el párrafo sin línea en blanco. Por eso el código empareja backticks de dos bloques distintos y enmascara el texto real que hay entre los dos.

Script: `/dev/shm/tlk3/scripts/edges_c3.py`. La salida está en `validation.log`. La columna HEAD se corrió con `git archive HEAD src`.

| Markdown | cambio | commonmark | HEAD |
|---|---|---|---|
| `` Usa el carácter ` para abrir código; ver [[real]].\n- otro ` suelto en un ítem\n `` | `[]` | `['real']` | `['real']` |
| `` - uno ` y [[real]]\n- dos ` y\n `` | `[]` | `['real']` | `['real']` |
| `` Un ` suelto y [[real]].\n# Título con ` suelto\n `` | `[]` | `['real']` | `['real']` |
| `` Un ` suelto y [[real]].\n> cita con ` suelto\n `` | `[]` | `['real']` | `['real']` |
| `` Un ` y [[real]]\n***\notro `\n `` | `[]` | `['real']` | `['real']` |
| `` Un ` suelto y [[real]].\n```\nx ` y\n```\n `` | `['real']` | `['real']` | ok (no falla: el fence ya está enmascarado) |

Un fuzz aleatorio contra commonmark (`/dev/shm/tlk3/scripts/fuzz.py`, seed 1, 20000 documentos de fragmentos) da:
- 90 documentos con pérdida de enlaces reales.
- 420 con enlaces de más.

La gran mayoría de las pérdidas son de este mismo tipo: un span que cruza ítems, citas, `---` o `\r\n`. En el corpus del repo no aparece (0 pérdidas reales), pero dos ítems consecutivos con un backtick suelto cada uno es un patrón plausible.

Arreglo sugerido: que `_mask_inline` corra por bloque (párrafo, ítem o encabezado) y no por tramo entre líneas en blanco. Por ejemplo, `mask_blocks` puede devolver también los límites de bloque, y el cierre se busca hasta el siguiente límite. Test: las cinco filas de la tabla.

## Validation (salida completa en `validation.log`)
Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`, y `uv` funcionó.

| Comando | rc | Veredicto |
|---|---|---|
| `pytest -q tests/test_links.py` | 0, 19 passed | PASA |
| `pytest -q tests/test_links_batch_cli.py` | 0, 5 passed | PASA |
| `pytest -q tests/test_clean_code_rules.py` | 0, 1208 passed | PASA |
| `bash tools/check.sh --fast` | 0, "TODAS LAS PUERTAS PASAN" | PASA |

No corrí la suite completa ni `sldb stores build --check`: los dos quedan delegados al integrador.

## Done When
- Validation pasa con los tests nuevos: **PASA**.
  - Los 5 tests nuevos cubren las cuatro filas de c1 y el fence sin cerrar dentro de un ítem.
- CHANGELOG: **PASA**, con un matiz. La entrada dice "con las reglas de CommonMark", y el código en línea no las cumple en el borde de arriba.
- Commit y aviso a sldb-ui: no hechos, por orden del coordinador.
- Goal ("los enlaces reales se siguen detectando igual"): **FALLA** por el borde de arriba.

## Bordes de las FALLAS anteriores, con variantes propias
Script: `/dev/shm/tlk3/scripts/edges.py`. Compara contra markdown-it-py en modo commonmark y comprueba también que `len(mask_code(md)) == len(md)`. Son 44 casos y 42 coinciden.

- **Código indentado en una lista:** ok.
  - Ítem y subítem de tres niveles (código contra párrafo).
  - `1)`, `10.`, `+`.
  - Tabs.
  - Párrafo después de la lista seguido de código.
- **Backtick escapado:** ok.
  - `` \` ``, `` \\` ``, `` \\\` ``.
  - Escape dentro de un span.
  - `` \`` `` y `` \`` `` después de un span doble.
- **CRLF:** ok.
  - Fence con backticks y con tildes, y fence con `\n` y `\r\n` mezclados.
  - Código indentado en un ítem.
  - Span con línea en blanco CRLF.
  - Fence en el marcador de lista con CRLF.
- **Fence en la línea del marcador de lista:** las cuatro filas de c1 y 19 variantes, todas ok.
  - `* ~~~`, y `1) ~~~~` con cierre corto.
  - `- 1. ```` (marcadores anidados) y un subítem.
  - Cierre a columna 0 (sigue abierto, igual que en commonmark) y cierre a +4 (no cierra).
  - Línea en blanco dentro del fence, gap de 2 y de 5 espacios, continuación perezosa.
  - `10.` y `3.`.
  - Info string con backtick (no es fence), línea horizontal `- - -` y apertura huérfana de primer nivel.
  - `> - ````, dos ítems con fence, ítem indentado 3 y fence tras el párrafo del ítem.
- **Dos diferencias, que no cuento como FALLA:**
  - `` -     [[x]]\n\n  [[y]]\n ``: código indentado en la línea del marcador. El ejecutor lo declara fuera de alcance.
  - `` -\n\n    [[x]]\n ``: ítem vacío seguido de código indentado de primer nivel.

  En los dos casos el cambio cuenta un enlace de más dentro de código indentado, igual que HEAD. No pierden enlaces reales y el Goal solo nombra el código cercado y el código en línea.

## Corpus contra HEAD
Scripts: `/dev/shm/tlk3/scripts/dump.py` y `cmp.py`. Base: `git archive HEAD src` en `/dev/shm/tlk3/base`. Los dos dumps se hicieron sobre el mismo árbol de trabajo.

Leí los 2354 `.md` de `git ls-files '*.md'`:
- Archivos que ganan enlaces: 0.
- Archivos que pierden enlaces: 17.
- Enlaces perdidos que commonmark da como reales: **0**.
- `parse_links` contra commonmark: **0 archivos distintos**.

**PASA.**

## Clean code de `code_blocks.py`
- 71 líneas y 0 clases.
- La función más larga es `_open_items`, con 7 líneas de lógica.
- `pytest tests/test_clean_code_rules.py -k "code_blocks or code_mask"`: 2 passed, así que el archivo sin trackear entra en el chequeo.
- `check.sh --fast` pasa.

**PASA.**

## Archivos tocados
- El código está en `parser.py`, `code_mask.py` y `code_blocks.py`.
  - Ninguno figura en `files` del contrato, que nombra `src/sldb/cli/commands/links.py`.
  - Aun así el Scope pide "encontrar el parser … y excluir", así que lo acepto.
  - `links.py` no se tocó.
- También cambian `tests/test_links.py` y `CHANGELOG.md`.
- El resto de los cambios no son del ejecutor: `.sldb/` y `desk/` son del despacho, y `runs/` es de otros runs.

**PASA.**

## Regresiones vecinas
`git diff --name-only` muestra en `src/` solo `src/sldb/links/parser.py`. Busqué con `grep -rlE` en `tests/` los archivos que usan `sldb.links`, `parse_links`, `code_mask` o `code_blocks`. Cada uno se corrió por separado:

| Archivo | rc | Resultado |
|---|---|---|
| `tests/store/test_semantic_rebuild.py` | 0 | 10 passed |
| `tests/test_composition_sections.py` | 0 | 7 passed |
| `tests/test_cli_reconciliation.py` | 0 | 3 passed |
| `tests/test_links.py` | — | ya está en Validation |

**PASA.**

No edité el repo. Solo escribí en `runs/subagents/20261116-test-lk-c2/` y en `/dev/shm/tlk3/`.
