---
sldb:
  by: agent
  at: '2026-11-19T07:56:58Z'
  authority: generated
  via: create_document
id: atom-una-escritura-por-campos-falla-antes-de-borrar-ruido-estructural-o-frontmatter-no-declarado-del-arch
title: Una escritura por campos falla antes de borrar ruido estructural o frontmatter
  no declarado del archivo
five_wh_one_plus: how
tags:
- system:sldb
- topic:api
---

# Una escritura por campos falla antes de borrar ruido estructural o frontmatter no declarado del archivo

## Answer

save_document_payload, y el update de apply_batch que pasa por él, re-renderiza el documento desde el payload. Antes de hacerlo aplica al texto actual del archivo las mismas guardas que al crear o trackear (refuse_structural_noise y refuse_undeclared_frontmatter, vía src/sldb/api/documents/lossy_overwrite.py). Si el archivo tiene encabezados o frontmatter que el modelo no declara, la escritura falla con el error de esas guardas, que nombra lo que se perdería, y el archivo queda intacto. Un documento trackeado con force que arrastra ruido no se puede escribir por campos hasta limpiarlo.
