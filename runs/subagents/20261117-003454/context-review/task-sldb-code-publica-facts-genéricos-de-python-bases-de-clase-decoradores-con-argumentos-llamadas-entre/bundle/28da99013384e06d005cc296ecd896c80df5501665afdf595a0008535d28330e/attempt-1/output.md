## REFORMULACION

Propósito: que `sldb.code` publique facts sintácticos genéricos de Python —bases de clase, decoradores con argumentos, llamadas entre símbolos y asignaciones con llamada— sin conocer ningún framework. Resultado: readers nuevos en módulos del paquete `sldb.code`, integración en `scan_file` para `.py`, fixture Django/DRF mínimo, tests y CHANGELOG; si cambia la forma de los facts existentes, se sube la normalización. Repo: SLDB_1; superficies nombradas: `src/sldb/code/scan.py`, `readers.py`, `tests/selfdoc/test_treesitter_symbols.py`, `CHANGELOG.md`. Límites: no interpretar Django/DRF (eso es specIR), no resolver tipos ni imports de llamadas, no TS/JS.

## AMBIGUEDADES

1. «un kind nuevo assignment ... así salen urlpatterns = [path(...)], router.register(...) como llamada de módulo (kind call, con func y args)»: no queda claro si una llamada suelta de módulo es `call` y una asignación es `assignment`, ni qué pasa con `path()` dentro de una lista. Obliga a inventar el kind y la relación entre ambos.
2. «cuyo valor es una llamada o un literal simple»: «literal simple» no está definido. Obliga a inventar si cubre strings, números, listas, dicts o tuples.
3. «attrs.decorators: lista de {name, args, kwargs} con los argumentos como texto normalizado»: no especifica la normalización. Obliga a inventar si se usa `py_norm` y con qué reglas.
4. «texto calificado tal cual» para bases frente a «texto normalizado» para decoradores: criterios distintos sin justificar. Obliga a inventar el criterio de cada campo.
5. «si cambia la forma de los facts existentes, se sube y se dice en el CHANGELOG»: no indica versión ni campo donde se registra. Obliga a inventar el valor de normalización.
6. «las llamadas que hace cada función o método a otros nombres»: no aclara lambdas, comprehensions, cuerpos de clase, decoradores ni asignaciones. Obliga a inventar el alcance.
7. «attrs.calls con línea de cada llamada»: no define línea inicial/final ni formato. Obliga a inventar el esquema.
8. La lista `files:` omite `facts.py`, `fingerprints.py` y las rutas del fixture que sí nombra «Implementation Path». Obliga a inventar los archivos tocados.

## DRY-RUN

Lecturas hipotéticas: `readers.py`, `scan.py`, `facts.py`, `fingerprints.py`, tests existentes y fixture. Cambios previstos: módulos nuevos de readers (bases, decoradores, llamadas, asignaciones), capturas tree-sitter adicionales, integración en `scan_file` para `.py`, relaciones `extends`/`calls`, kind `assignment`, fixture Django/DRF, tests y CHANGELOG. Dependencias: runtime tree-sitter, `Ids`, `fact`/`rels`, `py_norm`, regla de 80 líneas, pill `keep-sldb-generic`. Validaciones futuras: los siete comandos de Validation, anclas sin cambio de estado, CHANGELOG y commit, aviso a IR.

## FUTURO

specIR interpreta los facts como Django/DRF. Un humano o coordinador decide la versión de normalización y el alcance exacto de las llamadas; el closeout realiza commit y aviso a IR.
