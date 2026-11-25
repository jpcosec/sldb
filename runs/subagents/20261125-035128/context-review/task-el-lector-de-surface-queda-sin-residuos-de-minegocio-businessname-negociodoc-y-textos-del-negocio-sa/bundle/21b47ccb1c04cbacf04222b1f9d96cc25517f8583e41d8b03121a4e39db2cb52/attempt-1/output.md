## REFORMULACION

Encargo: refactorizar `surface/src` para eliminar residuos de minegocio del lector genérico, dejando fuera `WorkbenchShell.tsx`, `vite.config.ts` y `tsconfig`. Resultado: `surface/src` no nombra `NegocioDoc`, `businessName` ni textos del negocio; el título del índice en `wiki-index` se deriva del nombre del store (último segmento de su ruta, que surface ya conoce) o, en su defecto, `Documentos`; mensajes con "negocio" pasan a "documento"/"página". Se ajustan `wiki-index.ts`, `wiki-index.test.ts`, `WikiLectura.test.tsx` y la fixture afectada. Repo: sldb, área `surface`. Límite: `tsc --noEmit`, `vitest` de `src/core`, `src/react`, `src/views` y `check-layers` deben pasar, y el grep final no debe devolver nada.

## AMBIGUEDADES

1. "sale del nombre del store (el ultimo segmento de la ruta del store que surface ya conoce)": no se especifica cómo `wiki-index` obtiene esa ruta (¿parámetro, prop, hook?) ni qué pasa con rutas con barra final o vacías. Obligaría a inventar la API y el criterio de normalización.
2. "'negocio' pasan a 'documento' o 'pagina'": la elección entre ambos textos y su redacción exacta no está fijada. Obligaría a inventar copy final.
3. "grep ... --exclude=WorkbenchShell.tsx para el inventario completo": el Scope también excluye `vite.config.ts` y `tsconfig`, pero el grep solo excluye `WorkbenchShell.tsx`. Obligaría a decidir si esos archivos entran en el inventario.
4. "la fixture que nombre NegocioDoc o businessName (encontrarla con el grep del paso 1)": no se nombra ruta ni archivo. Obligaría a inventar su ubicación si el grep no la identifica.
5. "node scripts/check-layers.mjs": ejecutado tras `cd surface`, no queda claro si el script vive en `surface/scripts` o en la raíz del repo. Obligaría a inventar la ruta.

## DRY-RUN

Lecturas: TaskDoc, Board, pills y átomos ligados, `surface/src/core/wiki-index.ts`, `wiki-index.test.ts`, `WikiLectura.test.tsx`, fixture hallada por grep, `WorkbenchShell.tsx` (solo para no tocarlo) y `check-layers.mjs`. Cambios previstos: derivación del título desde el nombre del store con fallback `Documentos`; sustitución de mensajes; ajuste de tests y fixture. Dependencias: fuente de la ruta del store ya disponible en surface, reglas de `check-layers`, configuración de vitest. Validaciones futuras: grep sin resultados, `tsc`, `vitest` de los tres directorios y `check-layers`.

## FUTURO

Un humano decide el copy exacto de los mensajes y el criterio ante rutas límite; `deskops` liga pills y actualiza el Board; el nodo de testing ejecuta las validaciones; el de closeout audita git, commitea y retira la tarea.
