REFORMULACION
Nodo ejecutable (`task.refactor`) del repo sldb, superficie `surface`. Propósito: eliminar residuos de minegocio del lector genérico. Resultado: `surface/src` sin `NegocioDoc`, `businessName` ni textos del negocio, salvo alias deprecados y `WorkbenchShell.tsx`; el título del índice sale de `storeTitle` (último segmento de la ruta del store o `'Documentos'`); pasan `tsc`, los vitest de `src/core src/react src/views src/app` y `check-layers`. Límites: no tocar `WorkbenchShell.tsx`, `app/workbench.test.tsx`, `vite.config.ts` ni `tsconfig`; entran `core/wiki-index.ts` y su test, `WikiLectura.test.tsx`, `core/imagenes.ts`, `core/rechazo.ts` con test y fixture, `core/doc-ref.test.ts`, `styles/paper-tokens.css` y fixtures relacionadas. No hay pills ni átomos ligados en el input.

AMBIGUEDADES
1. «surface/src no nombra NegocioDoc, businessName» frente a «wiki-index exporta ademas ... 'export const businessName = storeTitle'»: contradicción; obliga a decidir si el alias cuenta como residuo.
2. «solo devuelve las lineas de alias deprecado» frente a «no nombra ... businessName»: el criterio de cierre contiene el mismo conflicto.
3. «tipos NegocioDoc pasan a un nombre generico (p. ej. DocumentoDoc)»: nombre no fijado; obliga a inventar el identificador.
4. «Mensajes con 'negocio' pasan a 'documento' o 'pagina'»: no se especifica qué mensaje usa cada término; obliga a inventar el mapeo.
5. «los textos de styles/paper-tokens.css»: no se citan selectores ni cadenas; obliga a inventar qué contenido es texto de negocio.
6. «el ultimo segmento de la ruta del store que surface ya conoce»: no se define cómo se obtiene la ruta ni casos límite (barra final, ruta vacía); obliga a inventar la derivación.
7. «surface/src entero salvo ... vite.config.ts y tsconfig»: no queda claro si esos archivos están bajo `surface/src`; obliga a asumir rutas.
8. La validación cubre cuatro directorios mientras el alcance es «surface/src entero»; obliga a decidir si hay más directorios que validar.

DRY-RUN
Hipotéticamente, un ejecutor leería el TaskDoc, los rituales execution/testing/closeout, el Board y los archivos nombrados. Haría `grep` de inventario; en `wiki-index.ts` renombraría a `storeTitle` con fallback y añadiría el alias de una línea; renombraría `NegocioDoc` condicionalmente; sustituiría textos; ajustaría tests, fixtures y CSS. Dependencias: import de `businessName` en `WorkbenchShell`, vitest y `check-layers`. Validaciones futuras: `tsc --noEmit`, vitest en los cuatro directorios y `check-layers`. Sin ejecutar nada.

FUTURO
JP migra `WorkbenchShell` a `storeTitle` y elimina el alias. El ritual de testing valida; closeout commitea y cierra. Un humano confirma nombres genéricos y textos finales.
