## REFORMULACION

El nodo encarga, en `/mnt/ssd/proyectos/SLDB_1`, exponer públicamente los facts de código para desbloquear IR08/IR09: crear el paquete `sldb.api.code` con `code_facts(root, paths=None)`, que devuelve `{"facts": [...], "skipped": [...]}` reutilizando `scan_file`/`scan_tree`, con facts que conservan su forma y traen `path`, `span` y `source_hash` no vacíos; además, hacer público `write_anchor` desde `sldb.api.anchors`, probar con `.py`, `.tsx` y `.sql` en `tests/api/test_anchors.py`, actualizar `CHANGELOG` y validar. Límites: no crear facts nuevos, no cambiar la forma de los facts ni tocar la CLI. El aviso a IR corresponde al coordinador. Nodo ejecutable, no agregado.

## AMBIGUEDADES

1. «si un archivo no tiene gramática disponible, se omite y la respuesta lo lista en un campo aparte (skipped)»: no define archivos con gramática pero parseo inválido, error de lectura o excepción del reader; obligaría a inventar si `code_facts` propaga, omite o añade a `skipped`.
2. «code_facts(root, paths=None) devuelve un dict» y «rutas relativas a root»: no define rutas inexistentes, absolutas, duplicadas, directorios o fuera de `root`; obligaría a inventar validación, normalización y errores.
3. «garantizando que span y source_hash vengan llenos» / «solo garantiza que no venga vacío»: no dice qué hacer si el fact o reader no los trae; obligaría a inventar si falla, omite o rellena.
4. «un paquete nuevo code dentro de sldb.api» frente a `files`, que no incluye el archivo nuevo; obligaría a inventar la ruta exacta del paquete.

## DRY-RUN

Sin ejecutar: un ejecutor leería `sldb.code.scan`, `sldb.code.files`, `sldb.code.facts`, los readers y `src/sldb/api/anchors/__init__.py`; después crearía el paquete `sldb.api.code` con `code_facts`, añadiría el import/export de `write_anchor` y su entrada en `__all__`, ampliaría `tests/api/test_anchors.py` y `CHANGELOG.md`. Dependencias: extra `code`, runtime tree-sitter y gramáticas Python/TSX/SQL. Validaciones futuras: los cuatro comandos del TaskDoc.

## FUTURO

El coordinador enviará el aviso a IR por `deskops message send`; IR08/IR09 consumirán la API. El cierre, commit y retirada del Board corresponden al flujo de closeout.
