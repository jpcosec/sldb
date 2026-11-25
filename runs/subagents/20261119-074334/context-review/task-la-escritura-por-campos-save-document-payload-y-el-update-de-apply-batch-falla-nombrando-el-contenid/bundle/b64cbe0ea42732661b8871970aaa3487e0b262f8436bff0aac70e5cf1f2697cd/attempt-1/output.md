## REFORMULACION

Encargo ejecutable (`task.code`): hacer que `save_document_payload` y el `update` de `apply_batch` dejen de borrar en silencio contenido. Propósito: "aplicar la misma guarda que al crear (refuse_structural_noise y refuse_undeclared_frontmatter sobre el texto actual del archivo) en el camino de save_document_payload (...) antes de re-renderizar". Resultado: la escritura por campos "falla antes de escribir, con un error que nombra lo que se perdería, y deja el archivo intacto; los documentos limpios se escriben igual que hoy". Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Superficie: `src/sldb/api/documents/payload_save.py`, `payload_save_steps.py`, `tests/api/test_structural_noise.py`, `tests/api/test_transaction.py`, `CHANGELOG.md`. Límite explícito: "No entra: un modo force para estas escrituras."

## AMBIGUEDADES

1. "con el mismo tipo de excepción" — no nombra la clase; obligaría a inventar si es `SLDBValidationError` (el que usa `track`) o `SLDBPayloadSaveError` (el del camino de guardado).
2. "aviso a deskops y graph_ui" — no fija canal ni verbo; obligaría a inventar el mecanismo del aviso.
3. "Los documentos limpios se escriben igual que hoy" — no define "limpio" para documentos ya trackeados con `force` que hoy arrastran ruido.
4. "falla antes de escribir" — no fija el orden frente a `pin_payload`, `check_rules_on_write` y `render_checked`; obligaría a inventar si la guarda precede a las reglas `on_write`.
5. "un error que nombra lo que se perdería" — no especifica formato del mensaje ni si reutiliza "ruido estructural en '...'" de los tests existentes.

## DRY-RUN

Lecturas: los cinco archivos del Implementation Path más `refuse_structural_noise.py`, `frontmatter_keys.py`, `transaction_ops.py`. Cambios previstos: importar ambas guardas en `payload_save_steps.py`, leer el texto actual de `doc_entry.path`, invocarlas antes de re-renderizar/escribir; tests nuevos en `test_structural_noise.py` (fallo con archivo ruidoso, archivo intacto) y `test_transaction.py` (`apply_batch update` con frontmatter extra, sin escritura parcial). Dependencias: que las guardas acepten texto y nombre, y que `force` de `track` siga funcionando. Validaciones futuras: los seis comandos listados (dos pytest de API, tres más y `tools/check.sh --fast`). Nada ejecutado.

## FUTURO

El ejecutor produce el commit (`fix(...)`), la entrada de CHANGELOG y el aviso; `deskops closeout` cierra la tarea y actualiza el Board. Un humano decide la clase de excepción y el canal del aviso si la ambigüedad persiste; `graph_ui` consume el nuevo comportamiento de `apply_batch update`.
