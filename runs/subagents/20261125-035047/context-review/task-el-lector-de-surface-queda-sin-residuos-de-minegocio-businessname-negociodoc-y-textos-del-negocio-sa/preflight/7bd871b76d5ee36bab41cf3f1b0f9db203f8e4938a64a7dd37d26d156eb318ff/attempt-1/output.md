## REFORMULACION

Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/sldb`, paquete `surface`, eliminar de `surface/src` los residuos de "minegocio" del lector de documentos: los identificadores `NegocioDoc` y `businessName` y los textos `'La wiki de tu negocio'` / `'Este negocio ya tiene su pagina'`, presentes en `core/wiki-index.ts`, sus tests y una fixture. Resultado: `surface/src` no nombra esos términos; el título del índice se deriva del nombre del store (último segmento de la ruta que surface ya conoce) y, si no hay, del texto fijo `'Documentos'`. Límites: no se tocan `WorkbenchShell.tsx`, `vite.config.ts` ni `tsconfig`; validación con `tsc --noEmit`, `vitest` de `src/core`, `src/react`, `src/views` y `check-layers.mjs`.

## AMBIGUEDADES

1. Cita: "el titulo ... sale del nombre del store (el ultimo segmento de la ruta del store que surface ya conoce)". No indica qué campo/API contiene esa ruta ni cómo normalizar barras finales, segmentos vacíos o valores no textuales; obligaría a inventar la fuente y las reglas.
2. Cita: "mensajes con 'negocio' pasan a 'documento' o 'pagina'". No fija qué mensaje usa cada palabra ni la redacción final; obligaría a inventar el mapeo.
3. Cita: "la fixture que nombre NegocioDoc o businessName (encontrarla con el grep del paso 1)". No la identifica; si el grep devuelve varias o ninguna, no hay criterio de desempate.
4. Cita: "si no hay, el texto fijo 'Documentos'". No define "no hay": cadena vacía, `undefined`, `/`, `.` u otro.

## DRY-RUN

Lecturas: TaskDoc, `surface/src/core/wiki-index.ts`, `wiki-index.test.ts`, `WikiLectura.test.tsx`, fixture(s) y el helper de ruta de store; el grep del paso 1 como inventario. Cambios previstos: derivar el título del último segmento de la ruta del store con fallback `'Documentos'`; sustituir `NegocioDoc`/`businessName` por nombres genéricos; reescribir mensajes; ajustar tests y fixture. Dependencias: que la ruta del store esté disponible en `wiki-index`. Validaciones futuras: los tres comandos de Validation y el grep de Done When. Sin ejecutar nada.

## FUTURO

Un nodo ejecutor produce el parche y los logs de `tsc`, `vitest` y `check-layers`; un humano decide la redacción final de los mensajes y acepta el cierre.
