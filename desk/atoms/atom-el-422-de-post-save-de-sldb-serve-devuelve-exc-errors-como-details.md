---
sldb:
  by: agent
  at: '2026-11-25T05:44:15Z'
  authority: generated
  via: create_document
id: atom-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details
title: El 422 de POST /save de sldb serve devuelve exc.errors() como details
five_wh_one_plus: how
tags:
- system:sldb
- topic:serve-422
---

# El 422 de POST /save de sldb serve devuelve exc.errors() como details

## Answer

Cuando pydantic rechaza un documento en POST /save, sldb serve responde 422 con details igual a la lista serializable de exc.errors() (loc, msg, type), conservando el body previo.
