## REFORMULACION

Propósito: que la arista transporte el efecto de su transición y que sldb lo resuelva sin persistir. Resultado: convención `RelationDoc.attributes {sets, terminal}` validada en el modelo; `edges_holding` devuelve cada `EdgeRecord` con `effects = {sets resueltos, terminal}`; `apply_effects(subject, effects, model)` puro que devuelve el payload nuevo validado; documentación de la convención y CHANGELOG. Repo: sldb (`src/sldb`, `tests/api`, `docs/architecture`). Límites: OUTPUT_SCOPE `src/sldb/api/edges/`, `relation_doc.py`, `docs/architecture/`, `CHANGELOG.md`; fuera GO08 (findings/orden), retiro en deskops (G_CONSUMER) y shims GO10. Nada se persiste.

## AMBIGUEDADES

1. "EdgeRecord (atributo effects)" y "src/sldb/store/models/edge_record.py" frente a OUTPUT_SCOPE, que omite esa ruta: ¿puede modificarse `edge_record.py` o `effects` vive solo en la capa api? Obliga a inventar el alcance real.
2. "apply_effects(subject, effects, model)" y "el llamante lo conoce: edges_holding sabe el Model:name del sujeto": no se define si `model` es objeto, nombre `Model:name` o cómo resolverlo. Obliga a inventar firma y tipo.
3. "un {campo} ausente, null o no escalar hace que la arista no se cumpla" frente a "null sí es un valor asignable en sets (sets: {x: null} escribe null)": no queda claro si un placeholder que resuelve a null invalida la arista o escribe null. Obliga a inventar la semántica.
4. "strings tal cual" con "serialización YAML del escalar": no se especifica comillas ni escape de strings. Obliga a inventar el formato exacto.
5. "los tests existentes de edges_holding y de RelationDoc sin cambios" frente a añadir `effects` y validadores nuevos: no se aclara si aserciones existentes pueden romperse. Obliga a inventar compatibilidad.

## DRY-RUN

Lecturas: TaskDoc, `relation_doc.py`, `edge_record.py`, `edges_holding.py`, `edge_effects.py`, `apply_effects.py`, `edges/__init__.py`, `api/__init__.py`, `docs/architecture/edges.md`, `CHANGELOG.md`, `tests/api/test_edge_effects.py`, artefactos GO05 (`payload_holds`, `fill_braces`) y `alcance.md`.

Cambios previstos: validadores pydantic de la convención; atributo `effects` en `EdgeRecord`; resolución en `edges_holding`; `apply_effects` puro; exports; doc; CHANGELOG; tests de aceptación y de rechazo por regla.

Dependencias: GO05 (8be66bde), resolución de `Model:name`, fixtures de store de prueba.

Validaciones futuras: `TMPDIR=/dev/shm pytest tests/api/test_edge_effects.py`; tests de rechazo por regla; tests existentes de `edges_holding` y `RelationDoc`; `tests/test_clean_code_rules.py` y `tests/test_store_seams.py`; suite completa final del supervisor.

## FUTURO

GO08 añadirá `findings` a `EdgeRecord` sin tocar `effects`; GO10 abordará shims; deskops (G_CONSUMER) retirará `sets_status`/`terminal`; un revisor en frío aceptará el nodo; el supervisor correrá la suite completa e integrará en main; si falta contrato, se registrará la hipótesis (regla 6), sin inventar API.
