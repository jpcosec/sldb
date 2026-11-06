## REFORMULACION
Propósito: que la arista transporte su efecto de transición (`sets`, `terminal`) en lugar de que deskops lo guarde en su YAML. Resultado: convención validada en `RelationDoc.attributes`; `EdgeRecord.effects` rellenado solo por `edges_holding`; `apply_effects(subject, effects, model)` puro que devuelve el payload validado; doc de edges y CHANGELOG; pruebas de aceptación. Repo: `sldb`, nodo GO09 hijo de PK04. Límites: fuera findings por arista y orden (GO08), retiro en deskops (G_CONSUMER) y shims (GO10); nada se persiste; no se inventa API ante contrato ausente.

## AMBIGUEDADES
1. «src/sldb/api/edges/edge_effects.py» y «src/sldb/api/edges/apply_effects.py» figuran en `files`, pero el Goal solo describe `apply_effects` y «resolución de effects». Obliga a inventar qué contiene cada módulo y qué importa cada uno.
2. «effects no aparece en la serializacion cuando no tiene valor» no fija el mecanismo: campo opcional con `None`, exclusión en serialización o centinela. Obliga a inventar el tipo y la regla exacta de serialización de `EdgeRecord`.
3. «{campo} solo se sustituye dentro de valores string de sets» no aclara si alcanza a strings dentro de listas de escalares. Obliga a inventar si `sets: {tags: ["{x}"]}` sustituye.
4. «store de prueba con tres estados y tres transiciones» no dice cómo se construye ni con qué modelos/documentos. Obliga a inventar el fixture.

## DRY-RUN
Lecturas: task file, rituales execution/testing/closeout, `relation_doc.py`, `edge_record.py`, `edges_holding.py`, `api/__init__.py`, `docs/architecture/edges.md`, CHANGELOG y tests existentes. Cambios previstos: validador pydantic de `attributes`; campo `effects` en `EdgeRecord`; resolución de `{campo}` y defaults en `edges_holding`; `apply_effects` puro con sustitución YAML y validación contra `model`; exports, doc, CHANGELOG y `tests/api/test_edge_effects.py`. Dependencias: `payload_holds`/`fill_braces` de GO05, resolutor existente de modelos, pydantic. Validaciones futuras: las ocho de la sección Validation, incluida suite completa por el supervisor.

## FUTURO
GO08 añadirá `findings` sin tocar `effects`; deskops/G_CONSUMER retirará `sets_status`/`terminal`; el supervisor ejecutará la suite completa; la revisión en frío y la integración en `main` deciden cierre.
