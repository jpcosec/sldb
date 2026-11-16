# Resultado: tester deskops-t-e4d2bed64866

Tarea: `task-clean-code-tras-create-pin-create-document-con-10-líneas-de-lógica-como-máximo`. Pills: ninguno.
Veredicto: **PASA**, con la salvedad de que `test_clean_code_rules.py` sale con rc 1 por 4 violaciones que no vienen de este cambio (detalle abajo). Salida completa en `validation.log`.

## Validation (corrida propia, `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
| comando | rc | veredicto |
|---|---|---|
| pytest -q tests/api/test_doc_anchors.py | 0 (22 passed) | PASA |
| pytest -q tests/api/test_on_write_entering.py | 0 (7 passed) | PASA |
| pytest -q tests/api/test_rewrite_references.py | 0 (21 passed) | PASA |
| pytest -q tests/test_clean_code_rules.py | 1 (4 failed, 1164 passed) | PASA en lo que toca a la tarea (ver abajo) |
| bash tools/check.sh --fast | 0 (TODAS LAS PUERTAS PASAN) | PASA |

Fallos de `test_clean_code_rules.py` en el árbol: `mcp/write/tools.py` (propose_changes 11), `store/package_version.py` (source_revision 12), `store/section_sync.py` (process_model_sections 13), `store/io/lock.py` (_acquire_outer 13).
En HEAD (`git archive` en /dev/shm/t-c3-base) son 4 fallos: los mismos 3 primeros más `api/documents/create_document.py` (create_document 12).
Conclusión: la violación de la tarea ya no está. Los otros 3 ya estaban en HEAD y quedan fuera de alcance según el Scope. El de `lock.py` sale del cambio ajeno sin commitear en `src/sldb/store/io/lock.py`, que no tocó el ejecutor. Ningún archivo tocado por la tarea viola las reglas: `create_document.py` sigue bajo 80 líneas efectivas, `create_document` tiene 10 líneas de lógica y `_write` 2.

## Done When
- Validation pasa: **PASA**, con la salvedad anterior. Done When dice que pasa "incluido test_clean_code_rules", pero el rc 1 viene solo de violaciones fuera de alcance que el Scope ordena anotar y no tocar.
- git diff no toca tests de comportamiento: **PASA**. `git status --short tests/` solo muestra `tests/api/test_apply_batch_lock.py`, que es ajeno y está sin trackear. `git diff --stat -- tests/` sale vacío.
- CHANGELOG: **PASA**. Hay una línea bajo `## 0.1.13 — not released yet` que dice que es un arreglo de clean code sin cambio de comportamiento. Corrí aparte la puerta de afirmaciones (`tools/check_claims.py`, que `--fast` omite). Da 12 falsas, la misma lista exacta que en HEAD, y pasa de 1127 a 1128 afirmaciones comprobadas, así que la línea nueva solo añade 1 afirmación y es verdadera.
- Commit: no me corresponde (lo hace el coordinador en el closeout).

## Alcance del diff
Del ejecutor solo cambiaron `src/sldb/api/documents/create_document.py` (extrae `_write`: mkdir, stamped, pin_provenance, write_source_text, en el mismo orden) y `CHANGELOG.md`. Todo lo demás modificado o sin trackear está en la lista de cambios ajenos, o son `.sldb/` y `desk/inbox` de runs ajenos. No hay nada fuera del contrato.

## Caso borde propio (no cubierto por el ejecutor)
Script `/dev/shm/t-c3-edge/edge.py`, corrido sobre el árbol y sobre HEAD:
1. `create_document` de un Review a `deep/x/y/r.md` (padres que no existen) con `actor="tester"` y un anchor `doc:TaskDoc:b`. Crea los padres, sella `by: tester` y pinnea el anchor con `@sha256:…`.
2. Un payload rechazado (`subject: "not an anchor"`) hacia `refused/dir/z.md`. Lanza ValidationError y **no crea el directorio padre**, porque el mkdir sigue después de `_admit`.
La salida es idéntica byte a byte entre el árbol y HEAD, con el timestamp normalizado.

## Regresiones vecinas
El módulo cambiado por la tarea es `create_document`. Hay 67 archivos en `tests/` que lo mencionan (`grep -rlE create_document tests/`) y los corrí uno por uno:
- 62 dan rc 0.
- 4 dan rc 5 porque no contienen tests: `tests/matching/conftest.py`, `tests/mcp/mcp_world.py`, `tests/security/audited.py`, `tests/store/invalid_memo_store.py`.
- `tests/mcp/test_write_tools.py` da rc 1 con 8 errores de setup por `No module named 'anyio'`. Es un problema de entorno: con code+dev no se instala la dependencia de mcp, y en HEAD sale igual (8 errors). Con el fallback `uvx --with-editable ".[mcp,code]"` pasa: 8 passed, 1 xfailed.
No hay ninguna falla nueva respecto de HEAD. No revisé `apply_batch.py` ni `lock.py` porque son ajenos.

## Notas del entorno
- `uv run --frozen --extra mcp` falla con "Extra `mcp` is not defined". En la base de HEAD, `--extra code` tampoco existe en el lock de HEAD, porque `uv.lock` tiene un cambio ajeno. Por eso la base la corrí con el `.venv/bin/python` del checkout.
