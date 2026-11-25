## REFORMULACION
Encargo ejecutable `task.code` en el repo SLDB: eliminar rutas absolutas del payload de átomos y de `store_documents`. Resultado: en `atom_payload.merge_atom`, cada átomo conserva `id`, `body`, `path`, `tags`, `provenance`; `path` es `doc_path` relativo a `project_root(store_path)` en posix, o el nombre del archivo si no está bajo la raíz; desaparece `store`. En `store_documents._document`, `path` es `doc.path` posix y desaparece `store`, manteniendo `store_name`. Adaptar lectores internos que usen rutas absolutas. Añadir test en `tests/matching/test_matching_explicit.py` y entrada en `CHANGELOG.md`. Límites: no tocar specir; no hacer commit ni push; líneas orientativas; aviso a IR al cerrar; informe en `result-summary.md`.

## AMBIGUEDADES
1. “Un lector interno de sldb que hoy use la ruta absoluta la recompone con project_root de su store y la ruta relativa.” Si el lector solo recibe el payload sin `store`, no se indica cómo obtener “su store”; obligaría a inventar el mapeo desde `store_name` o desde el documento.
2. “El assert del test recorre recursivamente todos los valores str del dict completo que devuelve la función” no nombra “la función”; obligaría a decidir si se prueba `merge_atom`, `_document` u otra API pública.
3. “si doc_path no está bajo esa raíz, se usa el nombre del archivo” no precisa si “nombre” es `basename` o una ruta relativa alternativa; obligaría a fijar el fallback exacto.

## DRY-RUN
Leería `atom_payload.py`, `store_documents.py`, `test_matching_explicit.py`, `CHANGELOG.md` y haría el grep indicado para localizar lectores. Cambiaría las claves y calcularía `path` posix relativo con `project_root`; adaptaría lectores recomponiendo absolutas cuando necesiten el filesystem. Añadiría el test recursivo sobre todos los `str` del dict y la nota de CHANGELOG. Dependencias: `sldb.store.layout.project_root`, `store_name` y fixtures existentes. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/matching/` y `TMPDIR=/dev/shm pytest -q tests/notations/test_spec_catalog_sync.py`, sin ejecutar aquí.

## FUTURO
El coordinador hará `deskops closeout commit` y no push. Otro nodo o humano decidirá la aceptación y el aviso a IR; si el repo no está registrado, quedará como línea en `result-summary.md`. Specir adaptará su consumo fuera de este encargo.
