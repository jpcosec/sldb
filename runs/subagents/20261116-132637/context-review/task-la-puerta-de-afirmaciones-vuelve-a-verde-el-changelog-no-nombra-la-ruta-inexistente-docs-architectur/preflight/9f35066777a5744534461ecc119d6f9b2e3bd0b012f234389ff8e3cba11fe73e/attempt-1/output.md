## REFORMULACION
Propósito: devolver a verde la puerta de afirmaciones corrigiendo la referencia del CHANGELOG y la violación de clean code asociada al port de pruebas de spec2viz. Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan; el CHANGELOG nombra la ruta real o describe el fixture sin forma de ruta; se añade una línea bajo `## 0.1.13 — not released yet`; el comportamiento y los tests originales no cambian. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no cambiar comportamiento, tests de comportamiento ni otras violaciones; solo tocar la línea indicada del CHANGELOG y los archivos necesarios para cumplir las reglas de clean code mediante extracción y reexportación. No es un agregado: es una tarea `task.code` ejecutable.

## AMBIGUEDADES
1. «sin la violación de task-portar-a-sldb-las-pruebas-de-spec2viz» frente a «Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo...»: no queda claro si la violación es solo la ruta inexistente del CHANGELOG o también estructura de código; obligaría a inventar qué archivos y módulos incumplen.
2. «los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport)»: no se nombra el módulo original ni sus nombres públicos; obligaría a inventar la API a preservar.
3. «otras violaciones que no sean de estos archivos»: «estos archivos» no tiene antecedente explícito; obligaría a inventar el conjunto exacto de archivos afectados.
4. «que diga que es un arreglo de clean code»: no fija redacción exacta; obligaría a inventar el texto editorial.
5. «los tests de la tarea original siguen verdes sin cambios»: no se enumeran esos tests; obligaría a inventar cuáles son.

## DRY-RUN
Hipotético, sin ejecutar: leer el TaskDoc, el bloque del CHANGELOG bajo `0.1.13`, `tests/test_clean_code_rules.py` y los módulos que el test señale; revisar `git status`/`git diff`. Cambios previstos: corregir la línea del CHANGELOG a `tests/notations/fixtures/docs/architecture/vistas.yml` o describirla sin ruta; extraer funciones/clases a módulos hermanos y reexportar desde el original; añadir la línea de clean code. Dependencias: `uv`, extras `code` y `dev`, `pytest`, `tools/check.sh`, `git`. Validaciones futuras: ejecutar los dos comandos de Validation y comprobar con `git diff` que no cambiaron tests de comportamiento.

## FUTURO
El ejecutor futuro producirá el diff y el commit conforme al alcance, y anotará en `result-summary.md` otras violaciones sin tocarlas. Un humano o nodo revisor decidirá la aceptación final del cambio y la redacción editorial si no se fija antes.
