---
sldb:
  by: agent
  at: '2026-11-16T09:54:26Z'
  authority: generated
  via: create_document
id: atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
title: Las pruebas de notaciones, paletas, vista resuelta y ViewDoc que tenía spec2viz
  viven en sldb y solo importan sldb
five_wh_one_plus: what
tags:
- system:sldb
- topic:notations
provenance: tests/notations/test_ported_from_spec2viz_notation.py
---

# Las pruebas de notaciones, paletas, vista resuelta y ViewDoc que tenía spec2viz viven en sldb y solo importan sldb

## Answer

Los siete archivos tests/notations/test_ported_from_spec2viz_*.py portan los casos de spec2viz/tests (notation, notation_view, style_palette, catalog_notation, catalog_resolved_views, view_contract_resolved, view_doc) sobre sldb.notations, sldb.api.notations, sldb.api.ViewDoc y la CLI sldb notations. Cada docstring lista los casos no portados y el motivo (sobre todo renderers y catalog build, que son de specIR). Los specs del repo de spec2viz se copiaron como fixtures en tests/notations/fixtures/docs/architecture/.
