REFORMULACION
GO09 es un encargo de planificación (`code`, `delivery`) del repo sldb, hijo de PK04. Propósito: fijar una convención documentada para `RelationDoc.attributes` de una transición: `sets` campo→valor, `terminal` booleano que sldb solo transporta, defaults, validación en `relation_doc.py`, sustitución `{campo}` desde el payload del sujeto, y que `edges_holding` devuelva `effects` resueltos. Resultado: función pura `apply_effects(subject, effects, model)` que copia el sujeto, reemplaza claves de primer nivel, valida contra el modelo y no persiste; doc de edges y CHANGELOG. Límites: `output_scope` acotado a `api/edges`, `relation_doc.py`, `docs/architecture` y CHANGELOG; depende de GO05 y del gate G_SEAM; no evalúa reglas ni persiste (eso es GO08/GO10/deskops).

AMBIGUEDADES
1. «Convención documentada para `RelationDoc.attributes`» / «attributes ausente, o sin sets». No define si `attributes` debe ser un mapa ni qué hacer si existe con otro tipo (lista, escalar, null). Obliga a inventar si se rechaza, se ignora o se trata como ausente.
2. «sin terminal equivale a false; terminal con un valor no booleano es error». No aclara si `terminal:` (null) es ausencia o valor no booleano. Obliga a inventar el tratamiento de null.

DRY-RUN
Un ejecutor futuro leería `relation_doc.py`, `edges_holding.py`, validación de payload, docs de edges y tests actuales; añadiría validación de `attributes`/`terminal` al escribir `RelationDoc`; resolvería `sets` con la sustitución de GO05 en `edges_holding`; incorporaría `effects = {sets, terminal}` sin alterar la condición; implementaría `apply_effects` puro con copia, reemplazo y validación; y añadiría tests de los tres estados/transiciones, defaults, sustitución y rechazo. Actualizaría docs y CHANGELOG. Dependencias: GO05 y G_SEAM. Validaciones futuras: pytest, tests de aceptación y doc de edges. No se ejecuta nada.

FUTURO
GO05 aporta la sintaxis y fuente de `where_subject`; GO08 consume `effects` y agrega `findings`; GO10 retira shims; deskops verifica en G_CONSUMER que puede retirar `sets_status`/`terminal`; la revisión de GO03 resuelve G_SEAM; el operador del desk promueve el TaskDoc y acepta la revisión. Nada de eso es ambigüedad de GO09.
