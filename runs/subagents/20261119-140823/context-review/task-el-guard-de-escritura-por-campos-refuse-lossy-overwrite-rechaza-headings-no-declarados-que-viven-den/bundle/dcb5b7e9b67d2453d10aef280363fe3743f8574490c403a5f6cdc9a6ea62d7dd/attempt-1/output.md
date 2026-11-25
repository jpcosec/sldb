## REFORMULACION

**Propósito:** corregir la regresión de 6a4e5ec5 en el guard de escritura por campos, de modo que `refuse_lossy_overwrite` solo rechace escrituras que realmente pierdan contenido.

**Resultado:** escrituras por campos con headings no declarados dentro del valor de un campo se permiten si el render nuevo los conserva; sigue rechazándose lo que se pierde (headings o claves de frontmatter ausentes en el texto nuevo).

**Repo/superficie:** sldb; `src/sldb/api/documents/lossy_overwrite.py` (y `payload_save.py` si hace falta), `tests/api/test_structural_noise.py`, CHANGELOG. Fuera: `refuse_structural_noise` de docs track/create.

**Límites:** no ejecutar; este nodo es ejecutable (task.code), no agregado. El test de deskops es verificación externa.

## AMBIGUEDADES

1. «y payload_save.py si hace falta pasarle el texto renderizado»: no se fija si `refuse_lossy_overwrite` cambia de firma ni quién le pasa el texto nuevo; obligaría a inventar la interfaz y el punto de llamada.
2. «headings (o claves de frontmatter) del archivo actual que no aparecen en el texto que se va a escribir»: «no aparecen» no define granularidad (línea exacta, texto normalizado, posición, repeticiones). Con headings duplicados o reordenados habría que inventar la semántica de comparación.
3. «el mensaje sigue nombrándolos»: no se especifica formato ni si lista solo los ausentes; obligaría a inventar el texto esperado en los tests.
4. Scope nombra solo `tests/api/test_structural_noise.py`, pero Validation incluye «tests/api/test_transaction.py»; no se dice si ese test se actualiza o solo se ejecuta.
5. «con rutas nombradas y Task-Id»: no se fija dónde va el Task-Id en el mensaje de commit (el ritual de closeout solo define el formato general).

## DRY-RUN

**Lecturas:** `lossy_overwrite.py`, `payload_save.py`, ambos tests, CHANGELOG, `git log` de 6a4e5ec5 y su padre.

**Cambios previstos:** (p1) tests (a) campo con `### Sub` sobrevive a escritura de otro campo y (b) heading fuera de campo sigue rechazado; (p2) diff de headings/claves actuales vs texto renderizado, rechazo solo de ausentes, mensaje nombrando ausentes; (p3) CHANGELOG; (p4) `bash tools/check.sh --fast` y commit `fix(documents): ...` con Task-Id.

**Dependencias:** texto renderizado disponible en el guard; posible parámetro nuevo; gates verdes.

**Validaciones futuras:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py tests/api/test_transaction.py`; quick_gates en 0; test de deskops.

## FUTURO

El integrador verifica con `tests/test_promotion_nesting.py` de deskops (repo externo, pin 7e8492ea). Un humano/deskops actualiza Board y cierra la tarea en el commit atómico; el ritual de testing/closeout decide si procede commit y retirada de pills.
