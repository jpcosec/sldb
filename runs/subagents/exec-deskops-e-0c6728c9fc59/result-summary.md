# Resultado
Cherry-pick de ef45950d (storeTitle, textos) + refactor: borrados businessName y el caso NegocioDoc.
- WorkbenchShell.tsx: wikiLectura = workbench+lectura para cualquier store; titulo = storeTitle(prop nueva opcional `storePath`, si no "Documentos"); document.title igual; documento inicial = route.doc o documents[0] (sin 'informe'); testid wiki-business-name -> wiki-titulo.
- workbench.test.tsx: borrado test Peluqueria Rayen; nuevo test de titulo de store en Lectura; como Lectura es la lente por defecto y ahora oculta la maquinaria, 4 tests de chrome arrancan en lens=fierros (beforeEach) y se ajustaron.
- Archivos: surface/src/app/WorkbenchShell.tsx surface/src/app/workbench.test.tsx surface/src/core/wiki-index.ts surface/src/core/wiki-index.test.ts surface/src/core/__fixtures__/rechazos-sldb.json surface/src/core/doc-ref.test.ts surface/src/core/imagenes.ts surface/src/core/rechazo.ts surface/src/core/rechazo.test.ts surface/src/styles/paper-tokens.css surface/src/workbench/WikiLectura.test.tsx
Revisar: surface no conoce hoy una ruta de store; añadi la prop opcional storePath, el host debe pasarla (si no, "Documentos").
Validacion: ver validation.log (rc 0). Commit en rama deskops/deskops-e-0c6728c9fc59.

Archivos commiteados: surface/src/app/WorkbenchShell.tsx surface/src/app/workbench.test.tsx surface/src/core/wiki-index.ts surface/src/core/wiki-index.test.ts surface/src/core/__fixtures__/rechazos-sldb.json surface/src/core/doc-ref.test.ts surface/src/core/imagenes.ts surface/src/core/rechazo.ts surface/src/core/rechazo.test.ts surface/src/styles/paper-tokens.css surface/src/workbench/WikiLectura.test.tsx
Hallazgo: `deskops advance task` bloqueado por rule-activation-task-refactor: falta recibo goldens aceptado e intacto (ReviewDoc ...-bundle-1 con anchor_state=changed).
