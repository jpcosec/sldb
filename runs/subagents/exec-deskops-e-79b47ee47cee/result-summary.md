run_id: exec-deskops-e-79b47ee47cee
session: n/a (executor inline)  session_sha256: n/a
Cambios (commit en rama deskops/deskops-e-79b47ee47cee):
- surface/src/core/wiki-index.ts: borrado el comentario y el alias businessName (sin sustituto).
main.tsx no se tocó: sldb serve (/health, /schema) no expone ruta ni nombre del store, así que Lectura sigue mostrando 'Documentos'. Nota enviada al inbox de sldb: desk/inbox/20261125-145224-suggestion-health-debe-traer-el-nombre-del-store.md.
Validación: ver validation.log (todo rc 0). No se agregó test: el alias era código muerto; el grep de Done When queda vacío.
Revisar: que la nota de inbox cubra el pedido.
