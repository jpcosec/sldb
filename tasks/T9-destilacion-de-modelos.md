# T9 · Destilación: anchors → regularidad → modelo

Estado: no existe · Dificultad: alta · El tramo abierto del ciclo
Worktree: `/home/jp/proyectos/hum-ecosystem/tools/sldb`

## Qué
Detectar anchors que se repiten con el mismo `kind`, proponerlos como campos,
y declarar un `__template__` cuando la posición es estable. Los anchors de
`kind: relation` son candidatos a `__references__` / `__containment__`.

Propuesta §16.1: el modelo no se escribe, se destila. El `motive` de cada anchor
hace auditable la destilación.

## Estado
Nada implementado. Ni en SLDB ni en el `core/ingest` retirado.
