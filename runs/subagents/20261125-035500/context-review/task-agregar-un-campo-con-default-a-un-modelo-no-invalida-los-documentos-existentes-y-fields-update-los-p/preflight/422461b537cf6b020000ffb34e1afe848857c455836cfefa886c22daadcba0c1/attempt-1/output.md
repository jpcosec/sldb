## REFORMULACION

**Propósito:** corregir la extracción de frontmatter para que un `StructuredNLDoc` registrado, al que se le añade un campo con default (`espera_segundos: int = 4` con su marcador `rev`), siga produciendo documentos válidos aunque el Markdown existente no contenga esa clave.

**Resultado:** un test nuevo que demuestre que un documento escrito antes del cambio, al re-extraerse, no cae en `store/doc-invalid` y su payload expone `espera_segundos == 4`; más el arreglo mínimo en la extracción para aplicar defaults de campos ausentes.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`. Test en `tests/test_campo_con_default.py`; ejecución con `TMPDIR=/mnt/ssd/tmp/sldb1` y el Python del venv del proyecto.

**Límites:** dentro, extracción con defaults y ese único test. Fuera, `fields update` (tarea hermana) y migraciones sin default.

## AMBIGUEDADES

1. «un StructuredNLDoc minimo registrado en un store temporal»: no se indica cómo se registra el modelo ni qué API crea el store temporal; obliga a inventar fixtures y nombres.
2. «se agrega al modelo el campo espera_segundos: int = 4 con su marcador rev»: no se explicita la sintaxis del marcador `rev` ni si el campo se añade redefiniendo la clase en el test; obliga a inventar el mecanismo.
3. «Arreglo en la extraccion»: no se nombra módulo ni función responsable de extraer frontmatter; obliga a localizarlo por conjetura.
4. «su payload trae espera_segundos == 4»: no se define cómo se obtiene el payload desde el store; obliga a asumir una API de consulta.

## DRY-RUN

**Lecturas:** TaskDoc, nota referenciada en inbox, definición de `StructuredNLDoc` y su extracción de frontmatter, tests existentes como patrón.
**Cambios previstos:** crear `tests/test_campo_con_default.py`; modificar la extracción para rellenar defaults de claves ausentes.
**Dependencias:** modelo registrable, store temporal, pytest y `TMPDIR`.
**Validaciones futuras:** ejecutar exactamente `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_campo_con_default.py`. Nada se ejecuta aquí.

## FUTURO

`fields update` queda para `task-fields-update-repara-un-documento-hoy-invalido-cuando-la-escritura-lo-deja-valido`. Un humano decide si el arreglo cubre solo defaults o también migraciones.
