REFORMULACION

El encargo es una tarea ejecutable (`task.code`), no un agregado. Propósito: eliminar la violación de clean code introducida por `task-sldb-version` en `source_revision` de `src/sldb/store/package_version.py`, donde hay 12 líneas de lógica frente al máximo de 10. Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan sin esa violación, manteniendo comportamiento y API pública; los tests de la tarea original siguen verdes sin cambios. Repo: `/mnt/ssd/proyectos/SLDB_1`, paquete `sldb`. Límites: tocar `package_version.py` y `CHANGELOG.md`, permitir módulos nuevos junto al original, extraer la corrida de git a `_git_describe(dir) -> str | None`, añadir una línea bajo `0.1.13`, y no cambiar comportamiento, tests de comportamiento ni otras violaciones (anotarlas en `result-summary.md`).

AMBIGUEDADES

1. “Se arregla extrayendo funciones o clases a módulos nuevos junto al original” frente a `files`, que solo lista `package_version.py` y `CHANGELOG.md`. Obliga a inventar nombre/ruta de los módulos nuevos y si `files` es exhaustivo.
2. “Extraer la corrida de git ... a una función privada _git_describe(dir) -> str | None.” No dice si `_git_describe` vive en el módulo nuevo o en `package_version`, ni si basta para dejar `source_revision` en ≤10. Obliga a inventar la estructura.
3. “se anotan en result-summary.md” no fija ruta ni formato. Obliga a inventar ubicación y esquema.
4. “git diff no toca archivos de tests de comportamiento” no enumera cuáles. Obliga a inventar el conjunto exacto si no se limita a los tests de Validation.
5. “CHANGELOG y commit” no fija mensaje ni alcance del commit. Obliga a inventar mensaje y archivos incluidos.

DRY-RUN

Un ejecutor leería `package_version.py`, `tests/test_clean_code_rules.py`, `tools/check.sh`, `CHANGELOG.md` y los tests de Validation. Crearía módulo(s) en `src/sldb/store`, movería `subprocess.run`/timeout y el manejo de `FileNotFoundError`, `TimeoutExpired` y rc≠0 a `_git_describe`, mantendría reexports desde `package_version`, editaría `CHANGELOG.md` y haría commit. Depende de `uv --frozen` con extras `code`/`dev`, `TMPDIR=/dev/shm`, pytest, bash y git. Validaría con los cuatro comandos listados y `git diff`; comprobaría que no cambió el comportamiento.

FUTURO

El ejecutor producirá el diff, el commit y, si aplica, `result-summary.md`. Un nodo de validación correrá los cuatro comandos y revisará el diff. Un humano decidirá la aceptación del cierre y el tratamiento de violaciones ajenas anotadas.
