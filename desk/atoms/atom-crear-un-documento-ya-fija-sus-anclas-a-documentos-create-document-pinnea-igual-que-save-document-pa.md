---
sldb:
  by: agent
  at: '2026-11-16T11:09:58Z'
  authority: generated
  via: create_document
id: atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa
title: 'Crear un documento ya fija sus anclas a documentos: create_document pinnea
  igual que save_document_payload'
five_wh_one_plus: what
tags:
- system:sldb
- topic:anchors
provenance: src/sldb/api/documents/create_document.py
---

# Crear un documento ya fija sus anclas a documentos: create_document pinnea igual que save_document_payload

## Answer

create_document (y Transaction.create, que pasa por él) llama pin_payload sobre el payload antes de renderizar y validar, y pin_provenance sobre el texto antes de escribirlo, en el mismo orden que save_document_payload. Un campo de __doc_anchors__ que nombra un destino trackeado sin @sha256 queda escrito con el hash de contrato del destino (anchor_state intact) sin necesidad de un save posterior. Un destino no trackeado queda como estaba (lost).
