## REFORMULACION
**Propósito:** dejar asentados los fundamentos del grafo operable antes de alterar el comportamiento del store: frontera sldb/deskops, semántica y gramática del lenguaje de reglas, y costura `GraphBackend`.  
**Resultado:** `G_BOUNDARY`, `G_SEMANTICS` y `G_SEAM` satisfechos mediante GO01, GO02 y GO03, en serie.  
**Repo:** sldb.  
**Límites:** PK01 es `aggregate`: no se ejecuta ni se promueve; termina cuando terminan sus hijos. No cambia el comportamiento observable de comandos existentes sobre stores existentes. GO03 puede escribir bajo `src/sldb/store/graph/`; una clave nueva de `store.yaml` con validación propia cuenta como comportamiento nuevo, no como cambio.

## AMBIGUEDADES
ninguna.

## DRY-RUN
PK01 no tendría ejecutor propio. Un operador promovería los hijos, nunca el agregado, y seguiría el orden fijado:

1. **GO01 (decisión):** lee la pill rev 5, `decisiones.md` D1 y `dag.yaml`. Crea el atom, lo enlaza en la pill y hace dos commits en `main`; el segundo satisface `gates.G_BOUNDARY` con el hash del primero. Envía la nota a `deskops/desk/inbox` por `deskops message send --to deskops`. Salidas: atom, pill enlazada, gate actualizado y mensaje. No cambia código.
2. **GO02 (diseño):** entra con `G_BOUNDARY` satisfecho. Lee D6 y la salida de GO01. Escribe `docs/architecture/rules-language.md` y tests de spec `xfail`. Salidas: gramática, semántica, `__contract__`, firma `eval`, tabla de equivalencias y `G_SEMANTICS` listo para revisión.
3. **GO03 (código):** entra tras GO02 y con `G_BOUNDARY`. Usa la firma de `eval` fijada por GO02 y D5. Implementa `GraphBackend` sobre networkx, enruta `graph` y `api/graph` por `analyze`, agrega `graph_backend` a `store.yaml`, documenta y actualiza CHANGELOG. Salidas: goldens idénticos, tests existentes sin cambios, backend espía, `eval` parcial y `G_SEAM`.

**Validación conjunta futura:** revisión en frío aceptada de GO02 y GO03, con disposición en `reviews/rN.md`; pytest en el host indicado sin rojos ni saltados; goldens de los seis comandos `graph` idénticos; gates con evidencia; CHANGELOG y docs. PK01 cerraría solo con sus tres hijos cerrados.

## FUTURO
El operador del desk de sldb acepta o rechaza las revisiones en frío y actualiza los gates. El host de pytest lo indica el dueño. La promoción de cada hijo se hace con `deskops add task --from-drawer`. `G_CONSUMER` y el consumo por deskops pertenecen a otro plan.
