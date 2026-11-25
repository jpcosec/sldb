## REFORMULACION

**Propósito:** ejecutar GD24 (plan `generalizar-desde-deskops` rev 3, hijo de PG2) para que toda escritura de sldb pase por una transacción reversible. **Resultado:** `sldb.api.transaction(store)` anidable con operaciones create/update/delete/move/track/untrack/write_file/record, `sldb.api.apply_batch` con prevalidación, `/save` atómico (`rolled_back: true`), validación de payload en las cinco rutas de escritura, `RollbackError`, `docs/architecture/transactions.md` y CHANGELOG; produce G_WRITE_API. **Repo:** sldb, worktree aparte en robocop2 (`wt/gd24` desde `origin/main 9182759f`; referencia de genericidad `6b80df36`). **Límites:** no editar `payload_save_steps.py`; fuera write_file por HTTP, modo diferido y nombres deskops; la parte on_write de GO08 queda fuera (q10).

## AMBIGUEDADES

1. «sldb.api.transaction(store)» no aclara si `store` es ruta o store abierto (las funciones de `sldb.api` reciben ruta); obligaría a inventar la firma.
2. «move(ref, new_path) (mueve el archivo y re-trackea con el mismo nombre…)» no fija la raíz de `new_path` ni qué ocurre si el destino ya existe; solo create dice «dentro de la raíz del store».
3. «track(path, model, name=None)» no dice de dónde sale el nombre por defecto.
4. «update(ref, payload, expected_source_hash=None, expected=None)» no dice cuál guarda prevalece ni el orden si se pasan ambas.
5. «RollbackError… unrestored: list[str] (rutas relativas a la raíz)» no precisa si es raíz del store o del proyecto.
6. «tiempo de pared de un lote de 20 updates antes (save_routes actual) y después» no nombra arnés ni cómo obtener el "antes" sin inventarlo.

## DRY-RUN

**Lecturas:** TaskDoc, rituales execution/testing/closeout y los archivos listados en `files`. **Cambios previstos:** crear `transaction.py`, `apply_batch.py`, `move_document.py`; editar `api/__init__.py`, `store/io/rollback.py`, `save_routes.py`, `save_plan.py`, `fields_mutate.py`, `fields_save.py`, `docs.py`; tests nuevos/ajustados (`test_transaction.py`, `test_write_paths_validate.py`, renombre en `test_serve.py`), doc y CHANGELOG. **Dependencias:** invalidadores existentes (q7) y `RollbackError` (q6); GO08 fuera. **Validaciones futuras:** los `pytest` listados, grep de genericidad, `stores check` y benchmark de 20 updates.

## FUTURO

El coordinador confirma GO08/on_write al despachar; el supervisor corre la suite completa y decide las revisiones en frío; el dueño respalda DA2 en CHANGELOG; deskops recibe la nota de cierre (regla 7); la promoción usa `deskops add task --from-drawer`.
