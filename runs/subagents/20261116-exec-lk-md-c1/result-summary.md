# Ejecutor deskops-e-2793fe94705d-a2: corrección 1 (front matter en la línea 0)

Task: `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com`. Pills: ninguno.

Parto del diff de `runs/subagents/20261116-exec-lk-md` y no lo deshago. Corrijo la FALLA de `runs/subagents/20261116-test-lk-md/result-summary.md` como indicó el coordinador.

## Cambios
- **`src/sldb/links/scan_text.py`, `_block_text(token, lines)`.**
  - Un token `front_matter` aporta sus líneas fuente, `"\n".join(lines[map[0]:map[1]])`, en lugar de `token.content`, que no incluye la línea de apertura.
  - `scannable_text` calcula `lines = markdown.splitlines()` una vez y se las pasa.
  - `RAW_BLOCKS` queda solo con `html_block`.
  - El docstring del módulo dice que el front matter aporta sus líneas fuente.
- **`tests/test_links.py`.**
  - `test_parse_links_front_matter_keeps_its_opening_line`: las dos filas DIFF del tester (`---[[b]]\n---\n\n[[a]]\n` da `['b','a']` y `- --- nota [[b]]\n- otro [[c]]\n` da `['b','c']`). Va con `_assert_targets`, que también compara contra el HTML de markdown-it-py en modo `commonmark`.
  - `test_parse_links_reads_a_front_matter_raw`: un front matter normal con `[[fm]]` y con `` `[[tick]]` `` adentro se sigue leyendo crudo, como en HEAD (`fm`, `tick` y `body`).
- **`CHANGELOG.md`, misma entrada.**
  - Precisa que el front matter se lee crudo desde sus líneas fuente, incluida la de apertura, y nombra los dos tests nuevos.
  - Actualiza el tiempo del corpus con la medición de esta corrida.

## Done When
- **Los comandos de Validation pasan con los tests nuevos: PASA.** El detalle está en `validation.log`.
  - `test_links.py`: 24 passed.
  - `test_links_batch_cli.py`: 5 passed.
  - `test_clean_code_rules.py`: 1207 passed.
  - `check.sh --fast`: "TODAS LAS PUERTAS PASAN", antes y después de editar el CHANGELOG.
  - Todos dan rc 0.
- **El test nuevo falla con el código anterior: PASA.** Con el `_block_text` de exec-lk-md (front matter → `content`), las dos filas dan `['a']` y `['c']`. Con el cambio dan `['b','a']` y `['b','c']`. Evidencia en `validation.log`.
- **Los bordes de los tres informes previos dan lo mismo que markdown-it: PASA.** Siguen los mismos tests, y pasan.
- **Fuzz del tester (`/dev/shm/lkmd-t/scripts/fuzz3.py`, 20000 documentos por semilla): las pérdidas reales bajan de 13/16/19 a 0/1/0.**
  - La única pérdida que queda (semilla 2) es un front matter dentro de un ítem que se traga lo que sigue (`'- ---\t`\n...[[a3]][[b]]---...'`). Es el caso de laboratorio que el tester anticipó.
  - Los "de más" (6/8/5) son `[[...]]` dentro del contenido crudo de un front matter, que HEAD también lee. El tester no los cuenta como falla.
- **En el corpus ningún enlace real que HEAD detecta se pierde: PASA.**
  - Método: `git ls-files '*.md'`, 1987 legibles, con la base `git archive HEAD src` en `/dev/shm/lkmdc1/base`. Scripts: `dump.py` y `cmp.py`, copiados de exec-lk-md a este directorio.
  - Cambian 17 archivos, ninguno gana enlaces y se pierden 0 reales. Hay 326 enlaces en HEAD y 286 con el cambio.
  - La salida es idéntica a la del intento anterior (0 archivos distintos), porque ningún `.md` del corpus tiene el borde.
  - Detalle en `corpus-diff.txt`.
- **Tiempo de `parse_links` sobre el corpus, mediana de 3 corridas en frío (segunda ronda; un proceso por corrida, primer parse incluido):**
  - HEAD: 0.352 s (0.353, 0.352, 0.331).
  - Cambio: 0.681 s (0.681, 0.702, 0.673).
  - En la primera ronda, la máquina estaba más cargada: HEAD 0.452, 0.351 y 0.340; cambio 0.743, 0.706 y 0.713.
  - El intento anterior midió 0.354 y 0.646. Leer las líneas fuente no cambia el orden de magnitud.
- **CHANGELOG: PASA.** `tools/check_claims.py` (extra, no está en `--fast`) da 12 falsas, las mismas preexistentes que con HEAD. Ninguna sale de esta entrada.
- Commit y aviso a sldb-ui: no hechos, por orden del coordinador.

## Comandos (con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
| Comando | rc |
|---|---|
| `pytest -q tests/test_links.py` | 0 |
| `pytest -q tests/test_links_batch_cli.py` | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 0 |
| `bash tools/check.sh --fast` | 0 |
| `pytest -q tests/test_cli_reconciliation.py tests/test_composition_sections.py tests/store/test_semantic_rebuild.py` (vecinos, extra) | 0 (20 passed) |
| `python3 tools/check_claims.py` (extra) | 1, 12 falsas preexistentes |

`uv` funcionó. La suite completa y `sldb stores build --check` no figuran en Validation y no los corrí.

## Archivos tocados en esta corrección
- `src/sldb/links/scan_text.py` (sin trackear, nuevo desde exec-lk-md)
- `tests/test_links.py`
- `CHANGELOG.md`
- `contracts/layers.toml` sigue con el desvío ya aceptado de exec-lk-md. No lo toqué en esta corrección.
- `src/sldb/links/parser.py` no cambia respecto de exec-lk-md.
- Entrega en `runs/subagents/20261116-exec-lk-md-c1/`: `validation.log`, `result-summary.md`, `corpus-diff.txt`, `dump.py` y `cmp.py`. Los temporales están en `/dev/shm/lkmdc1/`.

No toqué `desk/`, `.sldb/` ni los cambios ajenos. No stageé nada ni hice commit.

## Desvíos y dudas
- La corrección no estaba en el contrato como Precisión. La tomé del mensaje del coordinador y de la sugerencia del tester.
- Al primer intento, la medición de la base usó `python -I`, que ignora `PYTHONPATH` y cargó el árbol de trabajo. La descarté y la repetí sin `-I`. `dump.py` imprime de qué árbol importó `sldb.links`.
