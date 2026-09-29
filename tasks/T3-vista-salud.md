# T3 · Vista SALUD

Estado: pendiente · Dificultad: baja · Depende de: T1
Worktree: `/home/jp/AntonIA/repos/AgentsKBs_worktrees/knowledge-surface/sldb-surface`

## Qué
Vista de lectura sobre datos que ya existen: divergencias (`stores check`),
nodos aislados, ciclos, documentos que fallan el mapeo de template.

Propuesta §6.5.

## Nota
Corregido durante la implementación: el enunciado original decía que "los datos ya existen" y que hay endpoints de salud. Es falso. El cliente solo habla con `/graph`, `/schema`, `/document`, `/document/segments`, `/extract/segments` y `/save`. No existen endpoints de `stores check`, ciclos ni nodos aislados. La vista implementada (`#/salud`) deriva únicamente tres señales reales: fallo de mapeo de template, documentos no canónicos y modelos que no cargan en `/schema`.

## Brechas detectadas

- **Divergencias (`stores check`)**: no hay endpoint. No se pueden listar divergencias entre modelo y archivo en disco; se implementó solo lo derivable (`canonical:false`).
- **Ciclos**: no hay endpoint que exponga el grafo de dependencias entre documentos (composición `ref: document|field`). No derivable desde `/graph`, que no trae aristas.
- **Nodos aislados**: no hay endpoint ni campo de adyacencia; `/graph` no expone grado ni referencias entrantes/salientes. No derivable.
- **`/graph` no expone estado de salud por documento**: para saber si un documento falla el mapeo o es no canónico hay que sondear `/document/segments` documento por documento (N+1). Falta un endpoint de lote del tipo `/health` o `/documents/health`.
- **`/schema.errors`** informa `{model, error}` pero no la causa estructurada (template vs import vs dependencia); la vista solo muestra el mensaje crudo.
- **`/document/segments` 422** no distingue "template no mapea" de otros fallos de validación; la vista agrupa todo error de sondeo como fallo de mapeo, con el mensaje del backend como detalle.
