# T10 · `delete` deja el archivo en disco

Estado: **HECHO** (integrado a `main` 2026-09-30) · Worktree: `hum-ecosystem-worktrees/sldb-noise`
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

## Integrado
El fix estaba solo en la rama `feat/structural-noise-detection`. Traído a `feat/surface`
como `5f6dc95` (cherry-pick de `975fbc1`); suite completa: 1139 passed. Queda entrar a
`main` cuando la rama se mergee.
