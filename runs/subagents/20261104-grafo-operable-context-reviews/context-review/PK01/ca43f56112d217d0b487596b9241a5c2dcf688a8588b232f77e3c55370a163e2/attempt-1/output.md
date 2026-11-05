## REFORMULACION

PK01 es un agregado no ejecutable del plan `grafo-operable`, repo dueño `sldb`. Su propósito es dejar fijados, antes de cambiar el comportamiento del store: (1) la frontera sldb/deskops registrada y commiteada, (2) la semántica, gramática y firma de evaluación del lenguaje de reglas, y (3) la costura `GraphBackend` implementada sobre networkx. Resultado: `G_BOUNDARY`, `G_SEMANTICS` y `G_SEAM` satisfechos. Límite: no cambiar comportamiento observable; GO03 solo puede escribir bajo `src/sldb/store/graph/` y enrutar sin alterar salidas. Al ser agregado, no se promueve: termina cuando terminan GO01, GO02 y GO03.

## AMBIGUEDADES

1. **“sin cambiar ninguna salida”** / **“store.yaml sin clave carga networkx, con clave inválida falla con mensaje que lista ["networkx"]”**. El límite del padre dice que la restricción es no cambiar comportamiento observable; GO03 introduce un error nuevo al cargar el store con `graph_backend` inválida. Obliga a inventar si la validación de configuración cuenta como “salida” observable o si está permitida por ser explícita en GO03.
2. **“revisión en frío aceptada”** (aceptación de GO02 y G_SEMANTICS). No se nombra quién acepta ni el criterio además de los ejemplos. Obliga a inventar el actor y el estándar de aceptación; el gate dice “desk de sldb”, pero no identifica revisor ni procedimiento.

## DRY-RUN

GO01: lee pill editada sin commitear, `dag.yaml` y decisiones; crea atom, enlaza pill, commitea en main, edita `gates.G_BOUNDARY` con hash y envía nota a `deskops/desk/inbox`. Salida: commit, atom, nota, G_BOUNDARY satisfied. Depende de git y del canal entre desks; no toca código.

GO02: consume G_BOUNDARY; lee `where_parse`, `FieldCondition`, brief y decisiones; escribe `docs/architecture/rules-language.md` y tests xfail. Salida: gramática, semántica trivaluada, `__contract__`, firma `eval` y forma de findings. Transfiere a GO03 esa firma y semántica. G_SEMANTICS queda para revisión en frío.

GO03: consume GO02 y G_BOUNDARY; lee compose, `api/graph` y CLI graph; escribe protocolo e implementación networkx, enruta seis comandos y `api/graph`, añade `graph_backend`, doc y CHANGELOG. Salida: G_SEAM. Validaciones futuras: goldens idénticos, tests existentes, backend espía, carga del índice del repo, `eval(has(id))`, fallback/error de configuración.

Validación conjunta: los tres gates satisfied, tests verdes sin saltos, goldens sin cambios y revisión en frío de GO02/GO03.

## FUTURO

La revisión en frío de GO02 y GO03 y la aceptación de sus gates; la ejecución de los hijos tras `execution_authorized`; y el consumo posterior por deskops (`G_CONSUMER`), fuera de este nodo.
