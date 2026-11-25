## REFORMULACION

Encargo ejecutable único (no agregado) en el repo `/mnt/ssd/proyectos/SLDB_1/sldb`, subproyecto `surface`. Propósito: eliminar residuos de “minegocio” del lector genérico de surface (`businessName`, `NegocioDoc`, textos como “La wiki de tu negocio” o “Este negocio ya tiene su página”). Resultado: `surface/src` sin esos nombres ni textos; el título del índice de `wiki-index` se deriva del último segmento de la ruta del store y, si no hay, usa `'Documentos'`. Límites: todo `surface/src` salvo `vite.config.ts` y `tsconfig`, con la excepción declarada de `src/app/WorkbenchShell.tsx` y `src/app/workbench.test.tsx`. Se parte del intento 2 mediante cherry-pick de `ef45950d`.

## AMBIGUEDADES

1. “fuera de WorkbenchShell.tsx, que no se toca” frente a “entran tambien src/app/WorkbenchShell.tsx y src/app/workbench.test.tsx”. Obliga a inventar si ese archivo se modifica o no.
2. “(y el alias que dejo el intento 2)”: no se nombra el alias. Obliga a inventar cuál eliminar.
3. “el ultimo segmento de la ruta del store que surface ya conoce”: no se especifica cómo `wiki-index` obtiene esa ruta. Obliga a inventar la API o el parámetro.
4. “textos de styles/paper-tokens.css”: no se enumeran. Obliga a inventar qué cadenas borrar.
5. “si hace falta, un test nuevo de que en Lectura se ve storeTitle”: criterio subjetivo. Obliga a inventar cuándo es necesario.
6. “l.~349”, “l.~387”, “l.~384”: referencias aproximadas que pueden desplazarse tras el cherry-pick. Obliga a inventar la localización exacta.
7. “route.doc si viene, si no documents[0] (items?.[0] en l.109)”: no queda claro si `documents` e `items` son la misma colección. Obliga a inventar la variable correcta.

## DRY-RUN

Lecturas: TaskDoc, `core/wiki-index.ts` y su test, `WorkbenchShell.tsx`, `workbench.test.tsx`, `core/imagenes.ts`, `core/rechazo.ts` con test y fixture, `core/doc-ref.test.ts`, `styles/paper-tokens.css`, `scripts/check-layers.mjs`; commit `ef45950d`. Cambios previstos: cherry-pick; borrar `businessName`/`NegocioDoc` y textos de negocio; derivar `storeTitle` con fallback `'Documentos'`; modo lectura genérico; documento inicial `route.doc ?? documents[0]`; ajustar/borrar tests; limpiar CSS. Dependencias: acceso a rama/commit, worktree limpio, mapeo de líneas. Validaciones futuras: `npx tsc --noEmit`, `npx vitest run` sobre las rutas indicadas, `node scripts/check-layers.mjs` y los `grep` de Done When.

## FUTURO

El ejecutor resolverá conflictos del cherry-pick y el mapeo de líneas; un humano/JP deberá confirmar la contradicción de alcance y la lista de alias/textos; otro nodo ejecutará las validaciones y revisará el diff antes del cierre.
