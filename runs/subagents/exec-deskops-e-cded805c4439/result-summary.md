# Resultado
- py_calls.py: nuevo py_arg; call_parts da args/kwargs como {text,value} o {text,literal:false}; body_calls (attrs.calls) lleva args y kwargs; decoradores usan la misma forma. fingerprints.py intacto.
- Nota: text sale de py_norm, asi que "nodes" queda "'nodes'" (el encargo escribia '"nodes"'; sigo py_norm como pide la ruta).
- Los hechos call/assignment de py_statements tambien cambian de forma (usan call_parts); actualice sus expectativas en tests/selfdoc/test_treesitter_symbols.py.
- Docs: docs/architecture/code-anchoring.md (seccion nueva antes de la 9).
- Tests: tests/code/test_py_call_args.py (nuevo). Para correr hizo falta instalar el extra [code].
- Archivos: src/sldb/code/py_calls.py, docs/architecture/code-anchoring.md, tests/code/test_py_call_args.py, tests/selfdoc/test_treesitter_symbols.py
- Validacion: ver validation.log. run_id exec-deskops-e-cded805c4439
