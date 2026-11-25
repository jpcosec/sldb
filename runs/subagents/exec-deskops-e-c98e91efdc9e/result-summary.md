# Result: BLOCKED, sin cambios

No se modificó ningún archivo. Bloqueo por contradicción de alcance:

- `surface/src/app/WorkbenchShell.tsx` (que NO se debe tocar) hace `import { businessName } from "../core/wiki-index"` (l.6, usado en l.176),
  usa `NegocioDoc` (l.177) y el texto "La wiki de tu negocio" (l.349).
- Quitar `businessName` de `core/wiki-index.ts` (requerido por el Goal) rompe `tsc` por ese import; además
  `app/workbench.test.tsx` (l.387-390, no listado en el Scope) prueba ese comportamiento del shell con `NegocioDoc`.
- Además el grep de Done When devuelve más residuos fuera del scope listado: `core/imagenes.ts`, `core/rechazo.ts` (+test y fixture
  `rechazos-sldb.json`), `core/doc-ref.test.ts`, `styles/paper-tokens.css`, `app/workbench.test.tsx`.
  "Done When" (grep vacío excepto WorkbenchShell.tsx) exige tocar todos ellos.

Hace falta decisión del supervisor: (a) permitir editar WorkbenchShell.tsx y workbench.test.tsx, o (b) mantener un `businessName` genérico fuera de alcance; y confirmar que rechazo.ts/CSS/fixtures entran en alcance.
No se ejecutó validación ni `deskops advance`.
