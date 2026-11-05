## REFORMULACION

PK01 es un **agregado de planificación** del plan `grafo-operable`, repo dueño **sldb**. No se ejecuta: termina cuando completan GO01, GO02 y GO03.

- **Propósito:** dejar escritas la frontera sldb/deskops, la semántica del lenguaje de reglas y la costura `GraphBackend` antes de cambiar el comportamiento del store.
- **Resultado:** gates `G_BOUNDARY`, `G_SEMANTICS` y `G_SEAM` satisfechos mediante sus hijos.
- **Límites:** no cambiar comportamiento observable; GO03 puede escribir bajo `src/sldb/store/graph/` precisamente porque la restricción es funcional, no de rutas.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

PK01 no admite ejecución directa. Un ejecutor futuro recorrería sus hijos en serie:

1. **GO01 — Registrar la decisión de frontera y su atom.** Entradas: pill ya editada y sin commitear. Salidas: commit en `main` de sldb con pill y atom, más nota a `deskops/desk/inbox` vía `deskops message send --to deskops`; deja `G_BOUNDARY` actualizado citando el commit. Transfiere a GO02 la frontera registrada y `G_BOUNDARY`.
2. **GO02 — Semántica, gramática y firma de evaluación.** Entradas: `G_BOUNDARY`. Salidas: `docs/architecture/rules-language.md`, tabla de equivalencias, semántica de `incomplete`, `__contract__`, firma `eval(...) → findings` y tests de spec `xfail`; produce `G_SEMANTICS`. Transfiere a GO03 gramática, semántica, forma de findings y condiciones de contrato.
3. **GO03 — Costura GraphBackend sobre networkx.** Entradas: `G_SEMANTICS` y `G_BOUNDARY`. Salidas: protocolo `load`/`eval`, implementación networkx, documentos, clave `graph_backend` en `store.yaml` y enrutamiento de los seis comandos `graph` sin cambiar salidas; produce `G_SEAM`.

**Validación conjunta futura:** commit visible en `git log`; documento de semántica con ejemplos `xfail`; goldens idénticos de comandos `graph`; tests de carga y evaluación; gates actualizados. Sin ejecutar ahora.

## FUTURO

Confirmaciones humanas de D5 y D6; revisiones en frío de GO02 y GO03. GO05 consumirá la firma y añadirá caminos; nodos posteriores consumirán los gates y contratos producidos.
