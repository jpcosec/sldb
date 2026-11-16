---
sldb:
  by: agent
  at: '2026-11-16T10:38:59Z'
  authority: generated
  via: create_document
id: atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
title: 'Cargar un store por la API pública no aborta por un documento inválido: on_invalid=''skip''
  devuelve los sanos y nombra los inválidos'
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: src/sldb/api/documents/runtime_documents.py
---

# Cargar un store por la API pública no aborta por un documento inválido: on_invalid='skip' devuelve los sanos y nombra los inválidos

## Answer

sldb.api.load_runtime_documents(store_path, on_invalid='skip') devuelve RuntimeDocuments(documents, invalid), donde cada InvalidDocument tiene path, model y error. Con el modo por defecto ('raise') sigue devolviendo una lista y, si un documento no valida, lanza SLDBValidationError con su ruta. EdgeIndex.problem_details es una lista de EdgeProblem(kind, document, detail) paralela a problems, que se mantiene como lista de textos para no romper consumidores.
