## REFORMULACION

Propósito: implementar en el repo `sldb` una transacción multi-documento anidable en `sldb.api`, un `apply_batch` con prevalidación y un `/save` atómico, absorbiendo `doc_io.DocTransaction`. Resultado: `G_WRITE_API`, con operaciones create/update/delete/move/track/untrack/write_file/record, rollback de bytes, entradas y shards, guardas optimistas, validación G4 en las cinco rutas de escritura, tests, `docs/architecture/transactions.md` y `CHANGELOG.md`. Repo: `sldb`, worktree `robocop2`, base `6b80df36`. Límites: no editar `src/sldb/api/documents/payload_save_steps.py`; no exponer `write_file` por HTTP; no modo diferido; ningún nombre del caso deskops en `src/sldb/`; no cambiar contratos sin documentarlo.

## AMBIGUEDADES

1. «si GO08 cerró al promover» / «si GO08 no cerró al despachar»: obliga a inventar el estado temporal de GO08 y si la regla `on_write error` entra o queda fuera.
2. «se re-levanta con la ruta no restaurada» frente a «la lista de rutas no restauradas»: obliga a inventar tipo de excepción, formato y si se adjunta una ruta o una lista.
3. «invalidar las cachés (compose, runtime_cache)»: obliga a inventar la API concreta de invalidación y sus nombres.
4. «las rutas de fields update y docs update que el test por ruta delate»: obliga a inventar qué módulo/función exactos se tocan si el test falla.
5. «los tests existentes de /save pasan, salvo el caso de falla parcial»: obliga a inventar cuál test concreto se modifica y cómo se adapta a `rolled_back: true`.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, los módulos de API/CLI citados, `store/io/rollback.py`, tests y docs. Cambiaría: crear `transaction.py`, `apply_batch.py`, `move_document.py`; reexportar en `api/__init__.py`; generalizar rollback; adaptar `save_routes.py` y `save_plan.py`; corregir rutas de escritura delatadas; añadir tests y documentación. Dependencias: commit base, APIs existentes de store/índice/cachés, estado de GO08 y rutas CLI. Validaría después con los `pytest` listados, `grep` de genericidad, `sldb stores check` antes/después, medición de 20 updates y nota a deskops. No ejecuta nada ahora.

## FUTURO

El supervisor decide las revisiones en frío y corre la suite completa; el operador promueve con `deskops add task --from-drawer` y dispone correcciones. GO08 determina si aplica la regla `on_write`. Un humano decide si tocar `payload_save_steps.py` exige hipótesis y nota al coordinador.
