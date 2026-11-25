# Tester deskops-t-af5709ec1b51: resultado (corrección 2, líneas fuente cortadas como markdown-it)

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`.

Cambio revisado:
- `src/sldb/links/scan_text.py` (nuevo, sin trackear).
- `src/sldb/links/parser.py`.
- `tests/test_links.py`.
- `CHANGELOG.md`.
- `contracts/layers.toml` (desvío aceptado).

**Veredicto: PASA.**
- La FALLA de test-lk-md-c1 está corregida: el front matter se corta solo en `\r\n`, `\r` y `\n`.
- Las variantes del borde dan 0 diferencias, con los 8 separadores de `str.splitlines`, dentro y fuera del front matter.
- Los bordes de los cinco informes previos dan 0 diferencias.
- En el fuzz, la única pérdida es el caso de laboratorio.
- En el corpus se pierden 0 enlaces reales.
- Los tests vecinos dan igual que en HEAD.
- Clean code y `check.sh --fast` pasan.

Hay tres observaciones que no son FALLA (ver abajo). La salida completa está en `validation.log`, y los scripts en `/dev/shm/tlkmdc2/scripts/`.

## Validation (`TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`; uv funcionó)
| Comando | rc | Veredicto |
|---|---|---|
| `pytest -q tests/test_links.py` | 0, 25 passed | PASA |
| `pytest -q tests/test_links_batch_cli.py` | 0, 5 passed | PASA |
| `pytest -q tests/test_clean_code_rules.py` (también el "siempre") | 0, 1207 passed | PASA |
| `bash tools/check.sh --fast` (también el "siempre") | 0, "TODAS LAS PUERTAS PASAN" | PASA |

No corrí la suite completa ni `sldb stores build --check`: quedan delegados al integrador.

## Done When
- **Validation pasa con los tests nuevos: PASA.**
  - `test_parse_links_front_matter_lines_split_like_markdown_it` cubre las tres filas de test-lk-md-c1.
  - **Mutación:** en una copia (`/dev/shm/tlkmdc2/mut`) volví a `markdown.splitlines()`. Con eso, `tests/test_links.py` da `1 failed, 24 passed`, y el que falla es ese test. Es decir, el test atrapa el bug.
- **Los bordes de los informes previos dan lo mismo que markdown-it: PASA.** Los scripts de test-lk-md y test-lk-md-c1 cubren test-lk, test-lk-c1, test-lk-c2, test-lk-md y test-lk-md-c1. Los corrí todos con el cambio:

  | Script | Resultado |
  |---|---|
  | `e1.py` | todos ok; el INFO de HTML `<code>` sigue contando, como acordó el Scope |
  | `e2.py` | `diffs 0` |
  | `e2b.py` | 5/5 |
  | `edges.py` | 44 casos, 0 diffs |
  | `e3c.py` | 44 casos, 0 diffs |
  | `fm.py` | ok |
  | `fmvar.py` | 17 filas, ninguna `PIERDE`; las tres filas de c1 dan `['fm','a']`, como HEAD y commonmark |

- **En el corpus ningún enlace real que HEAD detecta se pierde: PASA.**
  - Base: `git archive HEAD` en `/dev/shm/tlkmdc2/base`. Corpus: 1987 `.md` legibles de `git ls-files '*.md'`.
  - Cambian 17 archivos. Hay 328 enlaces con HEAD y 286 con el cambio: se pierden 42, ninguno real (`lost_real 0`), y se ganan 0.
  - Comparé con el `cmp.py` de los informes previos, con el oráculo corregido (ver Observación 1).
- **Tiempo del corpus anotado por el ejecutor: PASA.** El ejecutor anota 0.325 → 0.656 s. Mi medición:
  - HEAD: 0.333, 0.330 y 0.339 s.
  - Cambio: 0.842, 0.801 y 0.676 s (mediana 0.80).
  - Mismo orden de magnitud: el cambio tarda unas 2–2.5 veces más.
- **CHANGELOG: PASA.**
  - La entrada dice cómo se corta el front matter y nombra el test nuevo.
  - Sus cifras de corpus (17 archivos, 328 → 286, 0 ganados, todo lo perdido dentro de código) coinciden con las mías.
  - `check.sh --fast` pasa.

## Borde de separación de líneas con variantes (`lsep.py`): PASA
- Probé los 8 separadores de `str.splitlines` que no son de markdown-it: `\x0b`, `\x0c`, `\x1c`, `\x1d`, `\x1e`, `\x85`, U+2028 y U+2029.
- Los crucé con 19 plantillas:
  - **Dentro del front matter:** 1 o 3 separadores, en la línea 0, antes del cierre, con CRLF, y con fence o código en línea después.
  - **Fuera del front matter:** párrafo, separador dentro de `[[...]]`, fence, info string, código en línea, código indentado, lista, cita, tabla, `html_block`, encabezado y predicado.
- Resultado: 152 casos, 0 diferencias (ni pérdidas que HEAD detecta y commonmark da como reales, ni enlaces de más).

## Fuzz (20000 documentos por semilla)
**`fuzz3.py`, el fuzz de los informes previos:**

| semilla | pérdidas reales | de más |
|---|---|---|
| 1 | 0 | 6 |
| 2 | 1 | 8 |
| 3 | 0 | 5 |

- Es lo mismo que en c1.
- La única pérdida es el caso de laboratorio: un front matter dentro de un ítem que se traga lo que sigue (`'- ---\t`\n…[[a3]][[b]]---…'`). Queda anotado, no es FALLA, como indica el coordinador.
- Todos los "de más" son `front_matter_linea0`: `[[...]]` en el contenido crudo de un front matter, que HEAD también lee.

**`fuzzsep.py` (caso nuevo, que el ejecutor no cubrió):** es `fuzz3` con estos fragmentos agregados:
- `\x0b`, `\x0c`, `\x1c`, `\x85`, U+2028 y U+2029.
- `\r` suelto.
- `---\n`.
- `[rel:: [[p]]]`.

Con el oráculo heredado aparecieron pérdidas de tipo "otra" (3, 1 y 2 según la semilla). Las analicé con `lossprobe.py`, que usa el `parse_links` real de HEAD:
- Las seis tienen la forma `\r\r\n` seguida de una línea indentada 4 espacios.
- Para markdown-it, `\r\r\n` son dos saltos, es decir, una línea en blanco. Por eso la línea siguiente es `code_block`.
- El oráculo hacía `replace("\r\n","\n")` antes de renderizar. Eso convertía `\r\r\n` en un solo salto y la línea pasaba a ser continuación de párrafo. Demostración en `validation.log`:
  - `p\r\r\n    [[b]]` da `<pre><code>[[b]]`.
  - Con el `replace`, da `<p>p\n[[b]]</p>`.

Con el oráculo commonmark sin `replace` (`oracle.py`), `fuzzsep` da en las semillas 1, 2 y 3:
- 0 pérdidas.
- 10, 8 y 9 de más, todas `front_matter_linea0`.

## Regresiones vecinas: PASA
- Módulo de `src/` cambiado: `src/sldb/links/parser.py`, más el nuevo `scan_text.py`.
- Por grep, importan `sldb.links` o `parse_links`: `tests/test_links.py`, `tests/test_composition_sections.py` y `tests/test_cli_reconciliation.py`.
- Sumé el que pidió el coordinador. Corrí uno a la vez, en el árbol y en HEAD (`git archive`):

| Archivo | cambio | HEAD |
|---|---|---|
| `tests/test_cli_reconciliation.py` | 3 passed | 3 passed |
| `tests/test_composition_sections.py` | 7 passed | 7 passed |
| `tests/store/test_semantic_rebuild.py` | 10 passed | 10 passed |

## Bordes propios (`mine.py`, contra el `parse_links` real de HEAD)
Dan igual que HEAD:
- Predicado partido en dos líneas (`[rel::\n[[a]]]`).
- Entidades (`[[a&amp;b]]`).
- Énfasis y tachado dentro del enlace.
- Escapes (`[[a\_b]]`).
- URL (sin linkify).
- Enlaces dentro del texto de `![alt](u)` y de `[t](u)`.
- Una transclusión en una tabla (el `[[c]]` en código de esa celda ya no cuenta, como corresponde).

Además:
- Hay una sola instancia de MarkdownIt por proceso: `_parser() is _parser()` da True.
- El `.disable(["text_join","linkify"])` no se filtra: un `MarkdownASTHandler()` nuevo conserva las dos reglas, porque cada instancia crea su propio `MarkdownIt`.

## Observaciones (no son FALLA)
1. **El oráculo de los tests normaliza mal `\r\r\n`.**
   - `_assert_targets` (`tests/test_links.py:634`) y el `cmp.py` de los informes previos hacen `markdown.replace("\r\n", "\n")` antes de renderizar commonmark.
   - Con `\r\r\n`, el oráculo ve un documento distinto del que parsea markdown-it.
   - Hoy ningún test ni archivo del corpus tiene esa secuencia, así que no cambia ningún resultado.
   - Conviene quitar el `replace`, porque markdown-it ya normaliza `\r\n?`.
2. **Un `[[...]]` que cruza un salto de línea pierde los espacios del borde en `raw` y `target`.**
   - Casos: espacios finales, hardbreak con dos espacios o con `\`, y sangría de la línea siguiente.
   - Ejemplos: `[[a  \nb]]` da `a\nb` (HEAD da `a  \nb`), y `[[a\\\nb]]` da `a\nb`.
   - Es efecto directo de "softbreak y hardbreak como salto de línea" del Scope.
   - El enlace se sigue detectando, `raw` solo se informa (recovery lo copia) y no se usa para ubicar texto en la fuente, y ningún archivo del corpus lo tiene.
3. **Otros dos casos donde `raw` difiere de la fuente.**
   - `[[<http://a.b>]]` da `http://a.b`, sin los `<>` del autolink.
   - Un NUL dentro de `[[...]]` sale como U+FFFD, por la normalización de markdown-it.
   - Mismo alcance que la observación 2: casos de laboratorio, ninguno en el corpus.

## Alcance: PASA
- Los archivos tocados son:
  - Los del contrato: `parser.py`, `tests/test_links.py` y `CHANGELOG.md`.
  - `src/sldb/links/scan_text.py`, que pide el Scope (3).
  - `contracts/layers.toml`, con el desvío aceptado: solo cambia `needs` de `enlaces` (4 → 5) y `needed_by` de `nucleo` (58 → 59), con su nota.
- Los cambios en `.sldb/` y en `desk/` son del despacho y el coordinador, no del ejecutor.
- Los cambios ajenos que nombra el brief (`apply_batch.py`, `lock.py`, `uv.lock` y el test de lock) ya no figuran como modificados en `git status`.
- No edité el repo, salvo esta carpeta de entrega.
- No usé `git stash`, `add`, `commit` ni suite completa.
