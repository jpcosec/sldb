## Intento 2
- graph-backend.md: quitado incomplete (líneas 44, 51-52).
- sldb selfdoc sync regenera cmd-sldb-rules-explain (ya sin "2 incomplete"); selfdoc check sin alertas. El knowledge de symbols citado no existe en el repo.
- Restaurado tests/api/test_rules.py::test_save_document_payload_returns_the_on_write_alerts_without_a_listener desde HEAD~2 (al final del archivo), sin tocar el resto.
- 78 tests pasan. check.sh --fast rc=1 solo por identidad/workbench_demo (autorizada).
- Commit en rama deskops/deskops-e-5cfcba8143e9-a2 con Task-Id.
