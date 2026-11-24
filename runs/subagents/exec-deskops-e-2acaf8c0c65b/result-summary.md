# result-summary — lector de minegocio en surface
run_id: exec-deskops-e-2acaf8c0c65b
session: (no disponible en esta corrida)   session_sha256: (n/a)

## Portado a surface/ (worktree deskops/deskops-e-2acaf8c0c65b)
Nuevos: src/core/{doc-ref,wiki-index,rechazo,imagenes}.ts y sus .test.ts; src/core/__fixtures__/rechazos-sldb.json;
src/workbench/{WikiIndex,Ficha,NuevaPagina,AvisoGuardado}.tsx; src/workbench/WikiLectura.test.tsx.
Modificados: src/core/{client,layout}.ts, src/main.tsx, src/react/{context.tsx,DocumentSurface.tsx,useDocumentEditor.ts},
src/styles/paper-tokens.css, src/views/ComposerView.tsx, src/workbench/{ProsaWorkbenchView.tsx,ProsaWorkbenchView.test.tsx},
src/app/workbench.test.tsx.

## SEÑALADO PARA EL COORDINADOR: WorkbenchShell.tsx
Se modificó src/app/WorkbenchShell.tsx (copia de la versión de minegocio). Sin él, 2 tests de workbench.test fallan y el lector no
queda cableado (docRef/findDocument, onDocumentsMutated, barra de lectura, subirImagen). El checkout principal no tenía cambios
locales en surface/ al empezar, pero avisar a JP antes de integrar si tiene trabajo propio en ese archivo.
vite.config.ts y tsconfig: SIN cambios. Se dejó fuera `base: SUPERFICIE_BASE` de vite.config.ts (solo sirve al panel de minegocio).
Fuera también: ORIGEN.md, README de minegocio, HANDOFF, assistant/.

## Especifico residual (conservado, inerte fuera de minegocio)
wiki-index.businessName y WorkbenchShell buscan un modelo `NegocioDoc` (null si no existe: en deskops no activa nada);
rechazo.ts reconoce mensajes "Este negocio ya tiene su página"; comentarios y CSS mencionan "negocio". main.tsx: la subida de imágenes
solo se activa con VITE_IMAGENES_URL (se retiró la mención a /panel/wiki/imagenes).
Agrupado: por carpeta (primer segmento del path) con semántica conectada pero sin la unificación de tags de deskops (no verificada).

## Tiempos contra el store real (sldb serve --store deskops/.sldb, 2085 documentos, localhost)
- /graph (base del índice): 3.5 s (4.5 MB), idéntico en 2 corridas; en el store sldb con links: 23.8 s en frío.
- buildWikiIndex sobre ese /graph (cliente): 83 ms.
- Lectura (/document?id=): 72 ms; ficha/segmentos (/document/segments?id=): 8.5 ms (atom-001, 8.9 KB / 3.9 KB).
- /schema 5 ms, /models 16 ms.
Medido por HTTP/cómputo; no se midió render en navegador. El cuello de botella es /graph (3.5 s).
(Un id de tarea recién creada dio 404: el servidor tenía el store cargado antes.)

## Validación
tsc, vitest (471) y check-layers pasan. tools/check.sh --fast: rc 1 por `identidad: workbench_demo sin clasificar` PREEXISTENTE
(falla igual en el checkout principal); no corregido por estar fuera del alcance. El coordinador debe decidir.
