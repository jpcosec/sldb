# Result
run_id: exec-deskops-e-3f55d98569b3
Los hallazgos builtin de tag_namespace llevan fix: namespace sin declarar -> declarar en tag_namespaces de .sldb/store.yaml o cambiar tags (lista los declarados); anclas faltantes -> modelo/campo y tags que faltan. Es la única regla builtin de tags.
Archivos: src/sldb/api/rules/builtin_tag_findings.py, tests/api/test_tags.py (assert del fix existente + test nuevo; los tests de findings viven ahí, no en test_rules_evaluation.py, que pasa sin cambios), CHANGELOG.md.
Validación: ver validation.log (rc 0).
Pendiente: aviso a sldb-ui (coordinador). session/session_sha256: no aplica (sin sesión hija).
