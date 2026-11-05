## REFORMULACION
GO08 es un nodo `code` de entrega, hijo de PK04, en el repo sldb. Su encargo es evaluar reglas en tres momentos: `on_write` antes de persistir, rechazando la escritura si hay error; `on_transition` dentro de `edges_holding`, agregando `findings` y `blocked` sin tocar `effects` de GO09; y `on_check` en `stores check`, incluyendo anclas de GO07 y exit 1 solo ante error. Además: caché derivada y dirty set en `.sldb_cache`, evaluación incremental, punto fijo semi-naive para recursión, `edges check` validando condiciones, test end-to-end y medición. Límites: no implementa RuleDoc, anclas ni effects; no persiste hechos derivados; no retira shims; el gate `G_OPS_PREREQ` está pendiente.

## AMBIGUEDADES
1. «edges_holding evalúa las reglas on_transition cuyo sujeto es el documento». No dice si “el documento” es el nodo de origen, el documento sujeto/destino de la arista, o ambos. Obliga a inventar qué extremo aporta el payload y qué reglas pueden bloquear una arista.

2. «Dirty set: los documentos escritos desde la última evaluación registrada en esa caché más, cuando cambia el content_hash de una regla, todos los documentos de la familia de esa regla». No cubre cambios de aristas ni cambios de contrato de un documento referenciado por anclas cuando el documento que contiene el ancla no se escribe. Obliga a inventar si esos dependientes se invalidan; sin ello, «borrar .sldb_cache y reevaluar da los mismos findings» puede no cumplirse.

## DRY-RUN
Lecturas hipotéticas: contratos de GO06 (`RuleDoc`), GO07 (`check_doc_anchors`), GO09 (`effects`), `payload_save_steps`, `edges_holding`, `stores check`, `validation.py`, `edges.py`, `Finding`/`alert_sink`, índice de aristas y caché. Cambios previstos: cablear evaluación en los tres momentos; añadir `findings`/`blocked`; implementar caché, dirty set y punto fijo; validar condiciones en `edges check`; tests, `rules.md`, CHANGELOG y medición. Dependencias: GO06, GO07, GO09; `G_OPS_PREREQ` pendiente bloquea ejecución. Validaciones futuras: suite de aceptación, ejemplo end-to-end, recálculos=0, equivalencia tras borrar caché, terminación con ciclo, condición mal formada, medición de 20 escrituras, pytest y CHANGELOG.

## FUTURO
El Board de sldb resuelve `G_OPS_PREREQ`; el TaskDoc fija nombres, formato de caché, instrumentación y host de medición; GO10 retira shims; un humano dispone la revisión; deskops consume el resultado en `G_CONSUMER`.
