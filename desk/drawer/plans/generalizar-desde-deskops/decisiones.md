# Decisiones registradas

Cada entrada dice quién decidió, con qué fuente y en qué fecha. Las decisiones D1–D8 de `grafo-operable/decisiones.md` siguen vigentes y no se copian salvo las que este plan consume. Las GP son propuestas de este plan: quedan como "propuesta" hasta que el dueño autorice el plan.

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| G1 | Lo general va a sldb y lo específico del caso deskops va a deskops; deskops es configuración sobre sldb. | Dueño | Aprobación del árbol de tareas `~/proyectos/SLDB_1/deskops-como-config-arbol.md` (brief `planes-config-brief.md`) | 2026-11-05 |
| G2 | Invariante de la migración: el formato del desk y la gramática del CLI de deskops no cambian; cada superficie se cambia y su código viejo se borra en el mismo paso. Para este plan significa que cada capacidad entra completa y probada en sldb antes de que deskops la consuma. | Dueño | Árbol aprobado, §Contexto | 2026-11-05 |
| G3 | P2 corre en paralelo a P1 (grafo-operable), en un worktree de sldb aparte; GD21 primero porque destraba el Board. | Dueño | Árbol aprobado, §Orden y paralelismo | 2026-11-05 |
| D3 | No hay coordinación central entre desks: cada desk tiene sus tareas y pide feedback al resto. | Dueño | `grafo-operable/decisiones.md` D3 | 2026-11-04 |
| D5 | networkx tras la costura `GraphBackend`; otro motor entra detrás de la misma costura. | Dueño | `grafo-operable/decisiones.md` D5 | 2026-11-04 |
| GP1 | La configuración de grafo de proyecto es dato puro (serializable a YAML) y se declara en `store.yaml` bajo `project_graph:`; el único hook que hoy es callable (`closed_document`) pasa a ser un predicado del lenguaje de sldb. | Propuesta de este plan | Rama `wt/closeout-graph-sldb`; G1 | 2026-11-05 |
| GP2 | La transacción escribe en el momento (lectura de lo propio dentro de la transacción) y revierte todo ante excepción; `apply_batch` es una transacción con prevalidación. No se introduce un modo diferido. | Propuesta de este plan | Semántica actual de `doc_io.DocTransaction` que deskops usa | 2026-11-05 |
| GP3 | La guarda optimista de un cambio es `expected_source_hash` (el `source_hash` de la entrada); la igualdad de payload completo de `/save` (`expected`) se conserva como alternativa por compatibilidad. | Propuesta de este plan | `save_plan.py:51`; `payload_save_steps.py:76-77` | 2026-11-05 |
| GP4 | Una vista es un documento `ViewDoc` del store (como `RuleDoc`), no una clave de `store.yaml`: se versiona, se consulta y se revisa como cualquier documento. | Propuesta de este plan | Paralelo con `RuleDoc` (GO06) | 2026-11-05 |
| GP5 | Las semillas del scaffold viven en `store.yaml` (`folders:`, `seeds:`), con dos modos: `if_missing` (nunca sobrescribe) y `managed` (reescribe si difiere y lo reporta). | Propuesta de este plan | `workspace.py:251 _write_if_missing`; GC04 de gates-por-tipo pedía reescritura gestionada de RelationDocs | 2026-11-05 |

## Pendientes del dueño

- **Hechos de git en las vistas.** Una tarjeta del Board muestra el estado del closeout (commit en HEAD, test existe), que sldb no calcula. GD25 deja un punto de extensión (`computed` por proveedor registrado en Python por el consumidor) en lugar de meter git en sldb; confirmar o pedir que esos hechos entren como recibos (`ReviewDoc`) y la vista solo los lea.
- **Atomicidad de `/save`.** GD24 hace que `/save` revierta todo ante falla (hoy deja `completed`). Es un cambio de contrato visible para clientes HTTP; confirmar.
