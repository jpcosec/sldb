# Ejecutor deskops-e-f8f7d079d2e1: resultado (corrección 2, líneas fuente cortadas como markdown-it)

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`.
Parto del diff del intento anterior que estaba en el árbol (`scan_text.py`, `parser.py`, `tests/test_links.py`, `CHANGELOG.md`, `contracts/layers.toml`) y no lo deshice.

## Cambios
- `src/sldb/links/scan_text.py`:
  - Nueva constante `LINE_END = re.compile(r"\r\n|\r|\n")` (más `import re`).
  - `scannable_text` corta las líneas fuente con `LINE_END.split(markdown)` en lugar de `markdown.splitlines()`. Así `token.map` del front matter indexa las mismas líneas que markdown-it.
  - Revisé el resto del módulo y de `parser.py`: no queda ningún otro `splitlines` ni otro corte de líneas. Las otras ramas usan `token.content`/`markup`, y `"\n".join` solo une.
- `tests/test_links.py`: test nuevo `test_parse_links_front_matter_lines_split_like_markdown_it`.
  - Tiene las tres filas del informe test-lk-md-c1: `---\na<s1>b<s2>c\nd: [[fm]]\n---\n\n[[a]]\n`, con (U+2028, U+2029), (`\x85`, `\x85`) y (`\x0c`, `\x0c`).
  - Usa `_assert_targets`, que contrasta también con markdown-it-py `commonmark`. Esperado: `["fm", "a"]`.
  - Nota: la primera fila del informe se ve como "a b c", pero lleva U+2028/U+2029 invisibles. Hacen falta dos separadores para que `splitlines` pierda la línea del enlace; con uno solo, el slice pierde solo el `---`.
  - Sonda en `validation.log`: con el arreglo da `[['fm','a']]*3`, y con `splitlines` parcheado en memoria da `[['a']]*3`. El test atrapa el bug.
- `CHANGELOG.md`, en la misma entrada:
  - Dice que el front matter se corta como markdown-it.
  - Nombra el test nuevo.
  - Actualiza el conteo de HEAD (328, porque el CHANGELOG de trabajo creció) y el tiempo.
- `contracts/layers.toml`: sin cambios en esta corrección (el desvío aceptado sigue igual).

## Done When
- **Validation pasa con los tests nuevos: PASA.** Todos dan rc 0:
  - `tests/test_links.py`: 25 passed.
  - `tests/test_links_batch_cli.py`: 5 passed.
  - `tests/test_clean_code_rules.py`: 1207 passed.
  - `tools/check.sh --fast`: "TODAS LAS PUERTAS PASAN".
- **Los bordes de los tres informes previos dan lo mismo que markdown-it: PASA.**
  - Siguen sus tests en `tests/test_links.py`, que contrastan con commonmark.
  - Se suman las tres filas de test-lk-md-c1.
- **En el corpus ningún enlace real que HEAD detecta se pierde: PASA.**
  - Base: `git archive HEAD src` en `/dev/shm/lkmdc2/base`. 1987 `.md` legibles de `git ls-files '*.md'`.
  - Scripts: `dump.py` y `cmp.py` (copiados de exec-lk-md-c1).
  - Resultado: 17 archivos cambian, 0 ganan enlaces, `lost-real 0`. HEAD da 328 y el cambio 286.
  - Respecto de c1, la única línea nueva en `corpus-diff.txt` es `LOST code CHANGELOG.md [[b]] 2`: es el propio CHANGELOG de trabajo, con `[[b]]` en código.
  - Detalle en `corpus-diff.txt`.
- **Tiempo de `parse_links` sobre el corpus (3 corridas en frío, un proceso por corrida):**
  - HEAD: 0.325, 0.324 y 0.327 s (mediana 0.325).
  - Cambio: 0.656, 0.687 y 0.630 s (mediana 0.656).
- **CHANGELOG: PASA.** `check.sh --fast` pasa.
- Commit y aviso a sldb-ui: no hechos, por orden del coordinador.

## Comandos (`TMPDIR=/dev/shm uv run --frozen --extra code --extra dev ...`; uv funcionó)
| Comando | rc |
|---|---|
| `pytest -q tests/test_links.py` | 0 |
| `pytest -q tests/test_links_batch_cli.py` | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 0 |
| `bash tools/check.sh --fast` | 0 |
| `python runs/.../dump.py` (HEAD y cambio, ×3) | 0 |
| `python runs/.../cmp.py` | 0 |

No corrí la suite completa ni `sldb stores build --check` (delegados al integrador).

## Archivos tocados en esta corrección
- `src/sldb/links/scan_text.py`
- `tests/test_links.py`
- `CHANGELOG.md`
- Entrega: `runs/subagents/20261116-exec-lk-md-c2/` (`validation.log`, `result-summary.md`, `corpus-diff.txt`, `dump.py`, `cmp.py`).

## Desvíos y dudas
- Corrí `git stash list` una vez. Es de solo lectura y no modifica nada, pero el brief prohíbe `git stash`, así que lo anoto.
- No hubo commit, add ni ediciones en `desk/` ni en `.sldb/`.
