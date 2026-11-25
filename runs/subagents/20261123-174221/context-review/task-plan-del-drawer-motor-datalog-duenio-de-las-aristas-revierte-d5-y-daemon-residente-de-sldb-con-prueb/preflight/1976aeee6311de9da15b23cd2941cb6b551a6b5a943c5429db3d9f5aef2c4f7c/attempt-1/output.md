## REFORMULACION

Nodo no ejecutable: `task.docs` de planificación; no es agregado ni declara hijos/atoms en el input. Propósito: producir un plan para que un motor Datalog sea dueño del almacenamiento y consulta de aristas —revirtiendo D5— y para un daemon residente de sldb, con PoC medida y decisiones abiertas para JP. Resultado: `desk/drawer/plans/grafo-datalog-daemon/` con alcance, brief, decisiones y `dag.yaml`; informe de tiempos/memoria; D5 revertida fechada; una `task.decision` por decisión. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: no cambiar `GraphBackend` ni producción; PoC fuera de producción; no reemplaza ni bloquea `task-matching…`, que va primero.

## AMBIGUEDADES

1. “Datalevin u otro con cliente Python”: no fija candidatos ni criterio de elección; obligaría a inventar el conjunto evaluado y el método.
2. “mide aristas de un nodo, recorrido, emparejamiento de atomos y stale contra el camino actual”: no define consultas, datos, repeticiones ni umbral; obligaría a inventar la carga y el criterio de comparación.
3. “consumo de memoria en robocop2 con el tope de 8 GB libres”: no fija límite aceptable ni método de medición; obligaría a inventar el presupuesto.
4. “cada decision de diseno abierta queda como una task.decision”: no enumera cuáles están abiertas ni su granularidad; obligaría a inventar el listado.
5. “dag.yaml valido (deskops review node puede leerlo)”: no da esquema ni campos mínimos; obligaría a inferir el contrato.

## DRY-RUN

Lecturas: `docs/architecture/graph-backend.md`; `desk/drawer/plans/grafo-operable/` y `decisiones.md`; `protocol.py`, compose y edge_index; notas de inbox; deskops. Cambios previstos: crear el directorio del plan y sus cuatro documentos; añadir scripts/informe de PoC en `reports/` o el plan; editar `decisiones.md` para D5; crear `task.decision`. Dependencias: índice federado real y `.sldb_cache/edges`; motor elegido con cliente Python; datos de memoria de robocop2; deskops; orden previo de task-matching. Validaciones futuras: repetir la PoC con el comando publicado; `deskops graph missing --root .`; `deskops review node` sobre `dag.yaml`; comprobar D5 y opciones/recomendación en cada `task.decision`. Sin ejecutar.

## FUTURO

JP decide motor, forma del daemon e invalidación desde las `task.decision`. Otro nodo implementa los cambios de `GraphBackend`/producción y el daemon. El nodo de review valida `dag.yaml` y el cierre documental; task-matching debe completarse antes.
