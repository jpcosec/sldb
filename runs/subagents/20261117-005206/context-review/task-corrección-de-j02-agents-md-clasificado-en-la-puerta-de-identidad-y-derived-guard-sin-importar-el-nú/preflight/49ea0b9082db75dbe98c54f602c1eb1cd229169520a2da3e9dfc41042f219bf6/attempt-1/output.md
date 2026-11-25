REFORMULACION
Nodo ejecutable `task.code` (no agregado). Propósito: corregir dos fallos de j02: `AGENTS.md` sin clasificar en la puerta de identidad y `derived_guard` importando el núcleo fuera de los seams. Resultado: `tools/check.sh --fast` y `tests/test_store_seams.py` pasan con j02 integrado, sin cambiar el comportamiento del merge driver, de rebuild-index ni el mensaje de error. Repo: `/mnt/ssd/proyectos/SLDB_1` (SLDB). Límites: tocar `tools/check_identity.py` y el guard de índices derivados en `sldb.store.io`; no cambiar la lista de seams del test ni otros archivos de j02.

AMBIGUEDADES
1. “usar la excepción que ya usan los demás módulos de sldb.store.io (leer cómo lo hacen) o mover la importación a un seam permitido según tests/test_store_seams.py”: no identifica módulos, patrón ni criterio de elección; obligaría a inventar cuál es “la excepción” y qué alternativa elegir.
2. “el error y su mensaje no cambian”: no cita el mensaje ni la clase exactos; obligaría a inferirlos del código de j02.
3. “con un comentario que diga que es la guía de procedimiento para agentes (merge de .sldb)”: fija la idea, no el texto exacto; obligaría a redactar el comentario.

DRY-RUN
Lecturas: `tests/test_store_seams.py`, `tools/check_identity.py`, `sldb/store/io/derived_guard.py`, módulos vecinos de `sldb.store.io` y tests citados. Cambios previstos: añadir `AGENTS.md` a `EXEMPT` con comentario; sustituir o trasladar el import de `sldb.core.exceptions` en `derived_guard` al patrón permitido, preservando error y mensaje. Dependencias: j02/commit `7dbb6bc9` presente, entorno `uv --frozen` y `TMPDIR=/dev/shm`. Validaciones futuras: los cinco comandos de Validation (`test_store_seams.py`, `test_update_fault_tolerance.py`, `test_merkle_shards.py`, `test_clean_code_rules.py` y `check.sh --fast`). Sin ejecutar nada.

FUTURO
El ejecutor futuro aplicará los cambios y ejecutará las validaciones; el tester/integrador producirá evidencia de cierre y el commit; un humano decidirá la aceptación final de j02 y cualquier discrepancia entre archivos citados y validaciones.
