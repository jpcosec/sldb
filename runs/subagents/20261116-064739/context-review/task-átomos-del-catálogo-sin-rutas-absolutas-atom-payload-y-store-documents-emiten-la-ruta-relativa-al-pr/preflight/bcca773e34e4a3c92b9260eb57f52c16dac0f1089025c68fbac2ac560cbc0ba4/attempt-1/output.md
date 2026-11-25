## REFORMULACION
Tarea de código ejecutable (no agregado) en el repo SLDB_1. Propósito: evitar que el catálogo incruste rutas absolutas de máquina. Resultado: `atom_payload.py` emite `"path"` relativo a la raíz del proyecto del store, en POSIX, y sin `"store"`; `store_documents.py` emite `"path"` como `doc.path` POSIX y sustituye `"store"` por `"store_name"`; adaptar lectores internos; test que compruebe ausencia de `str(tmp_path)` y ruta relativa; nota en CHANGELOG bajo `## 0.1.13 — not released yet`; aviso a IR. Límites: no tocar specir, no hacer push; el commit lo hace el coordinador; informe en `runs/subagents/<run-dir>/result-summary.md`; líneas orientativas se localizan por función.

## AMBIGUEDADES
1. “la ruta relativa al proyecto del store que tiene el documento” y “project_root del store”: no define cómo obtiene `atom_payload` ese `project_root` ni qué hacer si el documento no pertenece a un store; obligaría a inventar la resolución.
2. “se quita la clave "store"” frente a “"store" se reemplaza por "store_name" (que ya está)”: no aclara si `atom_payload` debe emitir también `store_name` o solo eliminar `store`, ni el esquema final; obligaría a inventar el contrato.
3. “si alguno necesita la ruta absoluta, la recompone con project_root”: no dice cómo decidir esa necesidad ni de dónde sale `project_root` en cada lector; obligaría a inventar el criterio.
4. “el payload de un store en tmp_path no contiene str(tmp_path) en ningún valor”: no precisa si “payload” es la lista de átomos, el dict completo o valores anidados; obligaría a inventar el alcance del assert.
5. “Aviso a IR” y “specir (repo IR)”: no aclara si el destinatario de `deskops message send --to` es `IR` o `specir`; obligaría a inventar el nombre.

## DRY-RUN
Lecturas: TaskDoc, `atom_payload.py`, `store_documents.py`, `tests/matching/test_matching_explicit.py`, `CHANGELOG.md`, usos vía grep de `atom_payload|store_documents|atoms_from_documents` y de `["store"]|["path"]|get("store")|get("path")` en `src/sldb/api/matching` y `src/sldb/api/notations`. Cambios previstos: reemplazar claves y recomponer rutas internas; añadir test; nota de CHANGELOG. Dependencias: fixtures/helpers del test o `sldb.api` en `tmp_path`; `project_root` disponible; `deskops` para el aviso. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/matching/` y `TMPDIR=/dev/shm pytest -q tests/notations/test_spec_catalog_sync.py`; revisar que ningún valor contenga `tmp_path`. Sin ejecutar nada.

## FUTURO
El coordinador ejecutará `deskops closeout commit` con el título corto y decidirá el cierre. IR/specir adaptará su consumo cuando reciba el aviso. La revisión humana aceptará o rechazará el resultado y el CHANGELOG.
