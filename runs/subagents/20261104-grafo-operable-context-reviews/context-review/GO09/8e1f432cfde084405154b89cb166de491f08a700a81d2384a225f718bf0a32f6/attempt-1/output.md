REFORMULACION

GO09 es un nodo `code`/`delivery` del repo sldb, hijo de PK04. Encargo: fijar la convención documentada de `RelationDoc.attributes` para transiciones —`sets` (campo→valor) y `terminal` (booleano que sldb solo transporta)—, con defaults y errores de validación en `relation_doc.py`; resolver `{campo}` desde el payload del sujeto; hacer que `edges_holding` devuelva `effects = {sets resueltos, terminal}` por arista que se cumple; y una función pura `apply_effects(subject, effects, model)` que copia, reemplaza claves de primer nivel, valida el payload contra el modelo y nunca persiste. Límites: no evalúa `on_transition` ni `findings` (GO08), no persiste, no toca deskops. Depende de GO05 y requiere G_SEAM.

AMBIGUEDADES

1. Claves extra en `attributes`. Cita: “attributes debe ser un mapa, o estar ausente o null; otro tipo es error de validación” y “sets = mapa campo → valor…; terminal = booleano”. No dice si un mapa con claves distintas de `sets`/`terminal` se rechaza, se ignora o se transporta; obliga a inventar validación y contenido de `effects`.

2. `null` en `sets` y en `{campo}`. Cita: “los valores de sets son escalares o listas de escalares de YAML” y “un {campo} ausente en el sujeto hace que la arista no se cumpla”. No define si `null` es escalar, si puede asignarse, ni si un campo del sujeto con `null` cuenta como ausente; obliga a inventar `apply_effects` y validación.

3. Representación de escalares en la sustitución. Cita: “por str(valor) si el valor del sujeto es escalar”. Para booleanos, números no string o fechas, `str()` de Python no fija si se usa representación Python o YAML; obliga a inventar el payload esperado en tests.

DRY-RUN

Lecturas: `dag.yaml` (GO09, GO05, PK04, gates), brief, alcance, decisiones, `relation_doc.py`, `edges_holding.py`, validación de modelos, `docs/architecture/`, tests existentes. Cambios previstos: validar `attributes`/`sets`/`terminal` en `relation_doc.py`; resolver `{campo}` y añadir `effects` en `edges_holding`; implementar `apply_effects`; tests, doc de edges y CHANGELOG. Dependencias: GO05 (`where_subject`/sustitución y API única), G_SEAM y la validación de modelos existente. Validaciones futuras: pytest de la acceptance (tres estados/transiciones, sustitución, defaults, rechazo de payload inválido, doc, CHANGELOG) y revisión en frío. Sin ejecutar.

FUTURO

GO08 añadirá `findings` y `blocked` y evaluará `on_transition` sin tocar `effects`; deskops en G_CONSUMER probará retirar `sets_status`/`terminal` de su YAML; el TaskDoc de promoción fijará nombres exactos de archivos, funciones y tests; el operador del desk acepta la revisión y GO03 resuelve G_SEAM. No son ambigüedades del nodo.
