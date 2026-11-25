REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: reparar el integrate fallido de 3f547569. Resultado: suite completa de sldb pasa en copia limpia con `pytest -n 4`; `layout.py` queda en ≤80 líneas efectivas sin subir el límite; `drop_disk_caches` sale de `layout.py`; la caché observa una reescritura in place en el mismo tick, en cualquier proceso y orden; si el test asumía algo falso, se corrige el arreglo, no se debilita el test. Repo: sldb. Límites: `src/sldb/store/layout.py`, módulo nuevo de `drop_disk_caches` si hace falta, `cache_keys.py`, `composed_disk.py`, `document_rows_disk.py`, `tests/api/test_select_documents_disk.py` y CHANGELOG; fuera, subir límites de código limpio.

AMBIGUEDADES
1. “drop_disk_caches pasa a un módulo propio o junto a las cachés que borra” deja abierta la ubicación; obligaría a inventar módulo, ruta e imports.
2. “la caché de filas de documentos document_rows_disk.py, si es la que lee el test” no identifica con certeza la caché culpable; obligaría a inventar cuál clave/almacén corregir.
3. La Validación solo nombra dos archivos, pero Done When exige “20 veces seguidas y con -n 4; la suite completa la corre integrate”; obligaría a decidir si este nodo ejecuta repeticiones y suite completa.
4. “en cualquier proceso y orden” no fija matriz de procesos/orden; obligaría a inventar escenarios y criterio de suficiencia.
5. “el test pasa 20 veces seguidas y con -n 4” no aclara si son 20 repeticiones bajo `-n 4` o dos comprobaciones; obligaría a inventar el comando exacto.

DRY-RUN
Un ejecutor futuro leería Board, rituales, TaskDoc y archivos nombrados; auditaría git para confirmar 04b9d13a; reproduciría ambas fallas con los comandos de p1. Extraería `drop_disk_caches` de `layout.py`, ajustaría claves/invalidación en `cache_keys.py`, `composed_disk.py` y `document_rows_disk.py`, corregiría el test solo si su premisa es falsa y actualizaría CHANGELOG. Dependencias: pytest, xdist/`-n 4`, `TMPDIR`, git. Validaciones futuras: comando de Validación, repeticiones/`-n 4`, `quick_gates` y suite completa en integrate. Sin ejecutar nada.

FUTURO
Integrate ejecuta la suite completa en copia limpia y confirma el resultado conjunto. Deskops/closeout valida commit, Task-Id, CHANGELOG, árbol limpio y gates; un humano revisa que no se haya debilitado el test.
