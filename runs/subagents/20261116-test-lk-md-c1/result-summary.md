# Tester deskops-t-fd80ce2d0b55-a2: resultado (corrección 1, front matter en la línea 0)

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`.
Cambio revisado: `src/sldb/links/scan_text.py` (nuevo, sin trackear), `src/sldb/links/parser.py`, `tests/test_links.py`, `CHANGELOG.md` y `contracts/layers.toml` (desvío aceptado).

**Veredicto: FALLA, por un borde estrecho que introduce esta corrección.** La FALLA anterior quedó corregida. También pasan:
- Validation.
- Las variantes del borde.
- Los bordes de los tres informes previos.
- El fuzz.
- El corpus.
- Los tests vecinos.
- Clean code.

Sin embargo, `_block_text` toma las líneas del front matter con `markdown.splitlines()`. `str.splitlines` corta además en `\x0b`, `\x0c`, `\x1c` a `\x1e`, `\x85`, ` ` y ` `, y markdown-it no trata esos caracteres como fin de línea: solo `\n`, `\r\n` y `\r`. Si un front matter contiene alguno de esos separadores, `lines[map[0]:map[1]]` se queda corta y pierde las últimas líneas. Un enlace en esas líneas, que HEAD y commonmark dan como real, desaparece. Con `token.content`, el intento anterior no tenía este problema. En el corpus no aparece: 0 archivos tienen esos caracteres.

## Borde que falla (script `/dev/shm/lkmd-t2/scripts/fmvar.py`, salida en `validation.log`)
| Markdown | cambio | HEAD | commonmark |
|---|---|---|---|
| `---\na b c\nd: [[fm]]\n---\n\n[[a]]\n` | `['a']` | `['fm','a']` | `['fm','a']` |
| igual, con `\x85` | `['a']` | `['fm','a']` | `['fm','a']` |
| igual, con `\x0c` | `['a']` | `['fm','a']` | `['fm','a']` |

Arreglo sugerido, probado con un monkeypatch en memoria (`/dev/shm/lkmd-t2/scripts/fixprobe.py`, sin editar el repo): en `scannable_text`, `lines = re.split(r"\r\n|\r|\n", markdown)` en lugar de `markdown.splitlines()`.
- Las tres filas pasan a dar `['fm','a']`.
- CRLF y `\r` solo siguen dando `['b','a']`.

Test sugerido: esas tres filas.

## Variantes del borde de la FALLA anterior: PASA
Script `fmvar.py`; `fm.py` también da 7/7 ok. Dan lo mismo que HEAD y commonmark:
- `---[[b]]` + cierre, y `- --- nota [[b]]`.
- CRLF, `\r` solo, espacios, `----`, un ítem ordenado y una cita.
- Un front matter sin cierre con texto, uno vacío, BOM y ` ` en la línea 0.

Un fence después del front matter se sigue saltando. En un front matter normal, `` `[[c]]` `` fuera de él no cuenta y `[[fm]]` adentro sí.

## Validation (`TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`, uv funcionó)
| Comando | rc | Veredicto |
|---|---|---|
| `pytest -q tests/test_links.py` | 0, 24 passed | PASA |
| `pytest -q tests/test_links_batch_cli.py` | 0, 5 passed | PASA |
| `pytest -q tests/test_clean_code_rules.py` | 0, 1207 passed | PASA |
| `bash tools/check.sh --fast` | 0, "TODAS LAS PUERTAS PASAN" | PASA |

No corrí la suite completa ni `sldb stores build --check`; quedan delegados al integrador.

## Done When
- **Validation pasa con los tests nuevos: PASA.** Están los dos tests nuevos de front matter.
- **Los bordes de los tres informes previos dan lo mismo que markdown-it: PASA.**
  - `e1.py`: 0 fallas. El caso INFO de HTML `<code>` sigue contando, como acordó el Scope.
  - `e2.py`: 0 diffs.
  - `e2b.py`: 5/5.
  - `edges.py`: 44 casos, 0 diffs.
  - `e3c.py`: ok.
- **En el corpus ningún enlace real que HEAD detecta se pierde: PASA.**
  - Base nueva: `git archive HEAD src` en `/dev/shm/lkmd-t2/base`. `files.txt` se regeneró y da 1987 legibles.
  - Cambian 17 archivos. Hay 328 enlaces en HEAD y 286 con el cambio.
  - Se pierden 42, ninguno real según commonmark (`lost_real 0`), y se ganan 0.
- **Tiempo del corpus en el result-summary del ejecutor: PASA** (0.352 → 0.681 s). Mi medición:
  - HEAD: 0.341, 0.322 y 0.321 s.
  - Cambio: 0.891 (primera corrida, en frío), 0.643 y 0.634 s.
  - Mismo orden de magnitud.
- **CHANGELOG: PASA.**
  - La entrada describe el front matter crudo desde sus líneas fuente y nombra los tests nuevos.
  - `check.sh --fast` pasa.
  - Se puede precisar cuando se corrija el borde de arriba.

## Fuzz (`/dev/shm/lkmd-t/scripts/fuzz3.py`, 20000 documentos por semilla)
| semilla | pérdidas reales | de más | antes (test-lk-md) |
|---|---|---|---|
| 1 | 0 | 6 | 13 pérdidas |
| 2 | 1 | 8 | 16 |
| 3 | 0 | 5 | 19 |

- La única pérdida es el caso de laboratorio: un front matter dentro de un ítem que se traga lo que sigue (`'- ---\t`\n...[[a3]][[b]]---...'`). Según el coordinador, no es FALLA.
- Los enlaces de más son `[[...]]` en el contenido crudo de un front matter, que HEAD también lee.
- El fuzz no genera separadores Unicode, por eso no vio el borde nuevo.

## Regresiones vecinas: PASA
- Los tests que importan `sldb.links` (grep) son `tests/test_links.py` y `tests/test_composition_sections.py`.
- Además corrí los que pidió el coordinador, uno a la vez:

| Archivo | Resultado |
|---|---|
| `tests/test_cli_reconciliation.py` | 3 passed |
| `tests/test_composition_sections.py` | 7 passed |
| `tests/store/test_semantic_rebuild.py` | 10 passed |

## Alcance: PASA
- Los archivos tocados son los del contrato, más el módulo nuevo `src/sldb/links/scan_text.py` (lo pide el Scope (3)) y `contracts/layers.toml` (desvío aceptado).
- Los cambios en `.sldb/` son RunDoc del despacho, no del ejecutor.
- Los cambios ajenos que nombra el brief ya no figuran en `git status`.
- No edité el repo, salvo esta carpeta de entrega.
