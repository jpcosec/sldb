## REFORMULACION

Encargo ejecutable (task.code) en el repo `sldb`: hacer que la instalación del merge driver de sldb sea automática al preparar un store y que su ausencia se detecte. Propósito: evitar conflictos en `.sldb/` irresolubles por CLI. Resultado esperado: (1) `init_store`, `scaffold_store` y `build_store` invocan `install_merge_driver` (src/sldb/api/stores/merge_driver_install.py) cuando el store está en un repo git, de forma idempotente, sin efecto fuera de git y avisando sin romper si git falla; (2) `stores check` reporta hallazgo `merge-driver-missing` (warning, fix `sldb stores merge-driver --install`) si faltan líneas de `.gitattributes` o claves `merge.sldb.*`. Límites: tocar init_store.py, scaffold_store.py, build_store.py, store_check.py (o módulo de hallazgos), tests y CHANGELOG; fuera: deskops y el driver mismo.

## AMBIGUEDADES

1. «tests en tests/api/ o tests/store/» — no fija ubicación; obligaría a inventar cuál es la canónica.
2. «o el módulo de hallazgos que use» — no nombra el módulo; obligaría a inventar su ruta y API.
3. «cuando el store está dentro de un repo git» — no define detección (¿`git rev-parse`, subida de directorios?); obligaría a inventar el criterio.
4. «si git falla avisan sin romper el comando» — no dice canal del aviso (stderr, warning estructurado, log); obligaría a inventar el mecanismo.
5. «nivel warning, con fix» — no da el esquema del hallazgo; obligaría a inventar campos y formato.
6. «CHANGELOG» — no indica archivo ni formato de entrada; obligaría a inventar convención.
7. Validation solo cita `tests/store/test_stores_build.py` pese a cubrir init/check; obligaría a inventar el resto de comandos de validación.

## DRY-RUN

Lecturas: los cuatro módulos citados, `merge_driver_install.py`, tests existentes de stores y CHANGELOG. Cambios previstos: tests nuevos primero (init, build, idempotencia, fuera de git, check antes/después); llamadas a `install_merge_driver` envueltas en manejo de error; hallazgo nuevo en check; entrada de CHANGELOG. Dependencias: git disponible en el entorno de test, repo temporal. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py`, suite completa vía integrador, `bash tools/check.sh --fast` en 0, commit con rutas nombradas y `Task-Id`.

## FUTURO

El integrador corre la suite completa y la de deskops; un humano decide ubicación de tests, esquema del hallazgo y convención de CHANGELOG.
