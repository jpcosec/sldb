## REFORMULACION

Propósito: desbloquear IR08/IR09 exponiendo públicamente los facts de código que hoy solo viven en `sldb.code.scan.scan_file`/`scan_tree`. Resultado: un paquete nuevo `sldb.api.code` con `code_facts(root, paths=None)` que devuelve `{"facts": [...], "skipped": [...]}` reutilizando los scanners, con `path` relativo, `span` y `source_hash` no vacíos; `write_anchor` añadido al `__all__` de `sldb.api.anchors`; tests en `tests/api/test_anchors.py`; CHANGELOG. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no crear facts nuevos (C3/C4), no cambiar la forma de los facts, no tocar la CLI; `paths` son rutas relativas a `root` y solo se escanean archivos con gramática.

## AMBIGUEDADES

1. "de los archivos dados (rutas relativas a root)": no aclara si `paths` admite directorios; obligaría a inventar si se expanden recursivamente o se tratan como error.
2. "si un archivo no tiene gramática disponible, se omite y la respuesta lo lista en un campo aparte (skipped)": no cubre rutas inexistentes, fuera de `root` o no-fichero; obligaría a inventar si van a `skipped`, se ignoran o lanzan.
3. "garantizando que span y source_hash vengan llenos": no define qué hacer si un reader devuelve vacío; obligaría a inventar entre omitir, lanzar o rellenar.
4. "skipped la lista de rutas (relativas a root, ordenadas)": no fija criterio de orden; obligaría a inventar clave (lexicográfica vs. recorrido).
5. "CHANGELOG y commit": no fija formato de entrada ni mensaje; obligaría a inventar convención.

## DRY-RUN

Lecturas previstas: TaskDoc, `src/sldb/api/anchors/__init__.py`, `tests/api/test_anchors.py`, `CHANGELOG.md`, `sldb/code/scan.py`, `sldb/code/files.py`, `sldb/code/facts.py`. Cambios: crear `src/sldb/api/code/__init__.py` con `code_facts` y `__all__`; añadir `write_anchor` a `__all__`; tests en `test_anchors.py` con árbol `.py`/`.tsx`/`.sql` (span, hash, skipped, `paths`); CHANGELOG. Dependencias: extras `code` (tree-sitter) y scanners existentes. Validaciones futuras: los cuatro comandos de Validation (pytest y `check.sh --fast`), sin ejecutar.

## FUTURO

El coordinador envía el aviso por `deskops message send` a IR. Un humano u otro nodo decide commit, cierre y merge. Las tareas C3/C4 aportan facts nuevos; la CLI queda fuera.
