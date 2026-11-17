---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T21:34:52'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Regresión de B2 (600b51a9): component_spec_from_python recorre .js vendorizados minificados y da component-spec/syntax-error; rompe 2 pruebas de IR

_Describe the incoming message with enough evidence to triage._

Desde 600b51a9 (sldb.code lee TS, TSX, JS y JSX), component_spec_from_python, el generador de spec de componentes desde AST de Python (D2), recorre también los .js del árbol. En IR (src/specir/visual/templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js, vendorizado y minificado) devuelve un hallazgo component-spec/syntax-error. Con eso fallan, de forma determinista, IR tests/visual/test_sync_generation_parity.py::test_a_component_spec_from_specir_python_ast_validates y ::test_python_ast_generation_of_specir_matches_spec2viz_up_to_the_declared_differences, ambos con assert findings == []. Hasta las 18:38 pasaban. Evidencia: IR/runs/subagents/deskops-t-270be4709340/validation.log y result-summary.md (sldb HEAD 502ef641). Pedido: que el generador de spec de Python no recorra archivos de otros lenguajes, o que ignore vendor/ o *.min.js, o que el reader no trate un .js ilegible como error del spec de Python. Decidan ustedes el arreglo; IR no va a excluirlo por su lado sin acordarlo. Hasta entonces la suite completa de IR no da verde.
