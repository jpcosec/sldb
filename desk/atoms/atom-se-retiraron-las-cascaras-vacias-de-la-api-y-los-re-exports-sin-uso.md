---
sldb:
  by: agent
  at: '2026-11-21T13:21:08Z'
  authority: generated
  via: create_document
id: atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso
title: Se retiraron las cáscaras vacías de la API y los re-exports sin uso
five_wh_one_plus: how
tags:
- system:sldb
- topic:api
---

# Se retiraron las cáscaras vacías de la API y los re-exports sin uso

## Answer

5f5eed9d borra las cáscaras vacías de la API y los re-exports sin uso (api.schema field_descriptor/field_kinds) y los residuos de kgdb. El tester dio FALLA solo por la puerta 'identidad' por workbench_demo (excepción f055723d). El coordinador verificó en worktree limpio tests/api, tests/segments y los de segmentos y código limpio: padre y commit dan las mismas 16 fallas, que son de la regresión de 6772820a con tarea aparte, y 2 passed menos por los tests de los re-exports retirados.
