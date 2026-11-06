---
id: atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill
title: El contrato completo de un modelo se declara y edita por drafts con validacion
  y backfill
five_wh_one_plus: how
tags:
- system:sldb
- topic:models
- topic:drafts
provenance: docs/architecture/model-authoring.md
---

# El contrato completo de un modelo se declara y edita por drafts con validacion y backfill

## Answer

create_model acepta containment, references, compositions, semantics y authority y genera las asignaciones de clase; describe_model los devuelve junto con template y has_draft; edit_model_metadata inserta o reemplaza esas asignaciones en el .draft.py por AST y sincroniza las secciones render del template; validate_model_draft rechaza campos inexistentes en containment o references y composiciones sin source_field con SLDBModelEditError; promote_model_draft(backfill=True) reescribe los documentos afectados y actualiza indice semantico y de aristas. Expuesto en sldb models create | metadata | validate --backfill y en POST /models/create, /models/metadata-edit y /models/promote. Decidido en SV04 (SV-D5), integrado en 6b80df36 y 6ba8bb20.
