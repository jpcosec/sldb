## REFORMULACION
Encargo: refactorizar `surface/src` para quitar residuos de “minegocio” del lector genérico. Resultado: `wiki-index` obtiene el título del último segmento de la ruta del store o usa `'Documentos'`; se renombran tipos, mensajes y fixtures; se conserva un alias deprecado de una línea para `WorkbenchShell.tsx`. Repo/ámbito: `surface/src`, excepto `WorkbenchShell.tsx`, `app/workbench.test.tsx`, `vite.config.ts` y `tsconfig`. Límite: no tocar el trabajo local de JP en `WorkbenchShell`. Validación: `tsc`, `vitest` sobre `src/core src/react src/views src/app` y `check-layers`.

## AMBIGUEDADES
1. “surface/src no nombra NegocioDoc, businessName” contradice “wiki-index exporta ademas... `export const businessName = storeTitle`” y el `Done When` que admite “las lineas de alias deprecado”. Obliga a decidir si el objetivo es ausencia total o ausencia salvo alias.
2. “el ultimo segmento de la ruta del store que surface ya conoce” no especifica cómo `wiki-index` accede a esa ruta ni qué hacer con barras finales, raíz o rutas vacías. Obliga a inventar API, normalización y firma.
3. “Mensajes con 'negocio' pasan a 'documento' o 'pagina'” no fija qué término corresponde a cada mensaje. Obliga a inventar el mapeo textual.
4. “los textos de styles/paper-tokens.css” no identifica qué textos ni si son contenido o tokens. Obliga a inventariar y decidir qué modificar.
5. “cualquier otra fixture que nombre NegocioDoc o businessName” exige un inventario no listado; si el grep no es exhaustivo, obliga a decidir el alcance real.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, `core/wiki-index.ts` y test, `WikiLectura.test.tsx`, `core/imagenes.ts`, `core/rechazo.ts` y test, `rechazos-sldb.json`, `core/doc-ref.test.ts`, `styles/paper-tokens.css`; solo lectura de imports de `WorkbenchShell.tsx`. Cambios previstos: ejecutar el grep de inventario; introducir `storeTitle` con fallback `'Documentos'`; añadir alias deprecado; renombrar `NegocioDoc`, ajustar mensajes, tests y fixtures; actualizar textos CSS. Dependencias: que `WorkbenchShell` siga compilando con el alias; reglas de `check-layers`; configuración de Vitest intacta. Validaciones futuras: `npx tsc --noEmit`, Vitest indicado, `check-layers`, y grep final del `Done When`.

## FUTURO
Un ejecutor producirá el diff y ejecutará las validaciones; CI o un validador reportará sus resultados. Un humano decidirá si acepta el alias deprecado o exige migrar `WorkbenchShell`; otro nodo podrá cerrar la tarea comprobando el grep y los checks.
