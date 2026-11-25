## REFORMULACION
Encargo del nodo: corregir en el repo `sldb` la fricción de `rev`/`optrev` con valor `None` y la actualización por `fields update` de un path con valor `None`, con tests. Resultado esperado: `rev None` renderiza `null` o falla con error claro; `optrev None` puede reinsertarse mediante `fields update`; los dos tests de `None` pasan. Límites: solo render/extract de `rev`/`optrev`, `fields update` con `None` y tests; fuera de alcance tablas vacías, dict de `BaseModel` y rutas relativas de `docs create`. Validación declarada: ejecutar únicamente `tests/test_rev_optrev_none.py` con el comando indicado.

## AMBIGUEDADES
1. «rev None renderiza null o da un error claro»: no define cuál de los dos comportamientos es aceptable; obligaría a inventar la semántica esperada.
2. «un optrev None se puede volver a poner con fields update»: no especifica path, valor esperado ni forma de invocación; obligaría a inventar el contrato de `fields update`.
3. «con un modelo mínimo»: no identifica esquema, campos ni fixture; obligaría a inventar el modelo de prueba.
4. «Los dos tests de None pasan»: no nombra los dos casos ni su granularidad; obligaría a inventar la suite exacta.

## DRY-RUN
Lecturas: TaskDoc, rituales de ejecución/testing/closeout, Board, referencia de inbox y código/tests existentes de render, extract y `fields update`. Pills y átomos ligados: ninguno declarado (`pills: []`, `atoms: []`). Cambios previstos: crear o ajustar `tests/test_rev_optrev_none.py` con un modelo mínimo; corregir render de `rev None`, extracción/render de `optrev None` y `fields update` de paths con `None`. Dependencias: entorno virtual del proyecto, `pytest`, `TMPDIR=/mnt/ssd/tmp/sldb1`. Validación futura: ejecutar el pytest indicado; después, ritual de testing y closeout, incluyendo auditoría de git, árbol limpio y actualización del Board mediante `deskops`.

## FUTURO
Otro nodo o un humano debe decidir si `rev None` produce `null` o error, precisar el contrato de `fields update`, definir el modelo mínimo y confirmar los dos casos de prueba. También corresponde al cierre ejecutar la suite pertinente, actualizar CHANGELOG/Board y commitear.
