---
sldb:
  by: agent
  at: '2026-11-21T15:33:24Z'
  authority: generated
  via: create_document
id: atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb
title: incomplete se retira del lenguaje de predicados de sldb
five_wh_one_plus: how
tags:
- system:sldb
- topic:rules
---

# incomplete se retira del lenguaje de predicados de sldb

## Answer

El tercer valor incomplete era inalcanzable con datos reales y se retiró del lenguaje, la API y la doc: el lenguaje es bivaluado, rules check ya no emite rules/<n>/incomplete y rules explain sale con 0, 1 o 3. Commits 22cfafb2c29e62a391d23be53d690a21955fe0ee (retiro) y 1d31c3d8e3c7a6dba59e44f2ea9e77fcf8ae840b (intento 2: graph-backend.md, referencias regeneradas con selfdoc, test on_write restaurado), más la cabecera de rules-language.md en su tarea aparte. Agotó los dos intentos de tester; la verificación del coordinador está en runs/subagents/20261121-verif-predicados-incomplete/.
