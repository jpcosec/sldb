# Plan: lo que specIR y las interfaces le piden a sldb

Reescrito el 2026-11-25. Las decisiones y su porqué están en `docs/architecture/`:

- `mechanism-in-sldb-content-in-specir.md`: sldb conserva el mecanismo de notaciones; el contenido
  pasa a specIR.
- `pron-is-archived.md`: pron se archiva y tres capacidades suyas pasan a sldb.
- `one-command-taxonomy-served-by-fastmcp.md`: una taxonomía de comandos servida por fastmcp.
- `surface-is-an-editor-contract.md`: las interfaces (plan aparte, en
  `desk/drawer/plans/superficie-como-contrato-de-editores/`).

Aquí va solo el trabajo de sldb que sale de eso. Estados y dependencias en `dag.yaml`.

## Pedidos que siguen

| Pedido | Para qué | Estado al 2026-11-25 |
|---|---|---|
| Cobertura de átomos por spec y vista | El `n/m` de átomos de un diagrama | tarea creada |
| Líneas del fragmento y estado de un `CodeAnchorDoc` | Ver un ancla de código en una interfaz | tarea creada |
| Facts de handler JSX con los atributos estáticos del elemento | El localizador de un control | tarea creada |
| Llamadas propias de cada handler en línea | Seguir un handler hasta su operación de API | tarea creada |
| `method` del segundo argumento de una llamada | Resolver envoltorios como `request('/x', {method:'POST'})` | tarea creada |
| Una notación declara qué estándar implementa | Revisar UML, IFML y ORCA como estándares | sin tarea |
| Un documento sin glifo se informa como hueco | Medir la cobertura de una notación; hoy falla todo el `resolve_view` (`node_view.py:17`) | sin tarea |
| Predicado de reglas sobre los tags semánticos del modelo y sus ancestros | Reglas por concepto, no por nombre de modelo | sin tarea |

## Pedidos que quedaron sin efecto

| Pedido | Por qué |
|---|---|
| `sldb serve --extension` | Una extensión pasa a ser un servidor montado en el de sldb. La tarea existe y está frenada |
| Notación BPMN en sldb | El contenido de las notaciones es de specIR |
| Exportar en `sldb.api` las clases de spec y los helpers de notación | Las clases se mudan a specIR |
| Facts de `component` y `handlers` en plantillas `htm` | graph_ui deja `htm` al pasar a React 19 con build |

## Trabajo nuevo

| Trabajo | Depende de |
|---|---|
| Taxonomía de comandos: una tabla que junta `sldb.api`, la CLI, `sldb serve` y `sldb mcp` | nada; la aprueba JP |
| Servidor fastmcp que declara cada operación una vez | la taxonomía |
| Retirar `sldb serve` | que las dos interfaces sean clientes del servidor nuevo |
| Rechazar una relación inválida antes de escribirla, y prevalidar un movimiento entero | nada |
| Registro persistente de movimientos y deshacer entre sesiones | nada |
| Sacar las notaciones builtin y las clases de spec, y dejar una notación mínima para las pruebas | que specIR las haya recibido |

## Lo que sldb ya tiene y pron duplicaba

Máquinas de estado y transiciones, lotes atómicos con prevalidación y `dry_run`, y edición de
modelos por borrador. No hay que traerlo.
