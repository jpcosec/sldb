# T7 · Vista LECTOR — anclar sobre texto crudo

Estado: pendiente · Dificultad: alta · Es el tramo que falta del ciclo
Worktree: `/home/jp/AntonIA/repos/AgentsKBs_worktrees/knowledge-surface/sldb-surface`

## Qué
Superficie para declarar anchors sobre una selección de texto crudo.
Propuesta §6.1 y §16.

## Estado de las piezas
- Contrato `AnchorDoc` (`symbol`/`kind`/`ref`/`motive`): **existe**
- `anchor_targets.py` resuelve `ref` → nodo del grafo: **funciona**
- `POST /extract/segments` da los tramos: **lo trae el handoff**
- Anchors → regularidad → modelo: **no existe en ningún lado**

`core/ingest/` se retiró en `d0df139` (producto anterior, muerto e inimportable).

## Nota
Esta tarea y T9 son el mismo problema. Es lo único que requiere diseño nuevo,
no solo implementación.
