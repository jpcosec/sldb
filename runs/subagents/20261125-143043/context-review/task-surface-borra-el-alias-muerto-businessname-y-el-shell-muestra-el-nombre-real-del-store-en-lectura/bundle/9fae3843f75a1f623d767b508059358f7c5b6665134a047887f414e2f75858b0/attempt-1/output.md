## REFORMULACION

**Propósito:** eliminar el alias muerto `businessName` reintroducido en `surface/src/core/wiki-index.ts` y hacer que la barra de Lectura muestre el nombre real del store servido.

**Resultado:** `grep -rniE 'NegocioDoc|businessName|negocio' surface/src` sin resultados; Lectura con el nombre del store si `sldb serve` lo expone; `tsc`, `vitest` y `check-layers` verdes.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`.

**Límites:** `surface/src/core/wiki-index.ts`, `surface/src/main.tsx` y, si hace falta, cliente de surface y un test. Fuera: `sldb serve`; si no expone la ruta, nota por inbox a sldb y mantener `'Documentos'`. Commit de código sin Task-Id.

## AMBIGUEDADES

1. "averiguar de donde lo obtiene surface hoy (cliente de sldb serve: /health, /schema u otra ruta...)" — no fija endpoint ni campo; obligaría a inventar cuál usar o a decidir tocar `sldb serve` (fuera de alcance).
2. "si hace falta, el cliente de surface y un test" — no define cuándo hace falta; obligaría a inventar el criterio.
3. "Que surface/src no nombre businessName ni negocio" frente a "grep -rniE 'NegocioDoc|businessName|negocio' surface/src no devuelve nada" — el substring puede coincidir con texto legítimo; obligaría a inventar si se borran ocurrencias válidas.
4. "el shell muestra el nombre real del store" vs "WorkbenchShell recibe una prop nueva storePath" — no aclara si mostrar ruta completa, basename o nombre; obligaría a inventar el formato.
5. "agregar o ajustar un test de main/shell si se cablea storePath" — sin criterio de cobertura; obligaría a inventar qué aserta.

## DRY-RUN

**Lecturas:** TaskDoc y rituales; `wiki-index.ts:127-128`; `main.tsx:28`; `WorkbenchShell`; cliente de surface; `src/sldb/cli/serve/health.py` y `routes.py`; `wiki-index.test.ts`.

**Cambios previstos:** borrar comentario y alias; derivar `storePath` de un endpoint ya existente o dejar `'Documentos'`; ajustar/añadir test de shell/main.

**Dependencias:** ruta de `sldb serve` que exponga store; vitest; check-layers.

**Validaciones futuras:** `npx tsc --noEmit`; `npx vitest run src/core src/react src/views src/app src/workbench`; `node scripts/check-layers.mjs`; grep. Sin ejecutar nada.

## FUTURO

Decisión humana ya tomada: borrar sin alias. Si `sldb serve` no expone el nombre, un nodo de sldb (inbox) decide y añade la ruta; el ritual de closeout hace commit y cierre. No son ambigüedades.
