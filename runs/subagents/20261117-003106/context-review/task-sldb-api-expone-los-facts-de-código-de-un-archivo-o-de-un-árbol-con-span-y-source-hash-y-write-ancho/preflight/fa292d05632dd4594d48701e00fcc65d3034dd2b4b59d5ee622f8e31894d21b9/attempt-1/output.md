## REFORMULACION

Encargo: en el repo SLDB_1, crear dentro de `src/sldb/api/` un paquete público `code` que exponga `code_facts(root, paths=None)`, reutilizando `sldb.code.scan.scan_file`/`scan_tree` sin duplicar lógica. Debe devolver los facts existentes (`fact()` de `sldb.code.facts`) de un archivo, de una lista de rutas relativas a `root`, o de todo el árbol si `paths is None`, con `path`, span de líneas, `source_hash`, `kind`, `qualified_name`, `signature`, `doc`, `relations` y `attrs`; los archivos sin gramática se omiten y se informan aparte. Además, añadir `write_anchor` al `__all__` de `sldb.api.anchors`, probar la API con un árbol que mezcle `.py`, `.tsx` y `.sql`, actualizar `CHANGELOG.md` y ejecutar las validaciones indicadas. Fuera de alcance: facts nuevos (C3/C4), cambiar la forma de los facts y la CLI. Resultado observable: imports públicos funcionando, facts con span y `source_hash` no vacíos, tests y `check.sh --fast` en verde.

## AMBIGUEDADES

1. «la respuesta lo lista en un campo aparte (skipped)»: no define si `code_facts` devuelve una lista, una tupla o un objeto con `facts` y `skipped`; obliga a inventar el contrato de retorno.
2. «span (líneas de inicio y fin)»: no aclara base 0/1 ni inclusividad; obliga a inventar convención.
3. «Tests de la API nueva en tests/api/test_anchors.py»: el archivo sugiere anclas, no facts de código; obliga a decidir si se añaden ahí o en un archivo nuevo.
4. «cada uno con path, span [...] source_hash del archivo»: no indica si `path` es relativo a `root` o absoluto; obliga a inventar.
5. «si un archivo no tiene gramática disponible, se omite»: no define si un archivo ilegible o con error también va a `skipped`; obliga a inventar.

## DRY-RUN

Lecturas hipotéticas: `src/sldb/code/scan.py`, `files.py`, `facts.py`, `src/sldb/api/anchors/__init__.py`, tests citados y `CHANGELOG.md`. Cambios previstos: nuevo `src/sldb/api/code/__init__.py` con `code_facts` y `__all__`; `write_anchor` en `__all__` de anchors; tests en `tests/api/test_anchors.py`; entrada de CHANGELOG. Dependencias: `scan_file`, `scan_tree`, `find_files`, `fact()` y cálculo de `source_hash`. Validaciones futuras: los cuatro comandos de Validation y comprobación de imports públicos. Sin ejecutar nada.

## FUTURO

Un humano decide el mensaje/commit, la versión del CHANGELOG y el aviso a IR; otro nodo (C3/C4) añadirá facts nuevos.
