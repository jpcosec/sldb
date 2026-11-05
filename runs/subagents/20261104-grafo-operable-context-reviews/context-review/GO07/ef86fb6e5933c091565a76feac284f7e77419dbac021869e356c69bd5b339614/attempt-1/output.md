## REFORMULACION
GO07 es un nodo de entrega (`code`) del repo `sldb`, hijo de PK03, que debe añadir anclas `doc:<Model:name>`: guardar el hash de contrato visto y, opcionalmente, campos vistos; exponer `anchors check` con estados `intact / changed / lost` y política de alerta; implementar el `verify` de `provenance.md`; y hacer que el lenguaje de GO05 consulte `anchor_state`. Límites: `output_scope` en `src/sldb/api/anchors/`, `src/sldb/models/provenance.py`, `docs/architecture/anchoring.md`; depende de GO04 y requiere `G_SEMANTICS`. No autentica actores ni produce hechos externos.

## AMBIGUEDADES
1. **Contradicción de vocabulario.** GO07 dice “con el mismo vocabulario y la misma política que las anclas de código”; `alcance.md` lista para código “`intact / changed / reconnected / lost`”, pero GO07 enumera “`intact / changed ... / lost`”. Obliga a decidir si `reconnected` existe, cuándo aplica o si se contradice la fuente.
2. **Declaración del contrato.** “campos declarados por el modelo destino como contrato; default: todos los campos del payload” no define dónde ni cómo se declara ese subconjunto. La aceptación exige distinguir campo de contrato y fuera de contrato; obliga a inventar el mecanismo.
3. **Dependencia faltante de GO05.** El scope dice “consultables desde el lenguaje de GO05” y la aceptación “una regla puede exigir `any(reviewed_by: anchor_state = "intact" and verdict = "accepted")`”, pero `depends_on` solo contiene GO04. Obliga a inventar la integración o asumir un contrato no disponible; si GO05 es prerrequisito, falta la arista.
4. **Verify de provenance sin aceptación.** “Implementa de paso el verify diseñado en provenance.md: un documento con from: doc: cuyo destino cambió emite la alerta” no aparece en la aceptación. Obliga a definir su comportamiento y validación o dejarlo sin prueba comprobable.

## DRY-RUN
Lecturas hipotéticas: GO04, `provenance.md`, anclas de código, modelos y tests existentes, CHANGELOG. Cambios previstos: modelo/provenance, API `anchors`, `anchors check`, doc de arquitectura, tests y envelope. Dependencias: GO04 debe aportar `field_hashes`/`content_hash`; `G_SEMANTICS` debe estar aceptado; GO05 falta para la aceptación. Validaciones futuras: A/B con campo de contrato, fuera de contrato y borrado; política changed=alerta; consulta desde regla; verify de `from: doc:`.

## FUTURO
GO04 produce payload y hashes; GO02 y el dueño resuelven `G_SEMANTICS`/D6; GO05 produciría el lenguaje consultable; GO08 consumirá anclas; PK03 cierra cuando terminen GO06 y GO07. No son ambigüedades del nodo.
