# Tester deskops-t-80f4da96f310: undo_changes en sldb mcp (IR04b)

**Veredicto: PASA**, con una observación para el coordinador sobre la comparación byte a byte (punto 3 de las aclaraciones).

La salida completa está en `validation.log`. Mis pruebas están en `test_undo_tester.py`, que es una copia de `/dev/shm/undo-tester/test_undo_tester.py` y no está en el repo.

## Validation (corrida propia)
| rc | comando | resultado |
| --- | --- | --- |
| 0 | `uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py` | 12 passed, 1 xfailed (el xfail ya estaba en HEAD) |
| 0 | `... --extra mcp pytest -q tests/mcp/test_signals.py` | 10 passed |
| 0 | `... --extra mcp pytest -q tests/mcp/test_dry_run.py` | 1 passed |
| 0 | `uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` | 1202 passed |
| 0 | `uv run --frozen --extra code --extra dev bash tools/check.sh --fast` | TODAS LAS PUERTAS PASAN |

Validation no nombra ni la suite completa ni `sldb stores build --check`, y no los corrí.

## Done When
- **Validation pasa con los tests nuevos: PASA.** Los 4 tests nuevos de `test_write_tools.py` están en la corrida de arriba.
- **undo_changes figura entre las tools servidas: PASA.** Lo comprobé en nivel 2 (`test_undo_changes_is_served...`, test_extension y test_mutability) y en nivel 1 con mi prueba `test_level_1_serves_undo...`. En nivel 0 no está y la respuesta es `unknown_tool` con «needs write level 1».
- **CHANGELOG y docs: PASA.** Hay una entrada en 0.1.13, y la sección «Undo» de `docs/architecture/mcp.md` coincide con el código: `stale`, `nothing_to_undo`, la parada en el primer fallo, `remaining` y que no hay dry-run. check.sh --fast valida las afirmaciones.
- **Commit y aviso a IR: no hechos.** Por la decisión (6), los hace el coordinador. Queda pendiente para el cierre, no es una falla del ejecutor.

## Scope, punto por punto
1. **Pila por sesión, en memoria, que apila solo tras un apply exitoso: PASA.** `run_batch` hace `undo.push` después de `apply_batch` y nunca en las ramas `stale` ni en las de refusal. Mi prueba `test_failed_apply_does_not_push...` hace que un `apply_changes` salga stale y comprueba que después `undo_changes` responde `nothing_to_undo`.
2. **`steps` (default 1), del más nuevo al más viejo, y un fallo deja la pila desde ese lote: PASA.** Lo prueban el test del ejecutor `stops_at_the_first_that_fails` y mi revisión de `_undo_last`, que hace pop solo después de escribir.
3. **Fuera de `PENDING` y de `PENDING_TOOLS`: PASA.**
4. **Dry-run: no aplica.** `apply_changes` no tiene dry-run (`propose_changes` es el dry-run de la propuesta), así que es coherente.
5. **Tests pedidos: PASA.** Están el round-trip con el store comparado por payload, el conflicto que no escribe (tree_digest) y la pila vacía.

## Aclaraciones del coordinador
**(1) Archivos fuera de `files:`.** Revisé el diff contra HEAD de cada uno:
- `registry.py` (+1 línea): sin `add_tool(writes.undo.undo_changes)` la tool no se sirve. Hacía falta.
- `unmet.py`: agrega `"undo_changes": 1` a `LEVEL_TOOLS`. Sin eso, en nivel 0 la respuesta sería «no tool» genérico. Hacía falta para que la señal sea clara.
- `server.py`: solo cambian el docstring y `WRITE_INSTRUCTIONS`. Es texto y no cambia lógica.
- `test_extension.py` y `test_mutability.py`: el conjunto exacto de tools pasa a incluir `undo_changes`. La aserción sigue siendo una igualdad de conjuntos, igual de estricta que antes, así que no se debilitó. Sin el cambio fallaban.
- `test_signals.py`: el test `not_implemented` de undo se reemplaza por el de nivel 0, que exige `unknown_tool` + «needs write level 1» + la entrada en el log. Es consecuencia directa del Scope (3) y no debilita nada que siga vigente.
  - **Observación:** con `PENDING_TOOLS = {}`, la rama `NOT_IMPLEMENTED` de `unmet.py` (`why_missing` y `unknown_tool`) ya no la ejercita ningún test. Es código muerto mientras no se declare otra tool pendiente. Es menor y no bloquea.

**(2) Extra mcp:** lo usé en todos los tests de `tests/mcp`.

**(3) Prueba de punta a punta con el servidor real por stdio.** Para cada caso, el resultado y su prueba:
- **Dos lotes y `undo_changes(2)`, comparado byte a byte: no es byte-idéntico (observación, no lo cuento como falla).** Es la prueba `test_e2e_two_batches_undo2_is_byte_identical`. El lote 1 es create + update. El lote 2 es delete + assert_edge + update.
  - Lo que vuelve igual: el documento creado y la arista desaparecen, el documento borrado vuelve, y los payloads y los cuerpos Markdown son iguales.
  - Lo que difiere, y solo eso: el bloque de procedencia `sldb:` (`by: agent` → `agent:sldb-mcp-tests`, `at` y `via: create_document` → `save_document_payload`) de los 3 documentos tocados, y los hashes derivados de eso (`source_hash` del shard, `model_hash` y `roster_hash` de `Item.yaml`, `store_hash`).
  - El diff exacto está al final de `validation.log`.
  - Es lo esperable: el undo es una escritura nueva del actor de la sesión, y `apply_batch` la sella. El contrato pide «comparar el store», no identidad de bytes. Si el coordinador quiere que el undo restaure también la procedencia original, es un cambio de `apply_batch`/`batch_inverse`, fuera de este Scope.
- **Undo tras una escritura ajena: PASA.** Es `test_foreign_write_then_undo_is_stale_and_writes_nothing`. Responde `stale` con `written` false y `remaining` 1, y el tree_digest no cambia.
- **Un servidor nuevo no tiene pila: PASA.** Es `test_new_server_has_no_stack`. La sesión A aplica y se cierra. Después la sesión B responde `nothing_to_undo` con `remaining` 0, sin escribir.

**(4) Concurrencia: PASA.** Es `test_two_live_sessions_do_not_share_the_stack`. Abrí dos servidores vivos a la vez sobre el mismo store, y cada uno aplicó un lote sobre un documento distinto.
- B con `steps=2` responde `nothing_to_undo` con `remaining` 1, así que solo ve su propio lote.
- El undo de A restaura solo el documento de A, y el de B queda en «B1».
- Después, el undo de B restaura el suyo.
- Como cada sesión es un proceso con su propio `WriteTools.undo`, no hay estado compartido.

## Casos que el ejecutor no cubrió (pruebas propias)
Los 5 casos pasan:
- Un `apply_changes` que sale stale no apila nada.
- `steps` 0 y -1 responden `nothing_to_undo` sin escribir.
- La tool está servida en el nivel 1.
- Después de un undo no hay redo: el segundo undo responde `nothing_to_undo`.
- Un lote con delete + assert_edge se deshace bien: el documento vuelve y la arista se retracta.

## Regresiones vecinas
Los módulos de `src/` que cambiaron son `sldb.mcp.{registry,server,signals.catalog,unmet,write.apply,write.pending,write.tools}`. Con grep, los importan directamente `test_cli_mcp.py`, `test_signals.py` y `example_extension.py`. Todos los `tests/mcp/test_*.py` levantan ese servidor por subproceso, así que corrí los 8 archivo por archivo:

| archivo | resultado |
| --- | --- |
| cli_mcp | 3 passed |
| dry_run | 1 passed |
| extension | 8 passed |
| mutability | 7 passed |
| no_writes | 2 passed |
| read_tools | 14 passed |
| signals | 10 passed |
| write_tools | 12 passed, 1 xfailed |

Todos dan rc=0. Como no hubo fallas, no hizo falta comparar contra una base de HEAD.

## Fuera de los archivos del contrato
- Los cambios de `src/`, `tests/`, `docs/` y `CHANGELOG.md` son los 13 archivos más `undo.py`, nuevo: 121 inserciones y 31 borrados. Todos son los que el ejecutor declaró, y el detalle está en (1).
- No vi archivos ajenos tocados por este cambio. Los modificados de `desk/` y `.sldb/` son de la task de facts TS/JS y del inbox (del coordinador), no de este ejecutor.

## Hallazgo del ejecutor (no verificado por mí)
El ejecutor reporta un `stale` espurio en un servidor de larga vida tras una escritura de otro proceso. Es fuera de alcance, y no lo reproduje ni lo descarté. Mis pruebas de escritura ajena usan sesiones nuevas para la otra escritura, igual que las suyas, y no lo dispararon. Sugiero una nota del inbox aparte.
