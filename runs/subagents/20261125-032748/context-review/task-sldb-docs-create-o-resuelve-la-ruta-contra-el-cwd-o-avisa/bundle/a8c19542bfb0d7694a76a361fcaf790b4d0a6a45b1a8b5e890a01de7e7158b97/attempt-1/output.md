## REFORMULACION
Encargo ejecutable (`task.code`, `current_node: ritual-execution`): corregir en `sldb docs create` la resolución de una ruta relativa pasada con `-o`, de modo que se resuelva contra el cwd o se avise claramente si se resuelve contra otro lugar. Resultado esperado: cambio en el comando y test `tests/test_docs_create_output_path.py` pasando. Repo implícito: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: solo `docs create` y un test; fuera “render y fields”; validación limitada al test indicado.

## AMBIGUEDADES
1. “la resuelve contra el directorio actual, o avisa claramente si la resuelve contra otro lado”: no fija si el comportamiento correcto es resolver contra cwd o conservar otra resolución con aviso; obligaría a inventar la política y el criterio de aceptación.
2. “El comando docs create y un test”: no nombra archivo/módulo del comando ni punto de entrada; obligaría a descubrir o inventar la superficie de cambio.
3. “avisa claramente”: no define canal, texto, formato ni exit code; obligaría a inventar la UX y sus aserciones.
4. “Test desde un cwd distinto de la raiz”: no concreta cwd, ruta relativa usada ni resultado esperado; obligaría a inventar fixture y expectativas.

## DRY-RUN
Sin ejecutar: un ejecutor futuro leería el TaskDoc, rituales enrutados, código de `docs create`, tests existentes y git history. Previstos: localizar el manejo de `-o`, ajustar resolución/aviso y crear o actualizar `tests/test_docs_create_output_path.py`. Dependencias: entorno `.venv`, `TMPDIR=/mnt/ssd/tmp/sldb1` y un cwd temporal distinto de la raíz. Validación futura: ejecutar exactamente `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_docs_create_output_path.py`, comprobando ruta resultante o aviso según la semántica que se aclare.

## FUTURO
Otro nodo ejecutor producirá el parche y el test; testing/closeout validarán, actualizarán Board/CHANGELOG si aplica y commitearán. Un humano deberá aprobar la semántica elegida si el producto exige una política concreta.
