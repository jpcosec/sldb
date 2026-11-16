---
sldb:
  by: agent
  at: '2026-11-16T11:18:07Z'
  authority: generated
  via: create_document
id: atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s
title: sldb.api.template_anchors dice, por campo de un modelo, el párrafo literal
  de la plantilla que ancla su extracción
five_wh_one_plus: what
tags:
- system:sldb
- topic:templates
provenance: src/sldb/api/model_registry/template_anchors.py
---

# sldb.api.template_anchors dice, por campo de un modelo, el párrafo literal de la plantilla que ancla su extracción

## Answer

sldb.api.template_anchors(model_type) -> dict[str, str] devuelve, para cada campo cuyo marcador en __template__ va inmediatamente después de un párrafo literal que el extractor usa como ancla, el texto de ese párrafo tal como está en la plantilla, cursivas incluidas. Usa las mismas recetas que Validator.extract y no reparsea la plantilla. Los campos sin párrafo ancla no aparecen. Sirve para que un consumidor (deskops) no guarde como valor el párrafo placeholder de la plantilla.
