# h47-worker: informe (H4-H7)

## Estado actual (commiteado antes del cambio)

- H4: `check_on_write` (`api/rules/rules_on_write.py`) solo se llama desde `save_document_payload`
  (`payload_save_steps.check_rules_on_write`). `create_document` y `track_document_file` no lo llaman;
  por eso un documento con tags sin ancla entra y solo `on_check` lo ve (rules.md H-GO08-6).
- H5: `declare_store._kept` conserva solo `generate` y `derived` de la declaración vigente. Las demás
  claves autoradas de `StoreDeclaration` que un índice no puede decir (`tag_namespaces`, `tag_models`,
  `policy`, `graph_backend`, `folders`, `seeds`, `project_graph`) se pierden con `stores declare --write`.
- H6: el hallazgo de la familia lleva su evaluación solo como texto (`cláusula (seen: {json})`);
  `tags check --format json` devuelve únicamente `findings`.
- H7: tags.md y rules.md no dicen que la familia solo ve documentos indexados.
