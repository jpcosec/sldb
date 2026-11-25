## REFORMULACION
Encargo: en el repo SLDB_1, modificar el modelo `SpecDoc` (`src/sldb/models/notation/spec_doc.py`) para que conserve los datos de un spec que no son elementos, en particular `data.entity`, y asegurar que el `style` llegue a la vista resuelta. Resultado: campo opcional `data: dict[str, Any]` con render/extract reversibles, escritura en `src/sldb/api/notations/spec_sync_docs.py`, round-trip de `data.entity`, `style` presente en `resolve_view`, tests en `tests/notations/test_spec_sync.py` (y `test_spec_loader.py` si aplica), `sldb stores build --check`, CHANGELOG y commit. Límites: no reexportar clases, no cambiar el YAML de specs, no migrar el `SpecDoc` de `docs.models`.

## AMBIGUEDADES
1. “leer primero la nota de origen completa para fijar qué claves de data pide IR11”: la nota no está en el input; obligaría a inventar el conjunto exacto de claves.
2. “cualquier otra clave de data que no sea elementos”: no define “elementos” ni “afines”; obligaría a inventar el criterio de inclusión/exclusión.
3. “con render y extract reversibles en la plantilla del modelo”: no indica sintaxis ni marcador; obligaría a inventar el formato.
4. “comprobar con un test que resolve_view ... pasa style a la vista resuelta”: no define la forma esperada de `style`; obligaría a inventar el contrato de la vista.
5. “tests/notations/test_spec_loader.py si hace falta”: criterio discrecional; obligaría a decidir sin base cuándo es necesario.
6. Validation no incluye `test_spec_loader.py` aunque Scope lo menciona; obligaría a elegir qué validación es exigible.
7. “data: dict[str, Any] = {}”: valor por defecto mutable, sin aclarar `None`; obligaría a inventar la convención.

## DRY-RUN
Es una tarea ejecutable, no un agregado. Lecturas previstas: nota de origen, `spec_doc.py`, `spec_sync_docs.py`, resolvedor de vistas, tests y `.sldb`. Cambios previstos: añadir campo y marcador de plantilla, escribirlo en la sincronización, propagar `style` si falta, añadir tests y CHANGELOG. Dependencias: contenido de la nota de origen, API de vistas, store existente, pytest y `sldb`. Validaciones futuras: los tres comandos listados, sin ejecutar ahora.

## FUTURO
Otro nodo o humano debe aportar la nota de origen y fijar las claves de `data`; decidir el contrato exacto de `style` en la vista; resolver las tareas de exports y migración; y aprobar commit/merge.
