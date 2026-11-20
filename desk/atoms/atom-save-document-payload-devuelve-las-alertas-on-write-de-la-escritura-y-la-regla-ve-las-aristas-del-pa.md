---
sldb:
  by: agent
  at: '2026-11-20T12:58:32Z'
  authority: generated
  via: create_document
id: atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa
title: save_document_payload devuelve las alertas on_write de la escritura y la regla
  ve las aristas del payload nuevo
five_wh_one_plus: how
tags:
- system:sldb
- topic:rules
---

# save_document_payload devuelve las alertas on_write de la escritura y la regla ve las aristas del payload nuevo

## Answer

save_document_payload devuelve en el DocumentReference un campo alerts con las alertas on_write de esa escritura (además de enviarlas por route), y una regla on_write cuya condición depende de una arista que declara el payload nuevo la ve al evaluarse, porque rule_graph se arma con el payload que se va a escribir. Código en 0f91540d.
