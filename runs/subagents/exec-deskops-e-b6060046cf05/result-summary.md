# Resultado
Archivos (rama deskops/deskops-e-b6060046cf05): surface/src/core/{wiki-index.ts,wiki-index.test.ts,doc-ref.test.ts,rechazo.ts,rechazo.test.ts,imagenes.ts,__fixtures__/rechazos-sldb.json}, styles/paper-tokens.css, workbench/WikiLectura.test.tsx.
- wiki-index: nuevo storeTitle(storePath) (ultimo segmento o "Documentos"); NegocioDoc/businessName fuera.
- Alias de una linea: businessName = (_documents) => null, con el comentario pedido (no puede ser "= storeTitle": el shell lo llama con documents y tsc fallaria).
- NegocioDoc -> DocumentoDoc, textos negocio -> documento en tests/fixtures/rechazo.
## BLOQUEO para el supervisor
src/app/workbench.test.tsx:396 (no tocable) espera que el shell muestre el nombre del negocio desde NegocioDoc; sin esa logica en wiki-index falla (1 test). Es consecuencia inevitable del alcance: requiere que JP migre el shell/test. tsc, check-layers y el resto de vitest pasan. No ejecute deskops advance.
