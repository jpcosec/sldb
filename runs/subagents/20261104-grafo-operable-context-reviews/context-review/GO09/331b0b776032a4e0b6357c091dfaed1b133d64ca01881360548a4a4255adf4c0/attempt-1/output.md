## REFORMULACION
Propósito: convertir el efecto de una transición en datos de la arista (`RelationDoc.attributes`) y exponerlo resuelto, sin persistirlo. Resultado: convención documentada (`sets`, `terminal`, defaults, sustitución `{campo}`); `edges_holding` devuelve `effects = {sets resueltos, terminal}` con cada arista cumplida; función pura `apply_effects(subject, effects, model)` que reemplaza claves de primer nivel, valida contra el modelo y lanza error si no valida; tests, doc de edges y CHANGELOG. Repo dueño: sldb. Límites: `output_scope` (api/edges, `relation_doc.py`, docs/architecture, CHANGELOG); no persiste; no toca `findings` (GO08); no retira `sets_status`/`terminal` de deskops (eso es G_CONSUMER); depende de GO05 y requiere G_SEAM.

## AMBIGUEDADES
1. «terminal = booleano que sldb solo transporta. Defaults: [...] sin terminal equivale a false.» No define qué ocurre si `terminal` no es booleano (p. ej. un string YAML): ¿validar, coercionar o ignorar? Obligaría a inventar semántica de error/coerción y dónde se reporta. Resto: ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` (GO09, GO05, PK04, gates), brief/alcance/decisiones, el contrato de GO05 (`where_subject`, API única), `relation_doc.py`, `edges_holding.py`, docs/architecture y CHANGELOG, y tests existentes de edges. Cambios previstos: documentar y validar `attributes` de transición en `relation_doc.py`; en `edges_holding`, resolver `sets` —incluida sustitución desde el payload— y añadir `effects` solo a aristas cumplidas; implementar `apply_effects` puro con reemplazo de primer nivel y validación de modelo; tests de aceptación (tres estados/tres transiciones, sustitución, defaults, payload inválido); doc de edges y CHANGELOG. Dependencias: GO05 debe entregar parser/`where_subject` y API única; G_SEAM debe estar resuelto por GO03. Validaciones futuras: pytest en el host indicado, casos de aceptación, doc y CHANGELOG; sin persistencia.

## FUTURO
GO08 consumirá `effects` y añadirá `findings` sin modificarlo; GO10 retirará shims; deskops, en G_CONSUMER, podrá retirar `sets_status`/`terminal` de su YAML. La promoción y disposición de la revisión las decide quien opera el desk de sldb.
