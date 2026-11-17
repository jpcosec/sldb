# Tester deskops-t-fd80ce2d0b55: resultado

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com` (contrato reescrito: enlaces desde el árbol de markdown-it).
Cambio revisado:
- `src/sldb/links/scan_text.py` (nuevo, sin trackear)
- `src/sldb/links/parser.py`
- `tests/test_links.py`
- `CHANGELOG.md`
- `contracts/layers.toml` (desvío aceptado por el coordinador)

**Veredicto: FALLA, por un solo borde estrecho.** Todo lo que pide el contrato pasa:
- Validation.
- Los bordes de los tres informes previos.
- El corpus contra HEAD, sin ningún enlace real perdido.
- Las regresiones vecinas.
- Escapes y énfasis.
- Clean code.

Pero el fuzz que pidió el coordinador sigue perdiendo enlaces reales que HEAD detecta, y todos por la misma causa. Cuando un `---` en la **línea 0** del documento lleva texto detrás (`---[[b]]`, o `- --- nota [[b]]` como primer ítem), el `front_matter_plugin` lo toma como apertura de front matter. El `content` del token no incluye esa línea, así que el enlace se pierde. Eso contradice el Scope ("el front matter … se escanea como hoy") y el Goal ("los enlaces reales se siguen detectando igual"). La probabilidad es baja: en el corpus no aparece (0 archivos) y en el fuzz sale en 0.08 % de los documentos. Si el coordinador lo acepta como límite del parser que exige el contrato, todo lo demás es PASA.

## Borde que falla: texto en la línea de apertura de un front matter en la línea 0
Script: `/dev/shm/lkmd-t/scripts/fm.py`. La salida está en `validation.log`.

| Markdown | cambio | commonmark | HEAD |
|---|---|---|---|
| `---[[b]]\n---\n\n[[a]]\n` | `['a']` | `['b','a']` | `['b','a']` |
| `- --- nota [[b]]\n- otro [[c]]\n` | `['c']` | `['b','c']` | `['b','c']` |
| `--- [[b]]\n\nTexto [[a]]\n` | ok | | |
| `---\n\n# T\n\nTexto [[a]]\n` (front matter sin cierre) | ok | | |
| `Intro\n--- [[b]]\n` | ok | | |
| front matter normal con `[[fm]]` dentro | ok (se lee crudo, como hoy) | | |

Tokens del primer caso: `front_matter map=[0,2] content=''`. El segundo da `list_item_open`, después `front_matter [0,1] ''` y después `list_item_close`: el plugin también se dispara dentro de un ítem que empieza en la línea 0.

Arreglo sugerido, probado en `/dev/shm/lkmd-t/scripts/fixprobe.py` con un monkeypatch en memoria (sin editar el repo): en `_block_text`, que `front_matter` aporte las líneas fuente `markdown.splitlines()[map[0]:map[1]]` y no `token.content`. Así, con las tres semillas, las pérdidas pasan de 48 a 1. La que queda es un front matter dentro de un ítem que se traga lo que sigue, un caso de laboratorio. Test: las dos filas DIFF de la tabla.

## Validation (salida completa en `validation.log`)
Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`, y `uv` funcionó.

| Comando | rc | Veredicto |
|---|---|---|
| `pytest -q tests/test_links.py` | 0, 22 passed | PASA |
| `pytest -q tests/test_links_batch_cli.py` | 0, 5 passed | PASA |
| `pytest -q tests/test_clean_code_rules.py` | 0, 1207 passed | PASA |
| `bash tools/check.sh --fast` | 0, "TODAS LAS PUERTAS PASAN" | PASA |

No corrí la suite completa ni `sldb stores build --check`. Validation no los nombra; quedan delegados al integrador.

## Done When
- **Validation pasa con los tests nuevos: PASA.**
- **Los bordes de los tres informes previos dan lo mismo que markdown-it: PASA.** Copié los scripts de `/dev/shm/tlk{,2,3}/scripts` a `/dev/shm/lkmd-t/scripts` y les saqué solo `mask_code`/`code_mask`, que ya no existe.
  - `e1.py` (test-lk): 23 casos, 0 fallas. El caso INFO `<code>[[a]]</code>` sigue contando, como acordó el Scope.
  - `e2.py` (test-lk-c1): 33 casos, 0 diffs.
  - `e2b.py` (fence en el marcador): 5 de 5 iguales.
  - `edges.py` (test-lk-c2): 44 casos, 0 diffs. Incluye los dos casos que c2 había anotado como diferencia (`-     [[x]]…` y `-\n\n    [[x]]`): ahora coinciden.
  - `e3c.py` (code span que cruza bloque): 7 de 7 ok.
  - Cada caso se compara con el HTML de markdown-it-py en modo `commonmark` fuera de `<code>`.
- **En el corpus ningún enlace real que HEAD detecta se pierde: PASA.**
  - Fuente: `git ls-files '*.md'`, 1987 legibles. La base es `git archive HEAD` en `/dev/shm/lkmd-t/base`. Scripts: `dump.py` (comprueba que importa el `sldb.links` de cada árbol) y `cmp.py`.
  - Cambian 17 archivos, los mismos de los intentos anteriores. Se pierden 40 enlaces (326 a 286, con `predicate_types={"p":"HOW"}`) y se ganan 0.
  - Enlaces perdidos que commonmark da como reales: **0**.
  - En los 1970 archivos restantes, las tuplas `(raw, target, predicate)` y el orden son idénticos a HEAD.
  - Ningún `.md` del corpus abre front matter con texto en la línea 0.
- **Tiempo del corpus en result-summary del ejecutor: PASA.** Lo medí también, en 3 corridas en frío:
  - HEAD: 0.322, 0.319 y 0.363 s (mediana 0.322 s).
  - Cambio: 0.642, 0.622 y 0.654 s (mediana 0.642 s).
  - Coincide con lo que informó el ejecutor (0.354 s y 0.646 s).
- **CHANGELOG: PASA.** Hay una entrada al principio de 0.1.13 y `check.sh --fast` pasa. Matiz: dice que el front matter "se lee como antes", y no es exacto en el borde de arriba.
- Commit y aviso a sldb-ui: no son de este rol.

## Pedidos del coordinador
- **`contracts/layers.toml`: PASA.** El diff solo cambia dos cifras: `needed_by` de `nucleo` (58 a 59) y `needs` de `enlaces` (4 a 5). Cada una lleva su nota "medido 2026-11-17 (scan de enlaces) …; antes N" delante de la historia anterior. `check.sh --fast` da rc 0.
- **Fuzz, 20000 documentos por semilla, contra commonmark.** Uso multiconjuntos y cuento solo las pérdidas de enlaces que HEAD también daba.
  - `fuzz.py` (el de c2, por conjuntos): semilla 1, 10 pérdidas y 8 de más; semilla 2, 11 y 8. El intento c2 daba 90 y 420.
  - `fuzz3.py` (multiconjunto, tres vías, con la causa):

    | semilla | pérdidas reales | enlaces de más | causa |
    |---|---|---|---|
    | 1 | 13 | 5 | front matter en la línea 0, todas |
    | 2 | 16 | 3 | front matter en la línea 0, todas |
    | 3 | 19 | 4 | front matter en la línea 0, todas |

    Ninguna diferencia tiene otra causa. Los enlaces de más son `[[...]]` dentro del contenido de un front matter (lo que parecen fences ahí se lee crudo). Eso es lo que pide el Scope y HEAD hace lo mismo, así que no lo cuento como falla. Las pérdidas son la FALLA de arriba.
- **Tests vecinos, uno a uno: PASA.** `git diff --name-only` muestra en `src/` solo `src/sldb/links/parser.py`, más `scan_text.py` sin trackear. Busqué con `grep -rlE` en `tests/` los archivos que usan `sldb.links`, `parse_links` o `scan_text`:

  | Archivo | rc | Resultado |
  |---|---|---|
  | `tests/test_cli_reconciliation.py` | 0 | 3 passed |
  | `tests/test_composition_sections.py` | 0 | 7 passed |
  | `tests/store/test_semantic_rebuild.py` | 0 | 10 passed |

  Sin fallas, así que no hizo falta comparar contra HEAD.
- **Escapes y énfasis dentro de `[[...]]`: PASA.** Probé `[[a\_b]]`, `[[*e*]]`, `[[a\]]`, `[[x**y**z]]`, `![[~~s~~]]`, `[p:: [[q\*r]]]`, `[[a&amp;b]]` y `[[\[x]]`. Dan las mismas tuplas `(raw, target, predicate, kind)` en el cambio y en HEAD: texto fuente, sin des-escapar, y el predicado primero.

## Revisión del código
- `scan_text.py`:
  - Toma el parser de `MarkdownASTHandler().md`, que es una instancia propia de cada handler (`self.md = MarkdownIt(...)` en `markdown_ast_handler.py:11`). Por eso el `.disable(["text_join","linkify"])` no altera el parser de `sldb.core.ast`.
  - Cachea una instancia por proceso en `_PARSER`, como pide Scope (2).
  - Diferencia con el Scope: también lleva `.enable("table")`, que ya está en gfm-like, así que no cambia nada.
- `parser.py`:
  - Los regex no cambian.
  - Si el texto no tiene `[[`, devuelve `[]` sin parsear, y eso es correcto porque los dos patrones lo necesitan.
- Clean code: `test_clean_code_rules.py` y `check.sh --fast` pasan.

## Archivos tocados
- Del contrato: `parser.py`, `scan_text.py` (permitido por Scope (3)), `tests/test_links.py` y `CHANGELOG.md`. Fuera del contrato: `contracts/layers.toml`, con el desvío aceptado.
- `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml` y los shards de RunDoc son del despacho (los RunDoc de este run y del ejecutor), no del ejecutor.
- No hay cambios fuera de esa lista. Los cambios ajenos que nombraba el brief (`apply_batch.py`, `lock.py`, `uv.lock`) ya no figuran en `git status`.

**PASA.**

No edité el repo. Solo escribí en `runs/subagents/20261116-test-lk-md/` y en `/dev/shm/lkmd-t/`.
