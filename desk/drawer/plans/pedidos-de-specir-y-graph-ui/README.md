# Plan: lo que specIR y graph_ui le piden a sldb

Escrito el 2026-11-25. Junta en un lugar todo lo que salió ese día como pedido a sldb desde el
trabajo de specIR (repo `IR`) y de graph_ui, con su estado, más lo que se averiguó sobre pron.
Tareas y dependencias en `dag.yaml`.

## Contexto, en tres frases

JP fijó que el render principal de un diagrama es la vista de notación de graph_ui y que specIR
declara (tipos, notaciones, vistas) en vez de dibujar. Eso deja a sldb como la pieza que resuelve:
notaciones, vistas, reglas, anclas y facts de código. Lo que sigue son los huecos que esa división
destapó.

## Pedidos

| # | Pedido | Para qué | Estado al 2026-11-25 |
|---|---|---|---|
| 1 | `sldb serve --extension MODULE:FUNCTION`, como `sldb mcp` | Que specIR sirva por HTTP impacto, reglas y controles | tarea creada |
| 2 | Cobertura de átomos por spec y vista en el payload de `sldb serve` | El `n/m` que mostraba el catálogo de spec2viz | tarea creada |
| 3 | De un `CodeAnchorDoc`, las líneas de su fragmento y su estado | Ver un ancla de código en una interfaz | tarea creada |
| 4 | Facts de handler JSX con los atributos estáticos del elemento | El localizador de un control (rol, nombre, `data-testid`) | tarea creada |
| 5 | Llamadas propias de cada handler en línea | Seguir un handler hasta su operación de API | tarea creada |
| 6 | `method` del segundo argumento de una llamada | Resolver envoltorios como `request('/x', {method:'POST'})` | tarea creada |
| 7 | Facts de `component` y `handlers` en plantillas `htm` | Que el extractor vea graph_ui, que es React con htm | **sin pedir** |
| 8 | Notación BPMN (carriles, eventos, compuertas) | BPMN en el render principal | **sin pedir** |
| 9 | Que una notación declare qué estándar implementa | Revisar UML, IFML y ORCA como estándares | **sin pedir** |
| 10 | Un documento sin glifo se informa como hueco, no hace fallar la vista | Medir cobertura de una notación | **sin pedir** |
| 11 | Predicado de reglas sobre los tags semánticos del modelo | Reglas por concepto, no por nombre de modelo | **sin pedir** |
| 12 | Exportar en `sldb.api` las clases de spec y los helpers de notación | Que specIR deje de importar módulos internos | pedido dos veces (notas del 15-11, cerradas), sigue sin exportarse |

Notas sobre algunos:

- **7.** El extractor de specIR lee facts de sldb, no código. Sobre el `htm` de graph_ui
  (`frontends/mindmap`) hoy salen 0 componentes y 0 handlers; sobre TSX salen bien. Se había
  descartado cuando la UI de specIR iba a ser TSX; revive porque el render principal es graph_ui.
- **9, 10, 11.** Hoy nada en una `NotationDoc` dice qué estándar implementa; un documento que ningún
  glifo casa hace fallar todo el `resolve_view` (`ViewError` en `node_view.py:17`); y el lenguaje
  de reglas no puede leer los tags que salen de `__semantics__` ni sus ancestros en el DAG.
- **12.** specIR importa `sldb.models.notation.diagram_specs.*` y `sldb.notations` en dos módulos
  exentos de su propia regla de "solo API pública" (`IR/src/specir/visual/spec_models.py`,
  `notation_style.py`).

## pron: qué es hoy y qué costaría retirarlo

JP daba pron por retirado. **No hay ninguna decisión que lo retire.** Lo que existe:

- **ADR aceptado el 2026-09-20** (`docs/architecture/sldb-absorbs-kgdb.md:81-106`): pron pasa a ser
  una "semantic shell". Suelta su fachada de store, su lector de grafo y su corpus, y conserva
  decir y evaluar formas, y los movimientos con su registro y su deshacer. El mismo ADR dice que
  "graph_ui is a graphical UI over SLDB, not a surface over pron". Es un achique, no un retiro.
- **Decisión de JP del 2026-11-11**, solo para specIR: no depende de pron porque "pron está
  desactualizado y no funciona bien como base".
- **`G_SLDB_PRON_MCP`** (gate del plan de specIR, 2026-11-12): que sldb integre y exponga las
  capacidades de pron por su API y su MCP. Pendiente, y **no existe ninguna tarea de sldb** que lo
  tome.

Estado de pron:

- Activo en el registro (`desk/registry/repo-pron.md`), con commits del 2026-11-17.
- **Su suite está en rojo contra el sldb actual**, con una tarea bloqueada desde el 2026-11-16
  (deshacer no restaura el hash del mundo; se pierde un documento tras untrack y track).

Quién lo usa:

| Consumidor | Qué usa | Reemplazo en sldb |
|---|---|---|
| graph_ui, modo local (el default) | `pron.world.store.Store` como puerta al store: leer, crear, reemplazar, quitar, registrar modelos | existe todo en `sldb.api` |
| graph_ui, editor de clases | borradores de modelo: detalle, plantilla, campos, validar, promover | existe todo en `sldb.api`; `sldb serve` ya usa las mismas funciones |
| graph_ui, modo remoto | nada: lee y escribe por `sldb serve` | ya está |
| legos (fuera del workspace) | `World`, `Session`, sesiones remotas, creación de modelos por MCP | parcial: las sesiones de solo lectura por proyección no tienen equivalente |
| kinesis (sin verificar) | lo dice el README de Kimun | sin revisar |
| sldb, deskops, IR, Kimun | nada | |

Lo que hoy **solo tiene pron**, sin reemplazo en sldb:

- Rechazar una arista **antes** de escribirla por sus tipos, cardinalidad y condición. sldb lo
  detecta después, en `check_edges`; su propio MCP lo lista como faltante.
- Prevalidar un movimiento entero, con condiciones y transiciones.
- Un registro persistente de cada movimiento y deshacer entre sesiones. El deshacer del MCP de
  sldb es por sesión y en memoria.
- Qué puede nombrar una sesión (proyección), con modo por relación.
- Las formas, el léxico, el diálogo, la superficie de lenguaje y el planificador `goal`.
- Simular el efecto de editar una regla sobre las aristas existentes.

Lo que sldb ya tiene y pron duplicaba: máquinas de estado y transiciones, lotes atómicos con
prevalidación y `dry_run`, edición de modelos por borrador.

**Sacar pron de graph_ui es barato** (reescribir un adaptador sobre `sldb.api`, o volver default
el modo remoto). **Retirar pron entero no lo es**: hay que decidir qué pasa con lo que solo él
tiene, y eso toca la edición por gestos de graph_ui.

## Decisiones abiertas para JP

- **Qué se hace con pron**: retirarlo entero; dejarlo como capa de lenguaje y sacar su uso como
  puerta al store; o dejarlo como está.
- **Si la edición de graph_ui escribe por sldb**, cuáles de las cosas que solo tiene pron pasan a
  sldb. La primera candidata es rechazar una arista inválida antes de escribirla.
- **Si se toma `G_SLDB_PRON_MCP`** como tarea de sldb, y con qué alcance.
