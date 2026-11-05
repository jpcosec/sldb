## REFORMULACION

GO07 entrega en el repo sldb la capacidad de anclar un campo de documento a otro documento mediante el valor `doc:Model:name@sha256:<hash de contrato visto>`. Los campos anclables se declaran en `__doc_anchors__` y `Provenance.from_` admite la forma con hash. El ancla persiste en el texto del propio campo. Al guardar payload, un valor sin `@sha256` se pinnea con el hash de contrato actual del destino (definido por GO02); si el destino no existe, se guarda sin hash. `anchors check` y `stores check` derivan `intact/changed/lost`; `changed` y `lost` son alertas, nunca error; no hay `reconnected`. `anchor_state` queda consultable desde el lenguaje de GO05. Resultado: código en `src/sldb/api/anchors/`, modelos, pinneado, `docs/architecture/anchoring.md` y CHANGELOG, con aceptación comprobable. Límite: no define modelos de recibo ni autentica actores.

## AMBIGUEDADES

1. «si el destino no existe, se guarda sin hash y queda lost» junto a «evalúan cada ancla a intact (hash igual), changed (hash distinto) o lost (documento ausente)». Obliga a inventar qué estado reportar si el destino aparece después y el ancla sigue sin `@sha256`: no hay hash que comparar y el destino ya no está ausente. También si se re-pinnea o no.

2. «anchors check (y stores check, que lo invoca) evalúan cada ancla» y la aceptación «anchors check y stores check lo reportan como alertas», pero `output_scope` no incluye `src/sldb/api/stores/` ni `cli/commands/stores*`. Obliga a inventar si GO07 debe tocar stores check fuera de su alcance o solo exponer una función para que GO08 la invoque, y cómo se prueba esa aceptación.

3. «El verify de provenance.md es el mismo mecanismo aplicado a from:» y «emite provenance_changed». No se suministra `provenance.md` ni se fija el canal de emisión. Obliga a inventar si sale por `anchors check`, envelope o finding, y con qué formato.

## DRY-RUN

Lecturas: dag, brief, alcance y decisiones; artefactos de GO04 (facet payload, `field_hashes`, staleness) y GO05 (lenguaje); definición de hash de contrato de GO02. Cambios previstos: `api/anchors/`, `__doc_anchors__` en modelo base, forma con hash en `Provenance.from_`, pinneado en `payload_save_steps.py`, `anchoring.md` y CHANGELOG. Dependencias: GO04 y GO05 entregados; gate `G_SEMANTICS` resuelto. Validaciones futuras: tests de pinneado; `changed/intact/lost` editando contrato; regla `any(reviews: anchor_state = "intact" and verdict = "accepted")`; `provenance_changed`; alertas en ambos checks; pytest en el host indicado; docs y CHANGELOG.

## FUTURO

`G_SEMANTICS` lo resuelve la revisión en frío de GO02 aceptada. GO08 consume `anchor_state` y define la evaluación de `stores check`; GO06 provee `RuleDoc`. Un humano decide la promoción con `deskops add task --from-drawer`, task-type y files, y confirma host y medición.
