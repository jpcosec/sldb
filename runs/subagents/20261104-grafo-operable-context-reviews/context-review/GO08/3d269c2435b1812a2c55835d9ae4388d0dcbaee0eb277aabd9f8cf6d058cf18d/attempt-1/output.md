## REFORMULACION

GO08 es un nodo `code` de entrega en sldb, hijo de PK04. Su propósito es evaluar reglas en tres momentos: `on_write` (una regla `error` rechaza la escritura sin persistir; una `alert` deja pasar y reporta), `on_transition` (`edges_holding` agrega `findings` sin tocar `effects`, que es de GO09) y `on_check` (`stores check` evalúa reglas y `check_doc_anchors`, con exit 1 solo ante `error`). Incluye caché derivada por dirty set, hechos a punto fijo semi-naive nunca persistidos, validación de condiciones de arista, un test end-to-end Task/Review/ancla, medición antes/después de 20 escrituras y documentación en `rules.md` y CHANGELOG.

Repo dueño: sldb. Límites: no es dueño de `effects`; no persiste hechos derivados; no autentica actores; no introduce motor externo; no modifica deskops; requiere `G_OPS_PREREQ`, pendiente.

## AMBIGUEDADES

1. «en el orden de los ids de las reglas». GO06 define `RuleDoc` pero no un campo `id` ni su orden/tie-break. Obligaría a inventar qué identifica una regla y cómo ordenar findings.
2. «un finding error hace que la arista no se cumpla (la transición queda bloqueada y el finding lo explica)». `edges_holding` devuelve aristas que se cumplen; no se define si la arista bloqueada aparece en el resultado, con qué forma, ni dónde van sus `findings`. Obligaría a inventar el contrato de retorno.
3. «Caché derivada por dirty set cuya clave incluye los content_hash de las reglas (GO06)». No se define qué documentos entran al dirty set tras una escritura, transición o cambio de regla, ni cómo se reinicia. Obligaría a inventar la semántica de invalidación.

## DRY-RUN

Un ejecutor futuro leería `dag.yaml`, brief, alcance, decisiones y los contratos de GO06 (`RuleDoc`, hash), GO07 (`check_doc_anchors`, `anchor_state`) y GO09 (`effects`), más el código actual de `output_scope`. Cambiaría `payload_save_steps.py`, `edges_holding.py`, `api/stores/`, comandos `stores*` y `edges.py`, validación de aristas, `rules.md` y CHANGELOG; añadiría test e2e y medición. Dependencias: GO06, GO07 y GO09 cerrados, `G_OPS_PREREQ` resuelto y host de pytest indicado. Validaría la aceptación completa: rechazo/alerta, dos errores simultáneos, findings/effects, exits, incrementalidad contada, ciclo A→B→C→A, condición mal formada, e2e y medición. No ejecuta nada.

## FUTURO

El Board de sldb resuelve `G_OPS_PREREQ`; GO06, GO07 y GO09 entregan sus contratos; GO10 retira los shims; el dueño indica el host y acepta la disposición; deskops consume el resultado en `G_CONSUMER`.
