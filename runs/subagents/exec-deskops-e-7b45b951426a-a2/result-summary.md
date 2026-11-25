# Resultado
run_id: run-deskops-e-7b45b951426a-a2 · session: scion://agent/deskops-e-7b45b951426a-a2 · session_sha256: (n/a)

Intento 2: la instalación del merge driver sale de las funciones de API (init_store, scaffold_store, build_store) y va en los comandos CLI (`stores init`, `stores scaffold --apply`, `stores build`). `merge-driver-missing` en `stores check` se queda (solo lee).

Archivos: src/sldb/api/stores/{init_store,scaffold_store,build_store,ensure_merge_driver}.py, src/sldb/cli/commands/{store_init,stores_scaffold,stores_build}.py, tests/store/test_merge_driver_auto_install.py (usa CLI + test nuevo: la API no deja .gitattributes ni merge.sldb.*), tests/store/test_migrate_layout.py (instala el driver a mano antes del check limpio), CHANGELOG.md.

Validación: ver validation.log. Test de deskops test_split_restores_source_and_store_when_the_second_atom_create_fails pasa con PYTHONPATH a este sldb.
Revisar: `check.sh --fast` da rc 1 solo por «identidad: workbench_demo sin clasificar» (preexistente, decisión pendiente, no de esta tarea).
