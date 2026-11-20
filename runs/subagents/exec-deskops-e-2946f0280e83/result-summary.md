# Resultado
Base: git revert --no-commit de 8e24da2e + patch del intento 2 (CLI instala, API no). Ajustes: tests/api/test_gitignore_policy.py (3 tests esperan ahora merge-driver-missing); ensure_merge_driver.py: missing_merge_driver partida en helpers (regla clean-code de 10 lineas).
Archivos: CHANGELOG.md, src/sldb/api/stores/{ensure_merge_driver,store_surroundings}.py, src/sldb/cli/commands/{store_init,stores_build,stores_scaffold}.py, tests/store/{test_merge_driver_auto_install,test_migrate_layout}.py, tests/api/test_gitignore_policy.py
Validacion: ver validation.log. Test de deskops en verde. check --fast: solo identidad (preexistente).
