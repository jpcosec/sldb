---
sldb:
  by: agent
  at: '2026-11-16T08:24:21Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T22:48:28'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:24:05'
---

# IR13 pide migrar lo que queda de sldb sobre spec2viz (oráculo de D2, vistas.yml, identity.toml)

_Describe the incoming message with enough evidence to triage._

IR13 (gate de retiro de spec2viz, repo IR) pide migrar lo que queda de sldb sobre spec2viz. El retiro no está declarado y no se borra nada todavía: este es el pedido de migración que exige el gate (G4). Salida del comprobador `specir retirement check` (IR, solo lectura) sobre sldb, más lo que lista el inventario de `IR/docs/spec2viz/matriz-de-cobertura.md`:

1. Importación (oráculo de paridad de D2): `tests/notations/test_component_spec_python.py:43` `pytest.importorskip("spec2viz.generators.python_ast")`. Se salta sin spec2viz; al retirar, guardar la salida de spec2viz como golden o quitar la comparación viva.
2. Registro de catálogo que se construye con `spec2viz catalog build`: `docs/architecture/spec2viz/vistas.yml` y sus specs (`current-*.yml`, `python-ast.yml`) -> `specir catalog build --config docs/architecture/spec2viz/vistas.yml` (misma página que spec2viz byte a byte, IR13b). La ubicación de esos specs depende de la decisión del YAML (G7, pendiente de JP).
3. Configuración de contrato: `contracts/identity.toml:299` `consumers = ["deskops", "spec2viz", ...]` -> quitar spec2viz de la lista cuando se declare el retiro (no antes).

Pedidos previos de IR que siguen abiertos y bloquean filas del gate (sin duplicarlos): `20261115-192054` (comando para validar spec, notación y paleta: SV-K16, K21, K26, K29), `20261115-214942` (`matching/label-key-underscore`: SV-G08), `20261115-203456` (`code/scan-tree-nested-imports`, pérdida declarada en SV-F02).

Cuando esté resuelto, respondan con la referencia del commit para registrarla en `IR/docs/spec2viz/acta-de-retiro.md`.
