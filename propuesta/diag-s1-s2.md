# S1 ejecución

## Veredicto

**AUSENTE.** No existe ni una parte separable. De los 9 paquetes de primer nivel, **cero son hojas**: todos dependen de al menos otro paquete del sistema (grafo-imports.json, sección "paquetes"). El caso límite, verificado ejecutándolo: `import sldb.models.structured_doc` — el modelo de datos puro, la biblioteca que el proyecto anuncia ("structured Markdown to Pydantic and back", pyproject.toml) — carga en runtime los paquetes `core`, `models`, `runtime` y **`store`** (trazado con `sys.meta_path` sobre src/). La capa de conversión no puede importarse sin el motor de almacenamiento.

La cifra que parece contradecirlo (586 archivos, ninguno pasa de 138 líneas) no es modularización: es fragmentación re-pegada. La separación no está en el tamaño del archivo sino en si el paquete puede ejecutarse solo, y no puede ninguno.

## Evidencia

- `propuesta/evidencia/grafo-imports.json` → "paquetes": los 8 paquetes con código listan dependencias; `links` (la menos acoplada) depende de `store`; `models` depende de `runtime`. Ninguna lista vacía.
- Traza de import verificada: `sldb.core.exceptions.sldb_store_error.py` línea 2 (`from sldb.store.exceptions import StoreError`) es el punto donde el modelo puro arrastra el almacén. Ese archivo de 5 líneas es un puente de herencia múltiple (`SLDBStoreError(SLDBError, StoreError)`) y es suficiente para que `sldb.store` (con su `__init__.py` de 54 líneas que importa `store.models`, `store.io`…) se cargue en cada import de `sldb.models`.
- `src/sldb/core/exceptions/__init__.py` importa las 14 subclases de error, incluida la que tira del puente hacia store.
- Fragmentación, no modularidad — 5 de los archivos de ≤15 líneas verificados en src/:
  - `src/sldb/cli/commands/models_validate_utils.py` (3 líneas): re-export puro de `sldb.api.model_drafts` con `# noqa: F401`. Docstring: "Compatibility bridge".
  - `src/sldb/cli/commands/doc_lookup.py` (7 líneas): re-export puro de `sldb.api.documents.document_lookup.find_doc`. Docstring: "Compatibility bridge".
  - `src/sldb/cli/commands/find_utils.py` (5 líneas): re-export puro de `sldb.api.records.runtime_doc_proxy.RuntimeDocProxy`. Docstring: "Compatibility bridge".
  - `src/sldb/api/records/flatten.py` (10 líneas): código real (función recursiva).
  - `src/sldb/api/records/section_record.py` (11 líneas): código real (dataclass).
  - Patrón: el grep "Compatibility bridge" aparece en **11 archivos** de src/. Es decir: se extrae código de un archivo grande para respetar un límite de líneas, y un segundo archivo lo re-exporta para no romper importadores. La extracción no crea un módulo; crea dos nombres para el mismo código.
- `tamanos.json`: 90 archivos de ≤15 líneas sobre 586 (15,4%); promedio general 44 líneas/archivo. El tamaño chico coexiste con cero separabilidad de paquete.

## Patología

- Hoy: nadie puede tomar la capa de conversión (`models` + `runtime` + `core`) y usarla sin el almacén, ni tomar `store` sin `api` (ciclo api↔store de 196 aristas). El producto vendible — la biblioteca de conversión — no existe como unidad desplegable; existe solo dentro del sistema entero.
- El mecanismo de "archivos chicos" se usa como métrica de limpieza y produce puentes de compatibilidad que **re-pegan** lo separado: el código migrado (`sldb.api.model_drafts`) sigue siendo alcanzable por su ruta vieja (`sldb.cli.commands.models_validate_utils`), así que nada puede morir y la superficie de import no se contrae nunca.
- Si el autor se va: ningún paquete es candidato a extracción, y la única frontera real (api no importa cli, declarada en el docstring de `src/sldb/api/__init__.py`) existe como convención de una persona, no como propiedad del grafo.

# S2 coordinación

## Veredicto

**PRESENTE SIN MECANISMO.** La coordinación se hace a mano, arista por arista: imports diferidos dentro de funciones (91, superficie.json), comentarios de una línea explicando por qué se posterga un import, y ciclos mantenidos en 1-1 o 1-N asimétricos porque alguien decidió no cerrarlos de más. **Nada rechaza un ciclo nuevo**: `.github/workflows/ci.yml` ejecuta `pytest`, `python -m sldb selfdoc check` y `python -m build`; `pyproject.toml` no contiene ninguna herramienta de lint ni de control de imports (sin ruff, flake8, import-linter ni sección `[tool.*]` de ese tipo). Mañana alguien agrega un import que cierra un sexto ciclo y nada lo detiene: a lo sumo Python falla en runtime si el orden de inicialización lo rompe, lo cual no es garantía ni registro.

## Evidencia

- `propuesta/evidencia/grafo-imports.json` → "ciclos": 5 ciclos, cuatro de ellos con arista minoritaria única.
- `.github/workflows/ci.yml` (724 bytes, único workflow): pasos = install, `pytest`, `selfdoc check` (compara la referencia CLI generada, no el grafo de imports), `build`.
- `pyproject.toml`: `[project.optional-dependencies].dev` = scipy, build, pytest, pytest-cov. Sin lint, sin import-linter.
- Imports diferidos verificados (5 casos concretos en src/):
  1. `src/sldb/store/edge_index/model_contribution.py#L41` — `from sldb.api.schema.describe_field import describe_field  # a pydantic-only leaf; imported late so sldb.store never loads sldb.api at import time`. **Esquiva el ciclo api↔store**: es la única arista store→api, postergada a mano para que el ciclo no estalle al importar. Confesión escrita en el comentario.
  2. `src/sldb/models/structured_doc.py#L67` — `from sldb.runtime.validation import extract_model_data` dentro de `_extract_composed_payload`. **Esquiva el ciclo models↔runtime**: `runtime/validation.py` importa `models.structured_doc` a nivel de módulo (línea 8), así que models solo puede importar runtime dentro de un cuerpo de función.
  3. `src/sldb/api/documents/document_serialization.py#L18` — `from sldb.api.journal import doc_hashes  # deferred: import-safe during package init`. **Esquiva el orden de inicialización del propio paquete api** (api/__init__ importa documents y journal en cadena): no es un ciclo entre paquetes pero es el mismo gesto manual, dentro de api.
  4. `src/sldb/store/runtime_codec.py#L8` — `from sldb.runtime.validation import extract_model_data` dentro del método. **No esquiva ciclo** (store ya importa runtime a nivel de módulo; no existe ciclo store↔runtime): es carga perezosa del validador pesado.
  5. `src/sldb/cli/commands/init.py#L31` — `from sldb.core.exceptions import SLDBError` dentro de `_check_exists`. **No esquiva ciclo** (cli ya importa core arriba; no hay ciclo cli↔core): import perezoso en una rama de error.
  Balance: 3 de 5 son esquivas manuales de ciclos/orden de init, 2 son pereza ordinaria. El patrón dominante en superficie.json (los `from sldb.store import built_cache` diferidos en `section_paths.py#L9`, `section_sync.py#L23`, `semantic.py#L37`, `edge_index/cache_keys.py#L18`) repite el caso 3 dentro de store: los submódulos de store no pueden importar el `__init__` de su propio paquete a nivel de módulo.

## Patología

- Hoy: 5 ciclos vivos y 91 puntos donde el orden de import se resuelve a mano, dentro de cuerpos de función. Cada uno es correcto el día que se escribió y frágil para siempre: mover un import de función a módulo (refactorización trivial y deseable) puede romper el arranque, y nada en CI lo detecta antes de que `pytest` explote con un `ImportError` de orden.
- La regla de capas existe y está bien escrita — `src/sldb/api/__init__.py` líneas 6-8: "Layering: `sldb.cli` -> `sldb.api` -> `sldb.store` / `sldb.runtime` / `sldb.core`; nothing here imports `sldb.cli`" — y su cumplimiento depende de que el autor la recuerde. Es exactamente el antipatrón "estándares sin mecanismo": el docstring dice una cosa, el grafo dice otra (api importa store y store importa api).
- Si el autor se va: el sexto ciclo se agrega en silencio, los 91 diferidos se "arreglan" uno a uno rompiendo el arranque, y nadie tiene un comando que diga dónde está el ciclo.

## Los 5 ciclos

| ciclo | aristas ida | aristas vuelta | arista minoritaria | reparable? |
|---|---|---|---|---|
| api ↔ store | api→store: 195 | store→api: 1 | `src/sldb/store/edge_index/model_contribution.py` importa `api.schema.describe_field.describe_field` (introspección pydantic); el comentario admite que se posterga para no cargar api. Podría vivir en `models`/`core` y la arista desaparece. | **Sí** — accidente confeso en comentario |
| cli ↔ selfdoc | cli→selfdoc: 14 | selfdoc→cli: 1 | `src/sldb/selfdoc/python_relation_registry.py` importa `cli.model_utils.resolve_model_ref` a nivel de módulo, para cargar documentos runtime. `resolve_model_ref` es utilidad compartida; podría vivir en `api`/`core`. | **Sí** — mover una función |
| core ↔ runtime | core→runtime: 1 | runtime→core: 4 | `src/sldb/core/renderer_engine/python_expr.py` importa `runtime.config.python_expression_is_allowed` (una comprobación de política de config dentro del render). La política puede vivir en `core` o inyectarse. | **Sí** — accidente |
| core ↔ store | core→store: 1 | store→core: 8 | `src/sldb/core/exceptions/sldb_store_error.py` importa `store.exceptions.StoreError` solo para la herencia múltiple `SLDBStoreError(SLDBError, StoreError)`. La clase puente puede definirse en store o en un paquete de errores compartido. Es además la arista que hace que importar `models` cargue `store` (verificado). | **Sí** — mover una clase de 5 líneas; alto retorno |
| models ↔ runtime | models→runtime: 1 | runtime→models: 1 | `src/sldb/models/structured_doc.py` importa `runtime.validation.extract_model_data` (diferido, dentro de `_extract_composed_payload`); a la inversa `runtime/validation.py` importa `StructuredNLDoc`. Son las dos caras de la conversión texto↔modelo: el ciclo es semántico, no un accidente. | **Parcial** — exige rediseño (protocolo o mover el extractor), no un movimiento de archivo |