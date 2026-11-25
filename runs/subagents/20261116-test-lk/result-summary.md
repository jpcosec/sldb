# Tester deskops-t-6c640e114961: resultado

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`
Cambio revisado: `src/sldb/links/parser.py` (modificado), `src/sldb/links/code_mask.py` (nuevo, sin trackear), `tests/test_links.py`, `CHANGELOG.md`.

**Veredicto: FALLA.** Validation pasa y el corpus del repo no pierde ningún enlace real. Pero dos bordes de CommonMark están mal, y los dos están confirmados con markdown-it-py en modo `commonmark`:

- (a) Un bloque de código indentado dentro de un ítem de lista se sigue leyendo como enlaces. Es el mismo error que pide arreglar la task, y el coordinador nombró este borde.
- (b) Unos backticks escapados (`` \` ``) se toman como código en línea, y el enlace real que encierran se pierde. Eso va contra el Goal: "los enlaces reales se siguen detectando igual".

## Validation (salida completa en validation.log)
| Comando | rc | Veredicto |
|---|---|---|
| `pytest -q tests/test_links.py` | 0 (11 passed, 303 s; los 3 tests nuevos tardan 0.94 s en total, el resto del tiempo es de tests anteriores) | PASA |
| `pytest -q tests/test_links_batch_cli.py` | 0 (5 passed) | PASA |
| `pytest -q tests/test_clean_code_rules.py` | 0 (1207 passed) | PASA |
| `bash tools/check.sh --fast` | 0 ("TODAS LAS PUERTAS PASAN") | PASA |

Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`; `uv` funcionó. No corrí la suite completa ni `sldb stores build --check`: el contrato no los nombra y quedan para el integrador.

## Done When
- Validation pasa con los tests nuevos: **PASA**.
- CHANGELOG: **PASA**, con una entrada al principio de 0.1.13. Matiz: dice "con las reglas de CommonMark", pero las listas son una aproximación (ver (a)).
- Commit y aviso a sldb-ui: **no hechos**. Es la decisión (5) del coordinador; los hace el coordinador o el integrador.

## Aclaraciones del coordinador
**(1) Archivos.** El cambio está en `parser.py` y en `code_mask.py` (nuevo). `src/sldb/cli/commands/links.py` no se tocó: llega al parser por `recover_links` y `parse_links`. Fuera de los archivos de la task no hay más cambios. Las modificaciones de `.sldb/` (RunDoc, store_index y store.yaml) y los shards RunDoc son del despacho, no del ejecutor. **PASA.**

**(2) Corpus HEAD contra el cambio.** Corrí `parse_links` sobre 2722 `.md`: `git ls-files '*.md'` más todo `desk/`. Para la base usé `git archive HEAD src` en `/dev/shm/tlk/base`. Scripts en `/dev/shm/tlk/scripts/{dump,cmp}.py`, salida en `/dev/shm/tlk/{head,new,lost}.json`.
- Enlaces ganados o movidos: **0**.
- Archivos que pierden enlaces: **17**, y en `desk/` ninguno.
- Revisé a mano cada una de las pérdidas con su contexto. Todas estaban dentro de código:
  - Código en línea: `CHANGELOG.md:7` y `:96`, `docs/architecture/*`, `docs/atoms/compose-vs-recover`, `docs/composition_modes.md:59`, `docs/documentation-review.md:58` y `:114`, `docs/faq.md:142-143`, las tablas de `docs/user-manual.md:642-643`, `propuesta/06:51` y varios `runs/subagents/*`.
  - Bloque cercado: `docs/atoms/predicate-links.atom.md:8-10` (```` ```markdown ````), los JSON de `knowledge/commands/cmd-sldb-docs-compose.md:120` y `cmd-sldb-predicates-add.md:63`, y `propuesta/09:54`.
- Ningún enlace real se pierde en el repo. **PASA.**

**(3) Bordes** (`/dev/shm/tlk/scripts/edges.py`).
| Caso | Resultado |
|---|---|
| `~~~` / `~~~~~` cerrado con `~~~` (no cierra) | ok |
| 4 backticks con ```` ``` ```` dentro | ok |
| fence sin cerrar | ok |
| `` ``[[a]] ` [[a2]]`` [[b]] `` (dos backticks que contienen uno) | ok, sale solo `b` |
| enlace pegado antes y después de un fence, y pegado a código en línea (`` `x`[[b]]`y` ``) | ok |
| cierre con info string (```` ``` x ````) no cierra | ok |
| fence en lista con 2 y 4 espacios, fence en blockquote, ```` ``` ```` indentado 4 tras párrafo | ok |
| predicado y transclusión dentro de código | ok |
| párrafo de un ítem indentado 4 (`- item\n\n    [[inlist]]`) | ok, es enlace |
| **(a)** `- item\n\n        [[code8]]\n\n- b [[real]]` | **FALLA**: da `['code8','real']`. CommonMark da `<pre><code>  [[code8]]` dentro del `<li>`, así que `code8` es código. Lo mismo con un subítem: `- item\n  - sub\n\n          [[c]]` da `['c']`. `_line_kind` marca como "nested" toda línea indentada dentro de una lista y nunca como código. |
| **(b)** `` \`[[b]]\` `` | **FALLA**: da `[]` y HEAD daba `['b']`. CommonMark da `<p>`[[b]]`</p>`: los backticks escapados no abren código y el enlace es real. `BACKTICK_RUN` no mira el `\` anterior. En el repo no aparece (el corpus no pierde nada), pero es una pérdida silenciosa de un enlace real. |
| (nota) CRLF pasado directo a `sldb.links.parse_links` (`` "```\r\n[[a]]\r\n```\r\n[[b]]\r\n" ``) | da `[]`. El cierre `[ \t]*$` no acepta `\r` y el fence llega hasta el fin del archivo; `BLANK_LINE` tampoco ve `\r\n\r\n`. No afecta al CLI ni a `recover_links`, porque `read_source_text` abre en modo texto y normaliza los saltos. Solo afecta a quien llame a la API pública con un string CRLF. No lo cuento como FALLA. |
| (info) `<code>[[a]]</code>` | se sigue contando. El HTML queda fuera de las reglas acordadas. |

**(4) Offsets.** En los 2722 archivos y en todos los bordes, `len(mask_code(md)) == len(md)`, y cada match de `LINK_PATTERN` y de `INLINE_PREDICATE_LINK_PATTERN` sobre el texto enmascarado coincide carácter por carácter con el original en el mismo `(start, end)`. Además, todo span que queda con el cambio está en HEAD en la misma posición (0 movidos). **PASA.**

## Regresiones vecinas
`git diff --name-only` muestra en `src/` solo `src/sldb/links/parser.py`, más `code_mask.py`, que no está trackeado. Busqué en `tests/` `sldb.links|parse_links|code_mask|links.parser|recover_links` con `grep -rlE`:
- `tests/test_links.py`: rc 0 (ver arriba)
- `tests/test_cli_reconciliation.py`: rc 0, 3 passed
- `tests/test_composition_sections.py`: rc 0, 7 passed

Sin fallas nuevas, así que no hizo falta comparar contra HEAD.

## Clean code
`code_mask.py` tiene 59 líneas, 1 módulo, sin clases y con funciones de 10 líneas o menos. `test_clean_code_rules.py` y `check.sh --fast` pasan. **PASA.**

## Qué falta para PASA
1. En `_mask_indented`, dentro de una lista, que una línea indentada 4 espacios o más por encima del ancho de contenido del ítem, tras una línea en blanco, sea código. Test: el caso (a).
2. En `_mask_inline`, que una racha de backticks precedida por `\` sin escapar no abra ni cierre código. Test: el caso (b).
3. Opcional: aceptar `\r` en el cierre del fence y en `BLANK_LINE`, o normalizar `\r\n` en `mask_code` sin mover offsets.

No edité el repo: solo escribí en `runs/subagents/20261116-test-lk/` y en `/dev/shm/tlk`.
