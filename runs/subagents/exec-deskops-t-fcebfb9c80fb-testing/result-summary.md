FALLA

# Tester deskops-t-fcebfb9c80fb: alias muerto y nombre del store en Lectura

Task: `task-surface-borra-el-alias-muerto-businessname-y-el-shell-muestra-el-nombre-real-del-store-en-lectura`
Commit revisado: `9384682fbaaf0ddc68aacbab955e97687f3685c4` — `surface: borra el alias businessName de wiki-index`
Archivos del commit: `surface/src/core/wiki-index.ts` (solo 2 líneas borradas). El commit no lleva Task-Id (el encargo pide no ponerlo); `283bb73c` es el commit de despacho.

## Veredicto

**FALLA.** La parte del alias está bien: `businessName` se borró sin sustituto y
`grep -rniE 'NegocioDoc|businessName|negocio' surface/src` no devuelve nada.
Pero la segunda mitad del encargo no se cumplió: Lectura sigue mostrando siempre
«Documentos» aunque `sldb serve` **sí** expone la ruta del store.

`GET /stores` ya devuelve `{"store": str(store_path), "root": str(root), ...}`
(`src/sldb/cli/serve/stores_routes.py:33-35`), con prueba existente en
`tests/test_serve.py::test_stores_describe_current_store` (líneas 893-905). El
encargo dice, textualmente, «averiguar de dónde lo obtiene surface hoy (… /health,
/schema u otra ruta que ya traiga la ruta o el nombre del store; ver
src/sldb/cli/serve/health.py y routes.py). Si ya existe, usarla». Existía y no se usó.

El ejecutor dejó `surface/src/main.tsx` sin pasar `storePath` y agregó
`desk/inbox/20261125-145224-suggestion-health-debe-traer-el-nombre-del-store.md`
pidiendo agregar `store_path` a `/health`. Esa nota es incorrecta: `/health` y
`/schema` no lo traen, pero `/stores` sí, desde antes del commit. La excepción del
«Done When» («o hay nota a sldb pidiéndolo») solo aplica si `sldb serve` no lo
expone; aquí sí lo expone, así que la nota no sustituye el cableado.

Resultado observable: en la app real `WorkbenchShell` recibe `storePath` undefined
(`surface/src/main.tsx:28`) y `storeTitle(undefined)` devuelve `"Documentos"`
(`surface/src/core/wiki-index.ts:123-126`). La prop y su test aislado
(`surface/src/app/workbench.test.tsx:385`) existen, pero nadie los alimenta.

## Validación ejecutada (detalle en validation.log)

| Comando | rc | Resultado |
|---|---|---|
| `cd surface && npx tsc --noEmit` | 0 | sin errores |
| `cd surface && npx vitest run src/core src/react src/views src/app src/workbench` | 0 | 35 archivos, 471 tests |
| `cd surface && npx vitest run src/core/wiki-index.test.ts src/app/workbench.test.tsx` | 0 | 26 tests |
| `cd surface && node scripts/check-layers.mjs` | 0 | contrato de capas OK |
| `bash tools/check.sh --fast` | 0 | todas las puertas pasan |
| `pytest tests/test_serve.py::test_stores_describe_current_store` | 0 | 1 passed (demuestra `/stores`) |

El commit no toca archivos `.py` ni tests de Python; no hay un `tests/test_wiki_index.py` equivalente. No se corrió la suite completa.

## Qué falta para PASA

1. Agregar `stores()` (o equivalente) a `SldbClient` leyendo `GET /stores`.
2. En `main.tsx` (o en el shell), obtener la ruta/nombre del store y pasar
   `storePath` a `WorkbenchShell`; elegir `root` o `store` según qué nombre deba
   verse (con `store` el último segmento puede ser `.sldb`; con `root`, el nombre
   del proyecto).
3. Cubrir el cableado con un test de `main`/shell; el test de `storeTitle` ya existe.
4. Corregir o retirar la nota a sldb: `/stores` ya expone la ruta; no hace falta
   agregarla a `/health`.

## Observaciones no bloqueantes

- El alias muerto quedó eliminado correctamente y `GraphDocument` sigue usándose en
  el archivo, así que no hay import huérfano.
- La nota del inbox existe en `desk/inbox/` y como `InboxNoteDoc`, pero su premisa
  («sldb serve no lo expone») es falsa.
- Entorno: `/tmp/ws-venv` no existía; se usó `/dev/shm/tester-venv/bin/python`
  (Python 3.12.16) y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-fcebfb9c80fb`.
