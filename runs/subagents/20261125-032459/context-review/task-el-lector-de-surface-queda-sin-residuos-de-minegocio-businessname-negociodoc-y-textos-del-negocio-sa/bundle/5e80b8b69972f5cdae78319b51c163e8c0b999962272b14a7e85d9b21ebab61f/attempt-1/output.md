## REFORMULACION

**Propósito:** eliminar del lector genérico de surface los residuos específicos de minegocio (`businessName`, `NegocioDoc` y textos como “La wiki de tu negocio” o “Este negocio ya tiene su pagina”) que quedaron tras la tarea 3cc5c36b.

**Resultado:** `surface/src/core/wiki-index.ts` y sus tests no nombran esos conceptos; el título del índice procede de un dato genérico con fallback neutro; `tsc`, `vitest` y `check-layers` pasan.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`, área `surface/`.

**Límites:** solo `wiki-index.ts`, `wiki-index.test.ts`, `WikiLectura.test.tsx` y la fixture necesaria. No tocar `WorkbenchShell.tsx`, `vite.config.ts` ni `tsconfig`.

El nodo es ejecutable, no un agregado: `atoms: []`, `depends_on: []`, sin hijos que recorrer.

## AMBIGUEDADES

1. “el titulo del indice sale de un dato generico (nombre del store o del documento raiz) con un texto de respaldo neutro”. Da dos fuentes alternativas y no fija el fallback; obliga a inventar cuál usar y el texto exacto.
2. “la fixture que lo necesite”. No identifica el archivo; obliga a inventar cuál es.
3. En Done When: “grep -rn 'NegocioDoc\|businessName\|tu negocio' surface/src … vacio”, pero el Rationale cita “'Este negocio ya tiene su pagina'”, que ese patrón no captura. Obliga a inventar si se elimina y cómo se verifica.
4. Scope limita a `wiki-index` y su fixture, mientras Done When exige grep vacío en todo `surface/src` salvo `WorkbenchShell.tsx`. Obliga a inventar si se corrige fuera del alcance declarado.
5. “textos del negocio” no enumera las cadenas; obliga a inventar el conjunto exacto.

## DRY-RUN

**Lecturas:** TaskDoc, Board, rituales execution/testing/closeout, pills y átomos ligados (ninguno), `wiki-index.ts`, sus tests y fixture; `WorkbenchShell.tsx` solo para confirmar la exclusión.

**Cambios previstos:** grep de los términos; sustituir las referencias por la fuente genérica elegida; ajustar tests y fixture; no tocar archivos excluidos.

**Dependencias:** decisión previa sobre fuente y fallback; no hay pills ni depends_on que resolver.

**Validaciones futuras:** `cd surface && npx tsc --noEmit && npx vitest run && node scripts/check-layers.mjs`; grep de Done When; auditoría de contexto y closeout.

## FUTURO

Un humano debe decidir la fuente genérica del título y el texto de respaldo, y si el grep de Done When amplía el alcance. El ritual de testing ejecutará la suite; closeout hará el commit atómico, retirará la tarea del Board y, si aparece residuo fuera de alcance, otro nodo creará una tarea nueva.
