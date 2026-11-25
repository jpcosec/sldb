## REFORMULACION
Encargo: corregir en el repo `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`) la regresión de `6a4e5ec5` en el guard de escritura por campos `refuse_lossy_overwrite`. El guard debe rechazar una escritura solo cuando pierda contenido real: headings o claves de frontmatter presentes en el archivo actual y ausentes en el texto que se escribirá. Los headings dentro del valor de un campo que el render conserva no deben bloquear. Resultado esperado: tests nuevos en `tests/api/test_structural_noise.py`, tests existentes de `6a4e5ec5` y `tests/test_promotion_nesting.py` de `deskops` en verde. Límites: tocar `src/sldb/api/documents/lossy_overwrite.py` y, si hace falta, `payload_save.py`; añadir tests; actualizar CHANGELOG; no cambiar `refuse_structural_noise` de docs track/create.

## AMBIGUEDADES
1. «status: draft» y «current_node: ritual-execution»: no aclara si la tarea está lista para ejecución o solo en preflight; obligaría a inventar la condición de arranque.
2. «p1: tests que fallen antes»: no fija nombres, fixtures ni aserciones exactas; obligaría a inventar el diseño concreto de los tests.
3. «y payload_save.py si hace falta»: no define el criterio de “hace falta”; obligaría a decidir e inventar si se cambia la interfaz para pasar el texto renderizado.
4. «El integrador verifica con el test de deskops»: no indica comando, ruta ni revisión de deskops; obligaría a inventar el procedimiento de verificación externa.

## DRY-RUN
Lecturas previstas: TaskDoc, `lossy_overwrite.py`, `payload_save.py`, `tests/api/test_structural_noise.py`, `tests/api/test_transaction.py`, CHANGELOG y referencias de la regresión. Cambios previstos: añadir tests rojo→verde para heading dentro de valor conservado y para heading no declarado perdido; comparar headings/claves actuales contra el texto nuevo y rechazar solo ausentes; ajustar mensaje; CHANGELOG. Dependencias: contexto de `6a4e5ec5`, renderizado disponible y repo `deskops` para verificación. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py tests/api/test_transaction.py`, `bash tools/check.sh --fast` en 0, test de deskops y commit con rutas y `Task-Id`. No se ejecuta nada.

## FUTURO
Otro nodo o el integrador aportará la ejecución real de la suite de `deskops` y su resultado. Un humano decidirá si el cambio de `payload_save.py` es aceptable si los tests no bastan para determinarlo.
