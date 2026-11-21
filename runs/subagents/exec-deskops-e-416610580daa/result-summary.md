# Resultado (BLOQUEADO en el gate check.sh --fast, no por el codigo de la tarea)
Worktree: .worktrees/deskops-e-416610580daa (rama deskops/deskops-e-416610580daa), cambios SIN commitear:
- src/sldb/store/documents_dirty_persist.py (nuevo): load/save/delete de .sldb_cache/documents_dirty.json, atomico (tmp+os.replace) bajo store_lock; corrupto/firma distinta -> borra y {}; fallos de escritura silenciosos.
- src/sldb/store/documents_dirty.py (56 lineas): carga perezosa en la primera llamada por store; mark/clear/invalidate reescriben; clear_all borra archivos.
- tests/store/test_merkle_operation_cache.py: 3 tests con subprocess (proceso nuevo ve el dirty, corrupto cae a calculo completo, firma cambiada invalida).
- CHANGELOG.md; contracts/layers.toml (modulo nuevo en eje op_documentos; needs operacion 72, needed_by persistencia 50, exigidos por check.sh).
Validation: ver validation.log. Los 4 pytest pasan. check.sh --fast rc 1 por `workbench_demo` sin clasificar en la raiz (identidad), preexistente (falla igual en main). Arreglarlo exige decidir si es producto/autoaplicacion/ajeno: fuera del alcance. No commitee ni avance la tarea por la regla "check rc 0 antes de commitear".
Nota de diseno: la firma incluye el store_hash, asi que un write posterior al mark (que mueve el indice) invalida el archivo; lo cubre el calculo completo. Asi lo pide la spec.
Supervisor: decidir workbench_demo, o autorizar el commit con el gate fallando.

## Excepcion autorizada (coordinador, 2026-11-21)
Commit hecho en el worktree con las 5 rutas listadas arriba y trailer Task-Id. check.sh --fast: unica puerta en rojo = identidad, solo por `workbench_demo` (preexistente, decision aparte f055723d); el resto en verde.
