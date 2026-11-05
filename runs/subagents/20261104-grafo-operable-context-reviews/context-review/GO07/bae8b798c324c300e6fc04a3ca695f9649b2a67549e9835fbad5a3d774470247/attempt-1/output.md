REFORMULACION
Propósito: implementar en sldb anclas `doc:<Model:name>` que guarden el hash de contrato visto del destino, y `anchors check` que derive `intact/changed/lost` (sin `reconnected`), más el verify de provenance que emite `provenance_changed` cuando `from: doc:X` ve un contrato distinto. Resultado: API/CLI de anclas, campo derivado `anchor_state` consultable desde el lenguaje de GO05 y `docs/architecture/anchoring.md`. Repo: sldb. Límites: `changed` es alerta, nunca error; no hay `reconnected`; no autentica actores ni define modelos de recibo. Depende de GO04 (payload/field_hashes) y GO05 (lenguaje); requiere G_SEMANTICS.

AMBIGUEDADES
1. «Ancla doc:<Model:name> que guarda el hash de contrato visto … y, opcionalmente, los campos vistos». No define dónde se persiste el ancla (¿modelo nuevo, campo de `Provenance`, documento?) ni `output_scope` incluye un modelo de ancla; obliga a inventar el esquema.
2. «opcionalmente, los campos vistos»: no dice si es obligatorio implementarlo, cómo se declara ni su formato; obliga a decidir alcance y representación.
3. «emite la alerta provenance_changed»: no fija momento ni comando (¿`anchors check`, `stores check`, `edges check`, on_write?); obliga a inventar el disparador y la superficie.
4. «borrar B la deja lost; anchors check lo reporta con la política de alertas»: solo se fija que `changed` es alerta; la severidad de `lost` queda indefinida.

DRY-RUN
Lecturas: definición de `__contract__` de GO02, contratos de GO04/GO05, `provenance.md`, `code-anchoring.md`, `Provenance`/`CodeAnchorDoc`, índice de aristas, CHANGELOG y docs. Cambios: almacén del ancla, comparación de hash de contrato vía `field_hashes`, estados derivados, comando `anchors check`, `anchor_state` en el lenguaje, alerta `provenance_changed`, `anchoring.md`. Dependencias: GO04 y GO05 ejecutados; G_SEMANTICS resuelto. Validaciones: los casos de aceptación como tests pytest, envelope CLI, doc y CHANGELOG.

FUTURO
Humano: confirmar D6 y resolver G_SEMANTICS. GO04 entrega payload/field_hashes; GO05, el lenguaje con `anchor_state`. GO08 consume anclas y `provenance_changed`. deskops define los modelos de recibo. La promoción usa `deskops add task --from-drawer` con preflight.
