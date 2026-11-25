# Tester deskops-t-6c640e114961-a2: resultado (reintento tras la FALLA de `runs/subagents/20261116-test-lk/`)

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`
Cambio revisado: `src/sldb/links/parser.py` (modificado), `src/sldb/links/code_mask.py` (nuevo, sin trackear), `tests/test_links.py`, `CHANGELOG.md`.

**Veredicto: FALLA.** Las tres FALLAS anteriores están corregidas: el código indentado en un ítem de lista, el backtick escapado y CRLF, cada uno con sus variantes. Validation pasa, y el corpus del repo no pierde ningún enlace real respecto de HEAD. Pero encontré un borde nuevo, confirmado con markdown-it-py commonmark, que **pierde enlaces reales que HEAD sí detecta**: un fence que se abre en la línea del marcador de lista. Eso va contra el Goal ("los enlaces reales se siguen detectando igual").

## Borde que falla: fence en la línea del marcador de lista
`FENCE_OPEN` exige 0 a 3 espacios antes del fence, así que no ve la apertura en `- ```` ni en `1. ```python`. Sí ve el cierre indentado (`   ````) y lo toma por una apertura. Como ese bloque nunca cierra, se enmascara **hasta el fin del archivo**.

| Markdown | cambio | commonmark | HEAD |
|---|---|---|---|
| `` 1. ```python\n   x = 1\n   ```\n\nVer [[real]].\n `` | `[]` | `['real']` | `['real']` |
| `` - ```\n  code\n  ```\n\nVer [[real]] y [[otro]].\n `` | `[]` | `['real','otro']` | `['real','otro']` |
| `` - ```bash\n  echo [[x]]\n  ```\n- [[item]]\n `` | `['x']` | `['item']` | `['x','item']` |
| `` - ```\n  [[f]]\n  ```\n[[r]]\n `` | `['f']` | `['r']` | — |

En la tabla hay dos fallas: se pierden todos los enlaces reales que siguen al bloque, y el contenido del bloque se cuenta como enlace. Un paso de una guía numerada con un bloque de código es un patrón común en Markdown. En el repo no aparece hoy (`grep -E '^ {0,3}([-*+]|[0-9]+[.)]) +(```|~~~)'` sobre `git ls-files '*.md'` no da nada), y por eso el corpus no lo detecta.

Arreglo sugerido: que `FENCE_OPEN` acepte un prefijo de marcadores de lista (o que el fence se detecte a la columna de contenido del ítem, junto con `_line_kind`). Test: las cuatro filas de la tabla.

## Validation (salida completa en `validation.log`)
| Comando | rc | Veredicto |
|---|---|---|
| `pytest -q tests/test_links.py` | 0, 14 passed | PASA |
| `pytest -q tests/test_links_batch_cli.py` | 0, 5 passed | PASA |
| `pytest -q tests/test_clean_code_rules.py` | 0, 1207 passed | PASA |
| `bash tools/check.sh --fast` | 0, "TODAS LAS PUERTAS PASAN" | PASA |

Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`, y `uv` funcionó. No corrí la suite completa ni `sldb stores build --check`: los dos quedan delegados al integrador.

## Done When
- Validation pasa con los tests nuevos: **PASA**.
- CHANGELOG: **PASA**. La entrada está al principio de 0.1.13. Matiz: dice "con las reglas de CommonMark", pero no cubre un fence dentro de un ítem de lista.
- Commit y aviso a sldb-ui: **no hechos**, por orden del coordinador.

## Bordes y variantes contra markdown-it-py commonmark
Script en `/dev/shm/tlk2/scripts/edges.py`, salida en `validation.log`. Son 33 casos y 32 coinciden. En todos, `len(mask_code(md)) == len(md)`.
- Código indentado en un ítem: `- item\n\n        [[code8]]`, el subítem, ordenadas `1.`, `1)`, `2.` y `10.`, tres niveles de anidación (código contra párrafo), gap de 4 y de 5 espacios tras el marcador, ítem vacío, tabs, marcadores mezclados `*`/`+` y salida de la lista. Todos **ok**.
- Escapes: `` \` ``, `` \\` ``, `` \\\` ``, escape dentro de un span, `` \`` `` y una barra al final de línea. Todos **ok**.
- CRLF puro y mezclado con `\n`: fences, una línea en blanco `\r\n\n`, código indentado en un ítem y un cierre con espacios antes de `\r`. Todos **ok**.
- Fence en la línea del marcador de lista: **DIFF** (ver arriba). Detalle en `/dev/shm/tlk2/scripts/edges2.py`.

## Corpus contra HEAD
Para la base usé `git archive HEAD src` en `/dev/shm/tlk2/base`. Corrí `parse_links` sobre los 1955 `.md` legibles de `git ls-files '*.md'`. Scripts: `dump.py` y `cmp.py`. Datos: `/dev/shm/tlk2/{head,new}.json`.
- Archivos que ganan enlaces: 0.
- Archivos que pierden enlaces: 17, los mismos del intento anterior.
- En cada archivo, cada enlace perdido se cruzó con los `[[...]]` fuera de `<code>` del HTML de markdown-it-py commonmark. **Ninguno es un enlace real.**
- `mask_code` contra commonmark en todo el corpus: **0 archivos distintos**.

## Archivos
Los cambios están en `parser.py`, `code_mask.py`, `tests/test_links.py` y `CHANGELOG.md`. `src/sldb/cli/commands/links.py` no se toca; Scope pide encontrar su parser. Los cambios en `.sldb/` (ReviewDoc, RunDoc, store_index y store.yaml) son del despacho. **PASA.**

## Regresiones vecinas
`git diff --name-only` muestra en `src/` solo `src/sldb/links/parser.py`, más `code_mask.py`, que no está trackeado. Los importan:
- `tests/test_cli_reconciliation.py`: rc 0, 3 passed.
- `tests/test_composition_sections.py`: rc 0, 7 passed.
- `tests/test_links.py`: rc 0, ya en Validation.

No hay fallas nuevas. **PASA.**

## Clean code
`code_mask.py` tiene 71 líneas, sin clases y con funciones de 10 líneas o menos. `test_clean_code_rules` y `check.sh --fast` pasan. **PASA.**

No edité el repo: solo escribí en `runs/subagents/20261116-test-lk-c1/` y en `/dev/shm/tlk2`.
