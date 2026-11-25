PASA
quick_gates rc=0

# Tester exec-deskops-t-1b08c45a3f10: alias muerto y nombre del store en Lectura

Task: `task-surface-borra-el-alias-muerto-businessname-y-el-shell-muestra-el-nombre-real-del-store-en-lectura`
Commit revisado: `35d35097fba74e27b26cc20c24aaf35b92df50af` — `surface: Lectura muestra el nombre del store servido (GET /stores)`
Prerrequisito ya en el árbol: `9384682fbaaf0ddc68aacbab955e97687f3685c4` — `surface: borra el alias businessName de wiki-index` (no se rehizo).
El commit de código no lleva `Task-Id`, como pide el encargo; la búsqueda por ese trailer no lo encuentra y se localizó por el mensaje y la fecha (15:39:41Z).
Archivos del commit: `surface/src/app/WorkbenchShell.tsx`, `surface/src/app/workbench.test.tsx`, `surface/src/core/client.ts`.

## Veredicto

**PASA.** Se cumplen las dos mitades del encargo:

- `grep -rniE 'NegocioDoc|businessName|negocio' surface/src` no devuelve nada (rc=1).
- Lectura ya no queda clavada en «Documentos»: `SldbClient.storeInfo()` pide `GET /stores`, `WorkbenchShell` la consulta al montar y pasa la ruta servida a `storeTitle`. Mientras carga o si la petición falla, sigue mostrando «Documentos». La prop `storePath`, si se pasa, conserva prioridad.

El commit no toca `surface/src/main.tsx`; el cableado asíncrono vive en el propio `WorkbenchShell` (que crea o recibe el cliente), no en `main.tsx`. Es una desviación de la ruta sugerida en el Implementation Path, pero cumple el resultado observable y mantiene el fallback pedido.

## Validación ejecutada

| Comando | rc | Resultado |
|---|---|---|
| `cd surface && npx tsc --noEmit` | 0 | sin errores |
| `cd surface && npx vitest run src/core src/react src/views src/app src/workbench` | 0 | 35 archivos, 472 tests passed |
| `cd surface && npx vitest run src/app/workbench.test.tsx -t "Lectura"` | 0 | 3 passed, 12 skipped |
| `cd surface && node scripts/check-layers.mjs` | 0 | 76 módulos L0..L3, sin violaciones |
| `pytest -q tests/test_serve.py::test_stores_describe_current_store` | 0 | 1 passed (contrato real de `GET /stores`) |
| `bash tools/check.sh --fast` | 0 | todas las puertas pasan (núcleo aislado, capas, identidad, ejes, superficie) |

El commit no incluye archivos `.py` ni tests de Python; los tests que agrega son vitest. No se corrió la suite completa.

Comprobación extra del cliente real (temporal, ya borrada, sin dejar cambios en `surface/`): con `createHttpClient("/sldb", fetchMock)` y un mock que responde a `/sldb/stores`, `storeInfo()` devuelve `{store, root}` y pide exactamente `GET /sldb/stores`. El test permanente del commit stubea `client.storeInfo` en vez de mockear `fetch`, pero la cadena cliente→shell queda verificada por las dos piezas.

## Observaciones no bloqueantes

- El test nuevo cubre el shell con un `storeInfo` inyectado, no el `fetch` de `/stores`; si se quiere cobertura permanente del método HTTP, falta un test de `src/core/client.ts`.
- `GET /stores` devuelve el directorio del store (`<raíz>/.sldb` en un store de proyecto), así que en la app real el título será `.sldb`, no el nombre del proyecto. Si JP espera el nombre del proyecto, habría que usar `root`; el encargo pedía «el nombre del store» y el prop documenta que titula el último segmento de la ruta del store, así que no lo considero fallo.
- Sigue en `desk/inbox/20261125-145224-suggestion-health-debe-traer-el-nombre-del-store.md` la nota a sldb que dice que `/health` y `/schema` no exponen el store y pide agregarlo. Su premisa es incompleta: `GET /stores` ya lo expone desde antes. No está en el Scope de esta tarea, pero conviene retirarla o corregirla en closeout.
- Entorno: `/tmp/ws-venv` no existía; se usó el venv del repo `/workspace/sldb/.venv` (Python 3.13.18) primero en `PATH`, con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-1b08c45a3f10`.
