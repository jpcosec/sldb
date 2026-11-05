## REFORMULACION
GO07 es un nodo delivery de código en sldb: define el ancla `doc:Model:name@sha256:<hash>` en campos declarados por `__doc_anchors__` y en `Provenance.from_`, la pinnea al guardar, deriva estados intact/changed/lost, expone `check_doc_anchors(store)` y extiende `anchors check`, implementa el verify de procedencia y agrega `<campo>__anchor_state` a la facet payload. Resultado: API, CLI, proyección, `docs/architecture/anchoring.md` y CHANGELOG. Repo dueño: sldb. Límites: sin `reconnected`, changed/lost solo alertas, no cablea `stores check` (GO08), no cambia el lenguaje (solo expone el campo), no autentica actores.

## AMBIGUEDADES
1. «GO07 agrega a la facet payload de GO04 ... una entrada derivada `<campo>__anchor_state` ... recalculada al reconstruir la proyección». No dice si esa entrada se persiste en el shard —y por tanto si GO07 altera claves o `EDGE_INDEX_VERSION`, que GO04 fija en cuatro claves y versión 5— o se calcula al leer. Obliga a inventar formato y compatibilidad.

2. «recalculada al reconstruir la proyección», con la aceptación de que editar el contrato de B deja el ancla de A en `changed`. GO04 invalida por `source_hash`/`contract_signature` del documento contenedor; editar B no marca stale a A. No hay disparador de recálculo. Obliga a inventar la invalidación o dependencia.

3. «en un camino que atraviesa un campo de ancla ... bajo el nombre anchor_state» y «any(^subject: anchor_state = "intact" ...)». No se fija si `^subject` es recorrido inverso de una relación o de un campo de ancla, ni cómo se adjunta el estado al elemento alcanzado. Obliga a inventar sintaxis/dirección y semántica de camino.

## DRY-RUN
Lecturas: GO02 (contrato de hash), GO04 (facet y staleness), GO05 (lenguaje), `provenance.py`, `payload_save_steps.py`, `anchors.py`, modelo base. Cambios: atributo `__doc_anchors__`, parseo/validación y pinneado, `check_doc_anchors`, CLI, entrada derivada, docs y CHANGELOG. Dependencias: GO04, GO05 y gate `G_SEMANTICS` pendiente. Validaciones futuras: tests de aceptación con A/B, edición dentro/fuera de contrato, borrado, alertas de `anchors check`, regla `any(^subject...)`, rechazo de valor no `doc:`, `provenance_changed`; pytest en el host indicado (robocop2); docs y CHANGELOG.

## FUTURO
GO08 cablea `stores check` y evalúa `on_check`; GO06 define `RuleDoc`; GO02 produce `G_SEMANTICS` y el contrato de hash; el TaskDoc fijará nombres exactos de archivos/funciones/tests; el desk de sldb dispone la revisión en `reviews/rN.md` y promueve con `deskops add task --from-drawer`.
