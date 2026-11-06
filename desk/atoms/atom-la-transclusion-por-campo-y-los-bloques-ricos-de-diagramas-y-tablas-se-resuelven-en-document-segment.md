---
id: atom-la-transclusion-por-campo-y-los-bloques-ricos-de-diagramas-y-tablas-se-resuelven-en-document-segment
title: La transclusion por campo y los bloques ricos de diagramas y tablas se resuelven
  en /document/segments con un resolver inyectado
five_wh_one_plus: how
tags:
- system:sldb
- topic:segments
- topic:transclusion
provenance: docs/architecture/segments-and-transclusion.md
---

# La transclusion por campo y los bloques ricos de diagramas y tablas se resuelven en /document/segments con un resolver inyectado

## Answer

Una composicion con ref: field (Model:name#campo) se resuelve en build_document_segments mediante un FieldRefResolver que se inyecta cuando hay contexto de store; cada CompositionPiece lleva su SourceRef con model, doc, path y field, y sin resolver la composicion rinde vacia sin fallar, de modo que el render basico sigue puro. Un campo con trait diagram o view adjunta en su FieldSegment la proyeccion ya resuelta (resolve_view / evaluate_projection_view) y uno con trait table adjunta columns y rows, listos para dibujar en la UI unificada. Decidido en SV03 (SV-D4), integrado en ea85af56.
