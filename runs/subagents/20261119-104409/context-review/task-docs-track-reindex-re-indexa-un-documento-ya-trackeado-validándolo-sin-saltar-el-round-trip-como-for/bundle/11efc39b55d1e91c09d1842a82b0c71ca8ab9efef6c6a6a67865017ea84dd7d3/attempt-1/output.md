REFORMULACION

Propósito: añadir `docs track --reindex` para re-indexar un documento ya trackeado en la misma ruta, validándolo como un `track` normal. Resultado: flag CLI, parámetro `reindex` en `track_document_file` y su paso a `StoreOperations.track`; rechazo conjunto con `--force`; tests, CHANGELOG, selfdoc y gates. Repo: `src/sldb/{api/documents,store,cli/parsers}`, `tests/api`, `CHANGELOG.md`. Límites: no cambia `--force`. Es un nodo ejecutable, no un agregado.

AMBIGUEDADES

1. «sobre un documento no trackeado se comporta como track». No aclara si `--reindex` sin documento previo equivale a `track` sin `force`; obligaría a inventar la condición exacta.
2. «se rechazan con un error claro». No fija excepción, mensaje ni código de salida; obligaría a inventarlos.
3. «deja el índice como estaba» y «el índice queda byte a byte igual». No delimita qué artefactos cuentan (shards, modelos, `store.yaml`); obligaría a inventar el conjunto comparado.
4. «el parser y el comando de docs track». Los archivos listados incluyen el parser, no el handler del comando; obligaría a inventar o descubrir su ubicación.
5. «aviso a sldb-ui» en Done When. No indica canal, destinatario ni formato; obligaría a inventar el mecanismo.

DRY-RUN

Lecturas: TaskDoc, rituales, átomo, `track_document_file.py`, `ops.py`, `docs1.py`, tests, comando CLI de `docs track`, selfdoc y `tools/check.sh`. Cambios previstos: añadir `--reindex` al parser y comando; propagar `reindex` por API y `StoreOperations.track`; ejecutar la validación normal cuando `reindex=True`; conservar `--force`; tests de reindex válido, inválido sin mutación, no trackeado y conflicto con `--force`; CHANGELOG y referencia CLI regenerada. Dependencias: camino `force`, `validate_model_input_roundtrip`, `check_entering_text`, `store_lock` y `_pre_check`. Validaciones futuras: los cinco comandos del TaskDoc, `selfdoc sync`, `selfdoc check` y `check.sh --fast`. No se ejecuta nada.

FUTURO

Otro nodo ejecutará implementación, tests y commit; un humano aprobará el mensaje exacto del conflicto, el canal de aviso y el closeout.
