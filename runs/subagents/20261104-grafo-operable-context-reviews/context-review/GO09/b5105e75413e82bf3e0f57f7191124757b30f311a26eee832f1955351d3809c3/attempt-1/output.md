REFORMULACION
El nodo GO09 (delivery, repo dueño sldb) define una convención para `RelationDoc.attributes` de una transición (`sets`, `terminal`), hace que `edges_holding` devuelva `effects` resueltos y añade `apply_effects(subject, effects)`, función pura que fusiona `sets` y valida sin persistir. Límites: `output_scope` (`src/sldb/api/edges/`, `src/sldb/models/relation_doc.py`, `docs/architecture/`), depende de GO05 y requiere G_SEAM; aceptación con store de prueba de tres estados y tres transiciones.

AMBIGUEDADES
1. “Aristas sin attributes se comportan como hoy (effects vacío, terminal false).” No define qué ocurre si `attributes` existe pero falta `sets` o `terminal`; el ejecutor tendría que inventar los valores por defecto.
2. “effects = {sets, terminal} ya resueltos (sustitución {campo} aplicada).” No indica de dónde se sustituye `{campo}` (payload del sujeto, arista, store) ni su sintaxis; obliga a inventar el mecanismo.
3. “apply_effects(subject, effects) → nuevo payload: copia del sujeto con sets fusionado en superficie y validado contra el modelo del sujeto.” La firma no recibe el modelo y el payload no necesariamente lo porta; hay que inventar cómo obtenerlo para validar.
4. `output_scope` lista “src/sldb/api/edges/, src/sldb/models/relation_doc.py, docs/architecture/”, mientras `alcance.md` regla 3 exige “entrada en CHANGELOG” para toda capacidad nueva. Cumplir una fuente excede el alcance o incumple la otra.

DRY-RUN
Lecturas: salida de GO05 (`edges_holding` sobre el lenguaje unificado), `RelationDoc` y `attributes`, `edges_holding` actual, `Validator`/modelo del sujeto, doc de `edges`, fixture de tres estados y tres transiciones. Cambios previstos: declarar/documentar la convención en `relation_doc.py`; resolver `effects` en `edges_holding`; añadir `apply_effects` puro; actualizar `docs/architecture/`. Dependencias: GO05 entregado; G_SEAM resuelto con confirmación de D5. Validaciones futuras: pytest del fixture con effects resueltos, rechazo de valor inválido, effects vacío sin `attributes`, texto de doc; si se resuelve el alcance, CHANGELOG. Nada se ejecuta.

FUTURO
GO05 entrega el lenguaje y `edges_holding`; GO03 produce G_SEAM y el dueño confirma D5; GO08 evalúa en escritura, transición y check; deskops verifica en G_CONSUMER el retiro de `sets_status`/`terminal`; el TaskDoc fija nombres exactos de archivos y tests.
