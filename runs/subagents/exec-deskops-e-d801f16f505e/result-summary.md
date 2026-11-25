# result-summary
Archivos (commit en deskops/deskops-e-d801f16f505e):
- surface/src/core/client.ts: nuevo `storeInfo()` -> GET /stores ({store, root}).
- surface/src/app/WorkbenchShell.tsx: si no llega prop storePath, la pide con client.storeInfo(); mientras carga o si falla, 'Documentos'.
- surface/src/app/workbench.test.tsx: test Lectura con storeInfo mockeado muestra el nombre del store.
Nota: main.tsx no se tocó; el shell resuelve el store solo, así el caller no necesita pasarlo (revisar si se prefiere en main).
Alias businessName ya borrado antes (9384682f); grep limpio. Validación en validation.log.
