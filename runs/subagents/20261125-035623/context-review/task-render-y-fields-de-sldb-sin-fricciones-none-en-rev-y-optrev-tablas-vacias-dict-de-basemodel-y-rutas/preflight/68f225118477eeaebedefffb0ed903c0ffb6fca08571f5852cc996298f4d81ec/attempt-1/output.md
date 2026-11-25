REFORMULACION
Encargo del nodo: corregir fricciones de render/extract y fields update cuando `rev` u `optrev` valen `None`. Resultado esperado: un `rev=None` renderiza `null` y `extract` lo devuelve como `None`; un `optrev=None` puede actualizarse con `fields update <doc> <campo> <valor>` y queda `x`; tests nuevos en `tests/test_rev_optrev_none.py`. Repo: `SLDB_1/sldb` (inferido de cwd y de la ruta de validación). Límites: solo `rev`/`optrev` con `None` y `fields update` de un path con valor `None`; fuera tablas, `BaseModel` y `docs create`; validación limitada a ese archivo de test.

AMBIGUEDADES
1. “Render y fields de sldb sin fricciones: None en rev y optrev, tablas vacias, dict de BaseModel y rutas relativas de docs create” frente a “Fuera: tablas, BaseModel, docs create.” Obliga a inventar si el título amplía el alcance o si prevalece `Scope`.
2. “un campo optrev que vale None se puede volver a poner” y “un documento con optrev None acepta fields update del campo a 'x'”. No aclara si `None` es línea ausente, `null` explícito o valor tipado; obliga a inventar el estado inicial y qué significa “volver a poner”.
3. “fields update de un path con valor None” y “igual con una clave null dentro de un dict tipado”. No queda claro si el dict tipado entra pese a que `BaseModel` está fuera; obliga a decidir alcance.
4. “un modelo minimo (un campo rev Optional[str] y un campo optrev Optional[str])” no indica la API o forma de declararlo en SLDB; obliga a inventar el modelo de prueba.

DRY-RUN
Sin ejecutar: leería el TaskDoc, tests existentes y módulos de render/extract/fields update; crearía `tests/test_rev_optrev_none.py`; modificaría render/extract y fields update. Dependencias: `.venv` y `pytest`. Validación futura: `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rev_optrev_none.py`; criterio: pasan los dos tests. No es agregado: es tarea de código.

FUTURO
El ejecutor futuro producirá el test y el parche; el validador ejecutará `pytest`. Un humano debe confirmar el alcance frente al título y la semántica de `None` antes de implementar.
