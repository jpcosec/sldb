## REFORMULACION
**Propósito:** evitar que documentos existentes queden inválidos al agregar al modelo un campo de frontmatter con default. **Resultado:** un documento sin la clave nueva toma el default al extraerse y sigue válido, con un test que lo demuestre. **Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`, inferido del cwd y de la ruta de validación. **Límites:** solo extracción de frontmatter con defaults y un test; quedan fuera `fields update` y migraciones sin default. Nodo ejecutable `task.code`, no agregado.

## AMBIGUEDADES
1. “agregar un campo con default a un modelo” / “modelo registrado”: no identifica modelo, campo ni API de registro; obliga a inventar dónde y cómo registrar.
2. “Extraccion que aplica el default ausente”: no nombra módulo, función ni mecanismo; obliga a inventar el punto de cambio.
3. “Un documento sin la clave nueva toma el default del modelo al extraer”: no aclara si el default se materializa en el documento o solo en la extracción; obliga a inventar la semántica.
4. “y fields update los puede reparar” (título) contradice “fields update ... falla” y “Fuera: fields update”; obliga a decidir si entra en alcance.
5. “sigue valido”: no define qué validación ni estado observable; obliga a inventar la aserción del test.
6. “Correr solo el test”: no aclara si prohíbe ejecutar la suite completa; obliga a inventar la política de ejecución.

## DRY-RUN
**Lecturas:** TaskDoc y nota referenciada; código de registro de `StructuredNLDoc`, extracción de frontmatter y tests existentes. **Cambios previstos:** crear `tests/test_campo_con_default.py` y ajustar la extracción para aplicar defaults ausentes. **Dependencias:** modelo registrado, API de extracción y pytest. **Validación futura:** ejecutar `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_campo_con_default.py`. Nada se ejecuta aquí.

## FUTURO
Un nodo ejecutor implementará el cambio y correrá el test; un humano resolverá el alcance de `fields update`, el modelo/campo concreto y el criterio de “válido”.
