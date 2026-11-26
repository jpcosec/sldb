# Resultado
Commit en rama deskops/deskops-e-4bd1d7c961f8 (Task-Id trailer). Archivos: batch_edges.py, batch_simulation.py (nuevo), notation_listing.py, notations_validate.py, notations_validate_checks.py (nuevo), notation_spec.py, notation_spec_checks.py (nuevo), standard_spec.py (nuevo) bajo src/sldb/..., tests/api/test_api_creation.py, tests/mcp/test_no_writes.py.

- (1)(2)(4) funciones partidas en helpers del mismo archivo (notation_standards, _simulated, _standard_shown/validate, _violations).
- (3) StandardSpec movida a notations/standard_spec.py y reexportada via import en notation_spec.
- Ademas: el test de reglas tambien exige <=80 lineas efectivas por archivo y otras funciones largas (_layout, _standard_shape...) que el primer fallo ocultaba; se movieron helpers a modulos nuevos: api/documents/batch_simulation.py, notations/notation_spec_checks.py, cli/commands/notations_validate_checks.py. Sin cambio de comportamiento.
- (5) test usa monkeypatch.chdir(api_store.root); ya no queda cli.md en el cwd.
- (6) anchors_resolve agregado a tests/mcp/test_no_writes.py (target: primer .md del store copiado).
Validacion: ver validation.log. Suite completa la corre el host.
