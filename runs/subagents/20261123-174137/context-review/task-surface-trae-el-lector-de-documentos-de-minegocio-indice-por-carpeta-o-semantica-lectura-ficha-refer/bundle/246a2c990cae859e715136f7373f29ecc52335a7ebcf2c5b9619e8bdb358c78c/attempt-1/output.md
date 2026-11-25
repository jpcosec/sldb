## REFORMULACION

Propósito: trasladar a `sldb/surface` la parte genérica del lector de documentos que quedó en la copia de minegocio (commit ab8fac2, base sldb 562847e2). Resultado: surface con índice por carpeta o semántica, lectura, ficha, referencias y rechazos legibles, operando contra `sldb serve` sobre el store de deskops, sin textos, rutas ni datos del negocio. Repo: `sldb`, área `surface/`. Límites: no tocar `WorkbenchShell.tsx`, `vite.config.ts` ni `tsconfig` sin señalarlo en el informe; la semántica queda supeditada a la unificación de tags de deskops; validación con tsc, vitest y check-layers.

## AMBIGUEDADES

1. «la parte generica del lector» / «lo especifico del negocio queda fuera»: no hay criterio de corte; obligaría a inventar qué archivos o fragmentos son genéricos.
2. «funciona contra sldb serve sobre el store real de deskops»: no se indica URL, puerto ni ruta del store; obligaría a inventar el destino.
3. «agrupar por carpeta y dejar la semantica conectada»: «conectada» no define comportamiento (flag, fallback, interfaz); obligaría a inventarlo.
4. «los tiempos medidos de cada pantalla»: no hay umbral ni formato; obligaría a inventar el criterio de aceptación.
5. «sin cambios o con el cambio senalado»: no se dice cuál sería ese cambio; obligaría a inventarlo.
6. Se pide medir tiempos en «Done When» pero Validation solo enumera tsc, vitest y check-layers; obligaría a decidir si medir es bloqueante.

## DRY-RUN

Nodo ejecutable (`task.code`), no agregado. Lecturas: TaskDoc, rituales, copia en `reports/lector-minegocio-20261123/superficie`, `surface/` actual, `package.json` y estado de la tarea de tags de deskops. Cambios previstos: portar `core/{doc-ref,wiki-index,rechazo,imagenes}.ts` y tests, fixture `rechazos-sldb.json`, `workbench/{WikiIndex,Ficha,NuevaPagina,AvisoGuardado}.tsx`, `WikiLectura.test`, y cambios en `core/client.ts`, `layout.ts`, `main.tsx`, `react/*`, `paper-tokens.css`, `ComposerView`, `ProsaWorkbenchView`, `workbench.test`. Dependencias: copia fuente, `sldb serve` y tags unificados. Validaciones futuras: `npx tsc --noEmit`, `npx vitest run`, check-layers y medición manual de pantallas.

## FUTURO

La tarea de deskops de vocabulario de tags produce la condición para agrupar por semántica. El coordinador recibe el informe y decide si integra cambios en WorkbenchShell, vite o tsconfig. JP valida la exploración del store.
