## REFORMULACION
Nodo `task.code` ejecutable, no agregado. Encargo: modificar `docs create` para que `-o` con ruta relativa se resuelva contra el directorio actual, o avise claramente si se resuelve contra otro lugar; añadir/ajustar un test y hacerlo pasar. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: solo el comando `docs create` y un test; fuera de alcance “render y fields”.

## AMBIGUEDADES
1. “la resuelve contra el directorio actual, o avisa claramente si la resuelve contra otro lado”: no queda claro si se exige resolver contra el cwd o basta advertir. Obliga a inventar el comportamiento esperado.
2. “Test desde un cwd distinto de la raiz”: no concreta qué cwd, cómo prepararlo ni qué aserciones usar. Obliga a inventar fixture y expectativas.
3. “Arreglo”: no identifica módulo, función ni punto de resolución de rutas. Obliga a inventar la superficie de cambio.
4. “El comando docs create y un test”: no define ruta del comando ni sintaxis exacta de `-o`. Obliga a inferir la interfaz.

## DRY-RUN
Lecturas previstas: TaskDoc, implementación de `docs create`, `tests/test_docs_create_output_path.py` y utilidades de rutas. Cambios previstos: ajustar resolución/aviso de `-o` relativa y completar el test. Dependencias: `.venv`, `pytest`, `TMPDIR`. Validación futura: ejecutar exactamente `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_docs_create_output_path.py`. No se ejecuta nada ahora.

## FUTURO
Un ejecutor posterior implementará el cambio y correrá el test; un humano validará el cierre y, si corresponde, aclarará previamente las ambigüedades.
