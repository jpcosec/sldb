## REFORMULACION

Propósito: desbloquear IR08/IR09 exponiendo en `sldb.api` los facts de código que hoy solo viven en `sldb.code.scan`. Resultado: un paquete nuevo `sldb.api.code` con `code_facts(root, paths=None)` que devuelve facts de archivo o de árbol, cada uno con `path`, `span` (líneas inicio/fin), `source_hash`, `kind`, `qualified_name`, `signature`, `doc`, `relations` y `attrs`; además `write_anchor` público en `sldb.api.anchors`. Repo: `SLDB_1`, tocando `src/sldb/api/anchors/__init__.py`, un paquete nuevo bajo `src/sldb/api/`, tests y `CHANGELOG.md`. Límites: no crear facts nuevos (C3/C4), no cambiar la forma de los facts, no tocar la CLI.

## AMBIGUEDADES

1. «devuelve la lista de facts» frente a «la respuesta lo lista en un campo aparte (skipped)». Obliga a inventar si `code_facts` retorna una lista o un objeto `{facts, skipped}`; ambos no caben en la misma firma.
2. «Tests de la API con un árbol de prueba que mezcle .py, .tsx y .sql» frente a «tests/api/test_anchors.py» y «Tests de la API nueva en tests/api/test_anchors.py». Obliga a decidir si los tests van en ese archivo —cuyo encabezado declara las reglas de anchoring— o en uno nuevo.
3. «cada fact … source_hash del archivo» sin indicar cómo se obtiene el hash ni si `fact()` ya lo trae. Obliga a inventar algoritmo, codificación y momento de cálculo.
4. «aviso a IR» en Done When, sin canal ni formato. Obliga a inventar el destinatario y el medio.
5. «todo el árbol» sin precisar extensiones ni exclusión de directorios; aunque remite a `find_files`, obliga a decidir si se recorren solo lenguajes soportados y si se respeta `node_modules`.

## DRY-RUN

Lecturas: `sldb/code/scan.py` (`scan_file`, `scan_tree`), `sldb/code/files.py` (`find_files`), `sldb/code/facts.py`, cálculo de `source_hash`, `sldb/api/anchors/__init__.py`, `tests/api/test_anchors.py`. Cambios previstos: crear `src/sldb/api/code/__init__.py` con `code_facts` y `__all__`; añadir `write_anchor` al `__all__` de anchors; tests con `.py`, `.tsx`, `.sql`; `CHANGELOG.md`. Dependencias: extras `code` y `dev`, runtime tree-sitter y fixtures SQL/TSX. Validaciones futuras: los cuatro comandos del TaskDoc, de menor a mayor alcance.

## FUTURO

El commit, el cierre con `deskops closeout` y el aviso a IR corresponden a nodos posteriores o a decisión humana; la aceptación de la forma de retorno y del archivo de tests requiere decisión humana si no se resuelve antes.
