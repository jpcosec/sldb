# T10 · `delete` deja el archivo en disco

Estado: **HECHO** · Worktree: `hum-ecosystem-worktrees/sldb-noise`
Commit: `975fbc1` — "save: delete borra el archivo, no solo lo destrackea"

## Qué
Bug encontrado probando la vista Destilación: `POST /save` con `action: delete` sacaba
el documento del grafo pero DEJABA el `.md` en disco; el próximo track o rescan lo
resucitaba.

## Causa
`apply_change` en `cli/serve/save_routes.py` llamaba `untrack_document` (que por
contrato conserva el archivo) en vez de `delete_document` (que ya existía y borra
archivo + purga la cache de extracción). El test afirmaba la conducta vieja.

## Resultado
Se usa `delete_document`. Suite: 1090 passed.

## OJO: falta integrar
El repo principal `/home/jp/proyectos/hum-ecosystem/tools/sldb` TODAVÍA tiene el bug
(`save_routes.py` sigue llamando `untrack_document`). El arreglo vive en la branch del
worktree y falta integrarlo.
