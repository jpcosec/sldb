# Tester deskops-t-937f21dafaca: apply_batch devuelve el lote inverso (inbox 20261115-123855)

Veredicto: **PASA**. Salida completa en `validation.log`.

## Validation (corrida propia, `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev ...`)

| comando | resultado |
|---|---|
| pytest -q tests/api/test_transaction.py | PASA: 15 passed, incluidos los 2 tests nuevos |
| pytest -q tests/api/test_apply_batch_lock.py | PASA: 2 passed |
| pytest -q tests/api/test_write_paths_validate.py | PASA: 5 passed |
| pytest -q tests/api/test_on_write_entering.py | PASA: 7 passed |
| pytest -q tests/test_serve.py | PASA: 61 passed |
| pytest -q tests/test_clean_code_rules.py | PASA: 1171 passed |
| bash tools/check.sh --fast | PASA: TODAS LAS PUERTAS PASAN |

La suite completa y `sldb stores build --check` no figuran en Validation; quedan para el integrador y no los corrí.

## Done When, punto por punto

- Validation pasa con los dos tests nuevos: **PASA** (ver tabla).
- Deshacer = `apply_batch(report.inverse)` deja el store como antes (payloads e índice iguales y, en los canónicos, bytes iguales): **PASA**. El test nuevo lo cubre para create+update+delete, comparando el índice sin `source_hash`/`provenance` y los bytes sin el front matter `sldb:`, como permiten las Precisiones del coordinador. Además probé por mi cuenta move+untrack, rehacer (el inverso del inverso) y el lote vacío; ver abajo.
- Guardas: un inverso aplicado después de una escritura ajena da `ConflictError` y no escribe nada: **PASA** (test nuevo). Por mi cuenta: el inverso de un delete cuyo documento recreó otro da `SLDBStoreError` y tampoco escribe nada.
- CHANGELOG: **PASA**, con entrada al principio de 0.1.13.
- Commit y aviso a IR: **no hechos, y no es falla del ejecutor**. El brief prohíbe hacer commit (le toca al integrador) y el aviso a IR lo manda el coordinador al cerrar. El ejecutor dejó redactado en su result-summary el texto sugerido del aviso.
- Clean code en los archivos tocados: `batch_inverse.py` tiene 61 líneas físicas, 1 clase como mucho y funciones de 1 a 6 líneas de lógica; `apply_batch` tiene 7. **PASA**, según test_clean_code_rules y check.sh.

## Casos que el ejecutor no cubrió (`/dev/shm/tinv/test_inverse_edges.py`, 5 passed)

1. Lote vacío → `inverse == []`.
2. Move a `sub/login2.md` más untrack, y después su inverso (move de vuelta con `expected_source_hash`, y track con modelo y ruta): payloads iguales y `check_store` ok.
3. Rehacer: aplicar el inverso del inverso deja los payloads del estado posterior al lote.
4. El inverso de un delete cuyo documento otro ya recreó → `SLDBStoreError` y árbol byte a byte igual.
5. El caso límite del ejecutor (ver la sección siguiente).

## Caso límite: borrar A en P y crear B en la misma P

**Clasificación: límite documentable, no falla del contrato. En la práctica, el caso no se puede alcanzar.**

Evidencia: el lote directo `[delete login (login.md), create b con path login.md]` **ya lo rechaza la prevalidación** con `SLDBStoreError: b: file .../login.md already exists` y no escribe nada. Lo mismo ocurre con `[move login→z.md, move c→login.md]` y con `[delete login, move c→login.md]` (test 5: los tres se rechazan y el árbol queda igual). La razón es que `_free` comprueba cada ruta destino contra el estado **anterior** al lote, así que ningún lote puede reocupar una ruta que él mismo libera.

Por qué eso basta: en el inverso, las rutas que se llenan (por create o move de vuelta) son las rutas de las que el lote directo sacó un documento, y las rutas que se liberan (por delete o move de vuelta) son las rutas que el lote directo ocupó. Para que coincidan, el lote directo tendría que haber ocupado una ruta que él mismo liberaba, y eso es justo lo que la prevalidación rechaza. Por lo tanto, todo inverso que sale de `apply_batch` es aplicable en el orden actual (create/track primero), si nadie escribió entre medio. Cambiar el orden del inverso no hace falta y además no alcanzaría: `apply_batch` vuelve a ordenar por `_ORDER`, así que el orden de la lista `inverse` no influye.

Se convertiría en problema solo si en el futuro la prevalidación dejara reutilizar rutas liberadas dentro del mismo lote. Propuesta: anotarlo como límite en el docstring de `batch_inverse.py` o en el CHANGELOG ("el inverso nunca necesita reocupar una ruta que libera, porque el lote directo no puede hacerlo"). Si alguien arma a mano un lote con esa forma, se rechaza con `SLDBStoreError` y sin escribir nada; no queda un estado parcial.

## Regresiones vecinas

Módulos de `src/` cambiados: `apply_batch.py`, `batch_report.py` y `batch_inverse.py` (nuevo). Con `grep -rlE 'apply_batch|batch_report|batch_inverse|BatchReport' tests/` aparecen test_apply_batch_lock, test_write_paths_validate, test_transaction y test_on_write_entering, los cuatro ya en Validation y los cuatro en verde. Como no hubo fallas, no hizo falta compararlos contra la base de HEAD.

## Alcance

Cambios del ejecutor: `CHANGELOG.md`, `apply_batch.py`, `batch_report.py`, `tests/api/test_transaction.py` y `batch_inverse.py` (nuevo, autorizado por Implementation Path 2 y por la aclaración del coordinador). No hay nada más en `src/` ni en `tests/`. Los cambios en `.sldb/` (RunDoc, ReviewDoc, store.yaml, store_index.yaml) son el registro de runs y reviews de deskops, no del ejecutor. `uv.lock` es ajeno. No toqué el repo salvo esta carpeta de entrega.

## Notas menores (no bloquean)

- El inverso de un untrack (un track) no lleva guarda, porque el archivo no está trackeado. Si alguien edita ese archivo entre medio, se vuelve a trackear con el contenido nuevo. El ejecutor lo documentó; lo veo aceptable porque el Scope no pide guarda sobre archivos sin trackear.
