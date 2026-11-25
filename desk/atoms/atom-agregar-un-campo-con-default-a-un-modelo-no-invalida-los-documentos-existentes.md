---
sldb:
  by: agent
  at: '2026-11-25T06:06:46Z'
  authority: generated
  via: create_document
id: atom-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes
title: Agregar un campo con default a un modelo no invalida los documentos existentes
five_wh_one_plus: how
tags:
- system:sldb
- topic:campo-default
---

# Agregar un campo con default a un modelo no invalida los documentos existentes

## Answer

Al re-extraer un documento al que le falta una clave nueva con default, sldb aplica el default del modelo y el documento no cae en store/doc-invalid.
