FALLA

# Tester deskops-t-78c922eaaaca: resultado

Task: `task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa`
HEAD revisado: `617e008ae3c7b7d241da2f54c399ef864824270b`
Commits con `Task-Id` de la task:
- `f94ea4e7b7ab6c504c3b6b99e07645b773f25521` — `surface: lector sin residuos de minegocio (storeTitle, sin businessName/NegocioDoc/informe)` (11 archivos, el grueso del trabajo)
- `c5a8a9dd904fcabe65b03fa1929bec77e12457d0` — `surface: wiki-index sin residuos de minegocio (storeTitle)` (1 archivo; **reintroduce el alias prohibido**)

## Veredicto

**FALLA.** El trabajo de `f94ea4e7` cumple casi todo: `WorkbenchShell` ya no usa `businessName`/`NegocioDoc`/`informe`, el modo Lectura es genérico (`route.view === "workbench" && route.lens === "lectura"`), la barra usa `storeTitle(storePath)` y el documento inicial es `route.doc` o el primero. Pero el commit final `c5a8a9dd` vuelve a declarar `businessName` en `surface/src/core/wiki-index.ts`, justo lo que la task manda borrar «sin alias».

El `Done When` explícito no se cumple:

```
$ grep -rniE 'NegocioDoc|businessName|negocio' surface/src
surface/src/core/wiki-index.ts:128:export const businessName = (_documents: GraphDocument[]): string | null => null;
rc=0
```

El alias es código muerto (nadie lo importa en `surface/src`), así que borrar las líneas 127–128 no rompe `tsc` ni los tests; pero su presencia incumple el criterio de aceptación y deja el nombre exacto que la task quería erradicar. El comentario que lo acompaña («alias para WorkbenchShell.tsx (trabajo local de JP)») no se sostiene: el shell actual importa `storeTitle`, no `businessName`.

## Validación ejecutada (detalle en `validation.log`)

| Comprobación | Comando | rc | Resultado |
|---|---|---|---|
| Residuos (Done When 1) | `grep -rniE 'NegocioDoc|businessName|negocio' surface/src` | 0 | **1 hit: `businessName` en wiki-index.ts:128** |
| `informe` en el shell (Done When 2) | `grep -n 'informe' surface/src/app/WorkbenchShell.tsx` | 1 | sin coincidencias (correcto) |
| Tipos | `cd surface && npx tsc --noEmit` | 0 | OK |
| Tests de surface | `cd surface && npx vitest run src/core src/react src/views src/app src/workbench` | 0 | 35 archivos, 471 tests pasan |
| Capas | `cd surface && node scripts/check-layers.mjs` | 0 | 76 módulos, 0 violaciones ni mocks |
| Puertas rápidas del desk | `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No hay archivos `tests/*.py` en los commits (el cambio es TypeScript); por eso la validación es la de la task (`tsc`, `vitest`, `check-layers`), no pytest. `/tmp/ws-venv` no existía; usé `/workspace/sldb/.venv` para `tools/check.sh`, que pasa.

## Comprobaciones adicionales

- `WorkbenchShell.tsx`: sin `businessName`, `NegocioDoc`, `esWiki` ni `document.title = negocio`; `titulo = storeTitle(storePath)`, `wikiLectura` genérico para cualquier store, texto de barra `wiki-titulo` y sin los textos «La wiki de tu negocio».
- Selección inicial: `items?.[0]` / `documents[0] ?? null`, con `route.doc` primero; no queda la búsqueda por `"informe"`.
- Tests ajustados: se borró el caso «wiki de un negocio en Lectura… (Peluquería Rayén)» y se añadió «Lectura: la barra muestra el título del store y esconde la maquinaria» con `storePath="/datos/mis-notas"`. Pasan.
- Fixtures y modelos de test migrados de `NegocioDoc` a `DocumentoDoc`, y `minegocio.paginas` a `sldb.paginas`.

## Observaciones no bloqueantes

- Quedan referencias de dominio del store de ejemplo en tests/comentarios (`Peluquería Rayén`, «store de la peluquería», `Rayén Soto`, `balayage`). No disparan el `grep` del `Done When`, pero son «textos del negocio» del demo; si el alcance incluye limpiarlos, conviene decidirlo aparte.
- `storePath` es una prop nueva de `WorkbenchShell` y ningún caller de producción la pasa (`src/main.tsx` sigue renderizando `<WorkbenchShell baseUrl … client … subirImagen … />`). Tal como está, en la app real la Lectura mostrará siempre «Documentos». No es la causa del veredicto (la task pedía `storeTitle(ruta del store)` y el test lo cubre con la prop), pero la ruta real del store no queda conectada; merece una decisión de JP.

## Para pasar

Borrar las líneas 127–128 de `surface/src/core/wiki-index.ts` (comentario y `export const businessName = …`), sin alias sustituto. Después repetir: `grep -rniE 'NegocioDoc|businessName|negocio' surface/src` (debe salir rc=1 sin salida), `npx tsc --noEmit`, `npx vitest run src/core src/react src/views src/app src/workbench` y `node scripts/check-layers.mjs`.
