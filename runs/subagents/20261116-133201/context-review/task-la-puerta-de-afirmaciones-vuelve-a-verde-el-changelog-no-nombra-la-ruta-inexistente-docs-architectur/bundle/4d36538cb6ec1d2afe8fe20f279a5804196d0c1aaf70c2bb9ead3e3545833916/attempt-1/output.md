## REFORMULACION
Encargo: devolver a verde la puerta de afirmaciones de sldb. Propósito: eliminar la violación introducida por `task-portar-a-sldb-las-pruebas-de-spec2viz` (bee4ae7f). Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan; los tests de comportamiento originales siguen verdes sin cambios; CHANGELOG corrige la ruta inexistente y añade una línea de arreglo clean code bajo `## 0.1.13 — not released yet`. Repo: `/mnt/ssd/proyectos/SLDB_1` (sldb). Límites: no cambiar comportamiento ni API pública (reexport desde el módulo original), no tocar otras líneas del CHANGELOG ni otras violaciones (solo anotarlas en `result-summary.md`). Es un nodo ejecutable (`task.code`), no un agregado.

## AMBIGUEDADES
1. «Se arregla extrayendo funciones o clases a módulos nuevos junto al original»: no nombra qué archivos ni módulos violan las reglas; obligaría a inventar el conjunto de módulos a refactorizar (¿los siete `tests/notations/test_ported_from_spec2viz_*.py`?).
2. «CHANGELOG.md ... nombra como ruta del repo un vistas.yml ... que no existe» frente a «Se arregla extrayendo funciones o clases a módulos nuevos»: el Rationale atribuye el fallo solo al CHANGELOG y el Scope ordena refactor de código; obligaría a inventar si hay refactor o solo edición textual.
3. «los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport)»: no identifica el módulo original ni su API; obligaría a inventar qué símbolos reexportar.
4. «Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code»: no fija redacción ni confirma que ese encabezado exista; obligaría a inventar texto y posición.
5. «los tests de la tarea original siguen verdes sin cambios»: no enumera esos tests; obligaría a inventar el alcance de la comprobación.

## DRY-RUN
Lecturas: `CHANGELOG.md`, `tests/test_clean_code_rules.py`, los siete `tests/notations/test_ported_from_spec2viz_*.py`, `tools/check.sh`, `git log`/`git show` de bee4ae7f. Cambios previstos: corregir la línea del CHANGELOG a `tests/notations/fixtures/docs/architecture/vistas.yml` (o descripción sin ruta) y añadir la línea bajo 0.1.13; si se confirma el refactor, extraer clases/funciones a módulos nuevos del mismo paquete con reexport. Dependencias: `uv`, `pytest`, `bash`, git. Validaciones futuras: los dos comandos de Validation y `git diff` para confirmar que no cambian tests de comportamiento. Nada se ejecuta aquí.

## FUTURO
Un humano o nodo de contexto resuelve las ambigüedades 1–5 antes de ejecutar. El ejecutor produce el diff y, si `check.sh` muestra otras violaciones, las anota en `result-summary.md`. El ritual de testing valida; el de closeout hace commit atómico, actualiza el Board vía `deskops closeout` y retira la tarea.
