REFORMULACION  
Encargo: refactor ejecutable en el repo `/mnt/ssd/proyectos/SLDB_1/sldb`, área `surface/src`. Propósito: dejar el lector de surface sin residuos de minegocio (`businessName`, `NegocioDoc`, textos como “La wiki de tu negocio”). Resultado: `wiki-index` toma el título del último segmento de la ruta del store y cae a `Documentos`; el modo lectura de `WorkbenchShell` usa `storeTitle` sin maquinaria de negocio; el documento inicial es `route.doc` o el primero disponible; pasan `tsc`, `vitest` y `check-layers`. Límites: no tocar `vite.config.ts` ni `tsconfig`; el alcance declarado incluye `WorkbenchShell.tsx` y `workbench.test.tsx` por decisión de JP. No es un agregado ni paquete no ejecutable.

AMBIGUEDADES  
1. “fuera de WorkbenchShell.tsx, que no se toca” frente a “entran tambien src/app/WorkbenchShell.tsx y src/app/workbench.test.tsx”. Obliga a inventar si `WorkbenchShell.tsx` se modifica o no; sin tocarlo no se pueden quitar import/bloque/textos ni cumplir el grep final.  
2. “el titulo del indice de wiki-index sale del nombre del store (el ultimo segmento de la ruta del store que surface ya conoce)”. No define representación de ruta ni casos límite; obliga a inventar extracción, barras finales y fallback.  
3. “route.doc si viene, si no documents[0] (items?.[0] en l.109)”. No aclara qué es `items`; obliga a inventar la colección exacta en esa línea.  
4. “git cherry-pick ef45950d (rama deskops/deskops-e-b6060046cf05...)”. No define resolución si el commit no aplica limpio; obliga a inventar política de conflictos.

DRY-RUN  
Lecturas hipotéticas: TaskDoc, rituales `execution`, `testing`, `closeout`; `surface/src/core/wiki-index.ts`, `WorkbenchShell.tsx`, `workbench.test.tsx`, tests/fixtures citados; `git show ef45950d`. Cambios previstos: cherry-pick; quitar `businessName`/`NegocioDoc`/textos; derivar título; ajustar documento inicial; borrar/ajustar tests; limpiar CSS. Dependencias: commit accesible y aplicable; ruta de store disponible; scripts npm presentes. Validaciones futuras: `tsc`, `vitest` sobre las rutas indicadas, `check-layers` y greps de Done When. Nada ejecutado.

FUTURO  
Otro nodo ejecutor producirá el diff y la evidencia de tests; closeout actualizará Board y commit. Un humano debe resolver la contradicción sobre `WorkbenchShell.tsx` antes de ejecutar y decidir conflictos de cherry-pick.
