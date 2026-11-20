# Resultado: caché de disco vieja tras reescritura in place

run_id: exec-deskops-e-2d196cc0ac15
session: (Scion claude, sin ruta de sesión hija)
session_sha256: n/a

## Reproducción (p1)
- El repo real ya no está bloqueado (`deskops next` de la tarea sldb move da 0 bloqueos): la caché se regeneró tras el repro; no pude ver el estado viejo.
- Casos que NO fallan: reescritura con save_document_payload / Transaction.update desde otro proceso, con `where` simple y con `any(^subject: anchor_state="intact" and verdict="accepted")` (ReviewDoc con __doc_anchors__ a TaskDoc). `document_rows` solo guarda identidad (export_id/path), no payloads; su clave ya incluía roster_hash.
- Hueco encontrado: la clave de la caché compuesta en disco (`composed_disk.disk_key`) es solo stats (mtime/size de directorios y archivos de primer nivel); no incluía contenido. Si ningún stat se mueve (mismo tick de reloj, o stats restaurados), una reescritura in place no invalida. Test que lo reproduce (fallaba antes): `test_a_rewrite_in_place_inside_one_clock_tick_is_seen_by_the_next_process`.
- NO confirmado que esta sea la causa del incidente original del 2026-11-19; no es un fallo de deskops (deskops usa Transaction.update de sldb).

## Cambios
- src/sldb/store/edge_index/cache_keys.py: `roster_state(store_path)` (roster_hash por modelo).
- src/sldb/store/edge_index/composed_disk.py: la clave incluye `roster_state`.
- src/sldb/store/layout.py: `drop_disk_caches(store_path)` (borra composed/ y document_rows/).
- src/sldb/api/stores/build_store.py: `build_store` llama `drop_disk_caches` tras actualizar índices (stores build deja la caché coherente). Se puso en layout para no añadir aristas entre ejes (check ejes).
- tests/api/test_select_documents_disk.py: 2 tests nuevos.
- CHANGELOG.md.
- document_rows_disk.py: sin cambios.

## Validación
Ver validation.log. Suite completa: la corre integrate. Pruebas relacionadas corridas aparte (ver abajo).

## Revisar
- La causa raíz real del incidente no se pudo reproducir; el arreglo es defensivo (clave por contenido + invalidación en build).
Nota: git commit con identidad -c (el entorno no tiene user.name); 'deskops advance task' corrió antes del commit por un encadenado mío.
