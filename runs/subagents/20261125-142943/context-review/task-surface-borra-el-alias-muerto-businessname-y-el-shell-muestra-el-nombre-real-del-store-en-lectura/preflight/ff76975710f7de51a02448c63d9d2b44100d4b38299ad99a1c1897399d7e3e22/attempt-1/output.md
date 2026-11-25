## REFORMULACION

Propósito: eliminar el alias muerto `businessName` en surface y hacer que la barra de Lectura muestre el nombre real del store. Resultado: `grep -rniE 'NegocioDoc|businessName|negocio' surface/src` sin resultados y `WorkbenchShell` recibiendo `storePath` desde `main.tsx` (o 'Documentos' + nota a sldb si serve no expone la ruta). Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: `surface/src/core/wiki-index.ts`, `surface/src/main.tsx` y, solo si hace falta, cliente de surface y un test; `sldb serve` queda fuera. Nodo ejecutable `task.code`.

## AMBIGUEDADES

1. "ver src/sldb/cli/serve/health.py y routes.py" frente a "Fuera: sldb serve" — no aclara si inspeccionar serve es lectura permitida o prohibida; obliga a inventar el alcance.
2. "si hace falta, el cliente de surface y un test" — no define el criterio de "hace falta"; obliga a inventarlo.
3. "si sldb serve lo expone... o hay nota a sldb pidiendolo" — la condición depende de código fuera de alcance; sin leerlo no se puede decidir; obliga a inventar la ruta o el criterio.
4. "npx vitest run src/core src/react src/views src/app src/workbench" frente a Done When "vitest de src/core src/app" — conjuntos distintos; obliga a elegir.
5. "No poner Task-Id en el commit de codigo" — no se indica si debe hacerse commit; obliga a inventarlo.

## DRY-RUN

Lecturas previstas: `wiki-index.ts:120-135`, `main.tsx:20-35`, `WorkbenchShell` (props/uso), `wiki-index.test.ts`, y solo lectura de `serve/health.py` y `routes.py`. Cambios: borrar líneas 127-128 sin sustituto; pasar `storePath` en `main.tsx:28`; ajustar/añadir test si se cablea. Dependencias: ruta de serve que exponga el store; si no, nota al inbox de sldb y mantener 'Documentos'. Validaciones futuras: `npx tsc --noEmit`; `npx vitest run ...`; `node scripts/check-layers.mjs`; grep final. Nada ejecutado.

## FUTURO

- sldb/serve decide si expone la ruta del store (respuesta al inbox).
- La decisión de JP de borrar `businessName` sin alias ya está cerrada.
- Un humano decide si hay commit y su mensaje.
- Otro nodo valida UI real y el grep de cierre.
