## REFORMULACION

Encargo ejecutable (`task.code`) en el repo `sldb` (cwd `/mnt/ssd/proyectos/SLDB_1/sldb`). Propósito: reparar la regresión detectada al integrar la tarea 3f547569 (caché vieja de ReviewDoc, cerrada en 04b9d13a): (a) `src/sldb/store/layout.py` tiene 86 líneas efectivas porque `drop_disk_caches` añadió líneas; (b) `tests/api/test_select_documents_disk.py::test_a_rewrite_in_place_inside_one_clock_tick_is_seen_by_the_next_process` falla en copia limpia con `pytest -n 4` (`assert [] == ['TaskDoc:b']`). Resultado: suite completa en copia limpia con `-n 4` en verde, `layout.py` ≤80 líneas efectivas sin subir el límite, y la caché ve realmente una reescritura in place en el mismo tick de reloj, en cualquier proceso y orden. Límites: tocar solo los ficheros del Scope (`layout.py`, módulo nuevo de `drop_disk_caches`, `cache_keys.py`, `composed_disk.py`, `document_rows_disk.py`, el test y CHANGELOG); fuera de alcance subir límites de código limpio; no debilitar el test.

## AMBIGUEDADES

1. "pasa a un módulo propio o junto a las cachés que borra" y "el módulo nuevo de drop_disk_caches si hace falta": no fija ubicación ni nombre; obligaría a inventar el módulo destino.
2. "la caché de filas de documentos document_rows_disk.py, si es la que lee el test, también tiene que ver el roster como la compuesta": condicional sin criterio; obligaría a inventar qué significa "ver el roster" y la clave correcta.
3. "composed_disk.py": ruta incompleta; obligaría a adivinar el directorio.
4. "el test pasa 20 veces seguidas y con -n 4": no aclara si son 20 con `-n 4` o dos comprobaciones; obligaría a inventar la matriz.
5. "Si el test asumía algo falso, se corrige el arreglo": no define quién determina falsedad ni qué es "debilitar".
6. "commit con rutas nombradas y Task-Id": no especifica formato ni valor del Task-Id.

## DRY-RUN

Lecturas: log de integrate citado, `layout.py`, `cache_keys.py`, `composed_disk.py`, `document_rows_disk.py`, test y `test_clean_code_rules.py`, CHANGELOG. Cambios previstos: reproducir fallas (pytest filtrado y test repetido con/sin `-n 4`), extraer `drop_disk_caches` a módulo ≤80 líneas, corregir clave de caché, repetir test 20 veces, `bash tools/check.sh --fast`, commit con rutas y Task-Id. Dependencias: pytest, TMPDIR, semántica de reloj/mtime, roster compuesto. Validaciones futuras: comando de Validation, repetición, quick_gates; suite completa la corre integrate. Nada ejecutado.

## FUTURO

Integrate ejecuta la suite completa y cierra; un humano decide ubicación del módulo y si la premisa del test era falsa; el commit queda a cargo del ejecutor.
