PASA

# Testing — surface trae el lector de documentos de minegocio

Commit del ejecutor: `3cc5c36bfb4bf91e406bbf2129783d4c1a3376f1` — `surface: lector de documentos de minegocio (indice, lectura, ficha, referencias, rechazos legibles)`, con el trailer `Task-Id` correcto. Toca **solo** `surface/` (26 archivos, +2944/−128); no toca `vite.config.ts` ni `tsconfig.json`. `src/app/WorkbenchShell.tsx` sí se modifica y el informe del ejecutor lo **señala explícitamente para el coordinador**, como pedía el alcance.

## Veredicto

**PASA.** La validación propia de la tarea pasa completa: `tsc --noEmit`, `vitest run` (35 archivos / 471 tests) y `check-layers` (76 módulos, 0 violaciones), todo rc 0. Los 7 archivos de test nuevos/modificados también pasan de a uno. El lector responde contra `sldb serve` sobre el store real de deskops (2085 documentos): índice por carpeta con la semántica conectada, lectura, ficha/segmentos, referencias y rechazos legibles.

## Validación ejecutada (detalle en `validation.log`)

| Comando | rc | Resultado |
|---|---|---|
| `cd surface && npx tsc --noEmit` | 0 | sin errores |
| `cd surface && npx vitest run` | 0 | 35 archivos, 471 tests |
| `cd surface && node scripts/check-layers.mjs` | 0 | 76 módulos L0..L3, 0 violaciones |
| `bash tools/check.sh --fast` | 1 | solo falla **identidad** (ver abajo) |

Tests de a uno: `doc-ref` 5, `wiki-index` 12, `rechazo` 18, `imagenes` 4, `WikiLectura` 22, `ProsaWorkbenchView` 34, `workbench` 14 — todos rc 0.

No hay `tests/*.py` en el commit: no toca Python ni agrega tests de pytest. Se exportó `PYTEST_ADDOPTS` igual, según el instructivo.

## La única puerta en rojo: identidad (`workbench_demo`), preexistente y ajena al commit

`bash tools/check.sh --fast` termina rc 1 por `identidad: directorio versionado sin clasificar en la raíz: workbench_demo`. Lo verifiqué en un worktree detached del **commit padre** (`b3df70da`, sin los cambios de surface): `tools/check_identity.py` falla idéntico, rc 1. `workbench_demo` entró en `562847e2` y este commit no toca `contracts/identity.toml` ni ese directorio. Existe la tarea de decisión `task-clasificar-workbench-demo-en-contracts-identity-toml-…`, que documenta la autorización del coordinador para commitear con esa puerta en rojo tarea por tarea. Por eso **no** lo cuento como falla del commit; si el coordinador aplica la regla de `check.sh --fast` al pie de la letra, este es el único rc distinto de 0 y es preexistente.

## Humo contra el store real de deskops

`PYTHONPATH=src .venv/bin/python -m sldb serve --port 8799 --store /mnt/ssd/proyectos/SLDB_1/deskops/.sldb`:

- `/health` 200 (arranque en frío ~45 s).
- `/graph` 200, 4527 KB, **4.6 s** (2085 docs, 2 corridas); el ejecutor reportó 3.5 s.
- `/document?id=<TaskCodeDoc real>` 200, 41 KB, **68 ms**.
- `/document/segments?id=…` 200, 16 KB, **23 ms**.
- `/schema` 25 ms; `/models` 20 ms.
- El store no tiene ids duplicados (0/2085), así que `docRef` usa el nombre simple y las lecturas responden. Los tiempos son del cómputo/HTTP, no del render en navegador.

## Revisión del alcance

- Portados y presentes: `core/{doc-ref,wiki-index,rechazo,imagenes}.ts` + tests + `__fixtures__/rechazos-sldb.json`; `workbench/{WikiIndex,Ficha,NuevaPagina,AvisoGuardado}.tsx` + `WikiLectura.test.tsx`; cambios genéricos en `client.ts`, `layout.ts`, `main.tsx`, `react/{context,DocumentSurface,useDocumentEditor}`, `paper-tokens.css`, `ComposerView`, `ProsaWorkbenchView` y `workbench.test.tsx`.
- Fuera y reportado: `vite.config.ts`/`tsconfig.json` sin cambios; se omitió `base: SUPERFICIE_BASE` y los textos/README/HANDOFF/assistant propios de minegocio.
- Agrupado: por carpeta (primer segmento del path) y semántica conectada; no se verificó la unificación de tags de deskops, tal como preveía el alcance.
- Residuo específico de negocio en código de producción (`businessName`/`NegocioDoc`, el texto de respaldo «La wiki de tu negocio», «Este negocio ya tiene su página»): es inerte en deskops (no hay `NegocioDoc`) y el ejecutor lo declaró. Los nombres de negocio en tests y en la fixture son datos de prueba exigidos por el propio alcance.

## Observaciones no bloqueantes

- `is_tracked` (`src/sldb/cli/serve/tracked_docs.py`) valida solo `doc.name`, no `Tipo/nombre`, aunque `resolve_runtime_doc` sí acepta esa forma. Si un store tuviera nombres repetidos entre modelos, abrir la referencia calificada daría 404 pese a lo que promete `doc-ref`. Es una limitación **preexistente del servidor** (fuera de este commit) y no se dispara en deskops (0 duplicados); conviene tenerla presente si se usa el lector con otro store.
- La medición del ejecutor (3.5 s) y la mía (4.6 s) para `/graph` difieren; el orden de magnitud y el cuello de botella (el grafo) coinciden. El arranque en frío del serve es de decenas de segundos.
