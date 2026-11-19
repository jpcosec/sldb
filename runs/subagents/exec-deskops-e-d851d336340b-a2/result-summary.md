# Intento 2: result-summary

Fantasma: el nombre está en el índice de documentos de su modelo (no en store_index.yaml). `docs list` leía solo índices; `docs show` usa load_runtime_documents, que descarta los documentos de un modelo cuyo model_ref no importa (en sldb-ui `deskops.models:EdgeDoc`) o cuyo archivo falta/no se lee.

Cambios (commit con Task-Id):
- src/sldb/api/stores/unresolvable_documents.py: causa `model-not-importable`, resolviendo el model_ref como load_runtime_documents (pythonpath, luego raíz del store); acepta `pythonpath`.
- src/sldb/cli/commands/docs.py: pasa args.pythonpath.
- src/sldb/cli/parsers/docs2.py: `docs list --pythonpath`.
- tests/test_cli_v2.py: test_docs_list_marks_a_document_whose_model_does_not_import.
- CHANGELOG.md.

Validación: ver validation.log (todo rc 0). Contra UIs/sldb-ui el nombre del tester ahora sale con `unresolvable: model-not-importable`.
Revisar: la opción nueva `--pythonpath` en docs list (el formato de salida solo cambia por la marca). Aviso a sldb-ui: pendiente del coordinador (el marcado de 339 documentos EdgeDoc indica que el modelo deskops.models:EdgeDoc no importa en ese store).
