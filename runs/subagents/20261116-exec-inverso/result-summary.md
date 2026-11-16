# Executor deskops-e-779515b3884a: apply_batch devuelve el lote inverso (inbox 20261115-123855)

Resultado: **LISTO 0**. Todos los comandos de Validation pasan con rc=0 (salida completa en `validation.log`).

## Cambios

- `src/sldb/api/documents/batch_inverse.py` (nuevo, autorizado por Implementation Path 2):
  - `before(location, plan, pythonpath)`: bajo el cerrojo y antes de la transacción, anota para cada cambio el modelo, la ruta (`doc.path`) y, solo en update y delete, el payload actual (`current_payload` de `batch_prevalidate`, que no cambia).
  - `inverse(location, prior)`: después de la transacción y todavía bajo el cerrojo, arma el lote inverso: create→delete, track→untrack, update→update con el payload previo completo, move→move a la ruta previa (todos con el `expected_source_hash` que dejó el lote, leído de la entrada del índice); untrack→track (modelo y ruta previos), delete→create (modelo, ruta y payload previos). Tablas `_UNDO`, `_CARRY` y `_GUARDED`; helpers `_prior`, `_undo` y `_tracked` (find_doc).
- `src/sldb/api/documents/batch_report.py`: `BatchReport.inverse: list[dict[str, Any]]`, por defecto `[]`.
- `src/sldb/api/documents/apply_batch.py`: `apply_batch` llama `before` tras la prevalidación y devuelve `BatchReport(saved=..., inverse=inverse(...))` dentro del `store_lock`, con 7 líneas de lógica. `prevalidate_changes` sigue importado por nombre en el módulo (el test del lock lo parchea y pasa). `batch_prevalidate.py` no se toca.
- `tests/api/test_transaction.py`: helpers `_state` y `_create_update_delete`, constante `PROVENANCE`, y dos tests nuevos:
  - `test_applying_the_inverse_puts_payloads_entries_and_bytes_back`: create+update+delete, después `apply_batch(report.inverse)`; los payloads, las entradas del índice (sin `source_hash` ni `provenance`) y los bytes de los Markdown (sin el front matter `sldb:`) quedan iguales a los previos; `fresh.md` ya no existe y `check_store` da ok.
  - `test_the_inverse_after_another_write_is_a_conflict_and_writes_nothing`: una escritura ajena sobre `login` entre medio hace que el inverso se rechace con `ConflictError` (ref `login`) y que el árbol quede byte a byte igual (sin escritura parcial, aunque el delete de `fresh` del mismo lote inverso era válido).
- `CHANGELOG.md`: entrada al principio de 0.1.13.

## Decisión pedida en el Scope (¿usar los snapshots de Transaction?)

No. El inverso se arma con payloads, como dicen las Precisiones del coordinador: los snapshots de bytes son el estado privado del rollback y no se pueden guardar con hash, ni pasar a un consumidor (MCP) en la forma que acepta `apply_batch`. Consecuencia, ya prevista en las Precisiones: la procedencia del front matter (`sldb.by/at/via`) y, por tanto, `source_hash` y `provenance` de la entrada cambian al deshacer; el contenido (payload, `content_hash`, `field_hashes`, tags y bytes del cuerpo) vuelve igual. Ejemplo: `login` sin front matter queda con un bloque `sldb:` después de deshacer. Los tests lo comparan así.

## Done When

- Validation pasa con los dos tests nuevos: sí (test_transaction 15 passed).
- deshacer = `apply_batch(report.inverse)` deja payloads e índice iguales, y bytes iguales en los documentos canónicos (salvo la procedencia): sí, primer test nuevo.
- CHANGELOG: sí. **Commit: no lo hice** porque el brief prohíbe `git commit` (manda el brief/coordinador sobre el contrato); queda para el integrador.
- Aviso a IR: según la aclaración del coordinador, no lo mando yo; lo manda el coordinador al cerrar. Contenido sugerido: "`BatchReport.inverse` ya existe en sldb; `undo_changes` del MCP puede exponerlo como `apply_batch(store, report.inverse)`; rechazo `ConflictError` si hubo una escritura ajena, `SLDBStoreError` si alguien recreó un borrado."

## Comandos (todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)

| comando | rc |
|---|---|
| pytest -q tests/api/test_transaction.py | 0 (15 passed) |
| pytest -q tests/api/test_apply_batch_lock.py | 0 (2 passed) |
| pytest -q tests/api/test_write_paths_validate.py | 0 (5 passed) |
| pytest -q tests/api/test_on_write_entering.py | 0 (7 passed) |
| pytest -q tests/test_serve.py | 0 (61 passed) |
| pytest -q tests/test_clean_code_rules.py | 0 (1171 passed) |
| bash tools/check.sh --fast | 0 (TODAS LAS PUERTAS PASAN) |

No corrí la suite completa ni `sldb stores build --check` (no figuran en Validation; en todo caso son del integrador).

## Archivos tocados (exactos)

- src/sldb/api/documents/batch_inverse.py (nuevo)
- src/sldb/api/documents/apply_batch.py
- src/sldb/api/documents/batch_report.py
- tests/api/test_transaction.py
- CHANGELOG.md
- runs/subagents/20261116-exec-inverso/validation.log, result-summary.md (entrega)

## Desvíos y dudas

- Sin commit (ver arriba).
- El inverso de un untrack (track) no lleva guarda posible: el archivo no está trackeado; la prevalidación solo exige que el archivo exista y que el nombre esté libre. Si alguien editó ese archivo entre medio, se vuelve a trackear con su contenido actual.
- Si un lote borra A en la ruta P y crea B en esa misma P, el inverso (create A en P antes que delete B, por el orden de `apply_batch`) se rechaza en la prevalidación con "file exists", sin escribir nada. Es un caso límite; no lo cubrí porque no lo pide el contrato.
- La primera vez, `uv run` no falló; no hizo falta `uvx`.
