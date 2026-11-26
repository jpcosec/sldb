# Result: task-una-notationdoc-declara-que-estandar-implementa-y-sldb-notations-validate-lo-muestra
Branch deskops/deskops-e-d61c09333b23 (worktree), one code commit (no Task-Id, per review note).
Tags semanticos no sirven (__semantics__ es de clase, sin validacion), asi que: campo opcional standard {name, version|None}.
Files: src/sldb/notations/notation_spec.py (StandardSpec + validacion que nombra la notacion), src/sldb/models/notation/notation_doc.py (campo + template), src/sldb/api/notations/notation_payloads.py, src/sldb/api/notations/notation_listing.py (clave "standards" solo si hay), src/sldb/cli/commands/notations_validate.py (texto "standard: <name> <version>"; con --json {findings, standard} solo si existe, si no la lista de siempre), docs/architecture/notations-and-views.md, tests/test_notation_declares_standard.py.
Revisar: el cambio de forma del JSON de validate cuando hay standard; list solo agrega "standards" si alguna notacion lo declara.
