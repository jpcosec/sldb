## REFORMULACION
Propósito: eliminar fricciones de `None` en `rev`/`optrev` y en `fields update` de SLDB. Resultado: `rev` con `None` renderiza `null` o produce un error claro; un `optrev` con `None` puede volver a establecerse mediante `fields update`; ambos casos cubiertos por tests. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: solo render/extract de `rev`/`optrev` y `fields update` de un path con valor `None`, con tests; quedan fuera tablas, `BaseModel` y `docs create`. Es una tarea `task.code` ejecutable, no un agregado con hijos.

## AMBIGUEDADES
1. «rev None renderiza null o da un error claro»: no se elige entre `null` y error; obligaría a inventar el contrato y la salida esperada.
2. «un optrev None se puede volver a poner con fields update»: no define representación de `optrev=None`, comando, ruta ni valor esperado; obligaría a inventar la API y el test.
3. «con tests» y «un modelo minimo»: no concreta fixture, modelo ni si `extract` también requiere test; obligaría a inventar la estructura de pruebas.
4. El título y el Rationale mencionan tablas vacías, `BaseModel` y rutas de `docs create`, pero el Scope dice «Fuera: tablas, BaseModel, docs create»; obligaría a decidir si se ignoran o si quedan como residuo.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, nota referenciada, código de render/extract/`fields update` y tests existentes. Cambios previstos: crear `tests/test_rev_optrev_none.py` con un modelo mínimo; ajustar render/extract para `rev=None`; ajustar `optrev=None` y `fields update`. Dependencias: `/mnt/ssd/proyectos/SLDB_1/.venv/bin/python`, pytest y `TMPDIR=/mnt/ssd/tmp/sldb1`. Validación futura: ejecutar exactamente `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rev_optrev_none.py` y comprobar que pasan los dos tests. Sin ejecutar nada.

## FUTURO
Un humano debe decidir si `rev=None` renderiza `null` o falla, y fijar el contrato de `fields update` para `optrev=None`. Después, otro nodo o el ejecutor implementa y valida; la aceptación, revisión y eventual integración quedan fuera de este preflight.
