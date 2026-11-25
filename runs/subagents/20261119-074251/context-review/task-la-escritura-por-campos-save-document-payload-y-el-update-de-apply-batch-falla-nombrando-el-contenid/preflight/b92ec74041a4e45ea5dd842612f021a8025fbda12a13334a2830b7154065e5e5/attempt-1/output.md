## REFORMULACION

Nodo ejecutable `task.code` (no agregado ni paquete). Propósito: evitar que una escritura por campos borre en silencio contenido existente no declarado. Resultado: `save_document_payload` —y el `update` de `apply_batch` que pasa por él— falla antes de escribir si el archivo actual tiene ruido estructural o frontmatter no declarado; el error nombra lo que se perdería, el archivo queda intacto y los documentos limpios se escriben igual que hoy. Repo: `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`). Límites: aplicar la guarda en `src/sldb/api/documents/payload_save.py` y `payload_save_steps.py`, reutilizando `refuse_structural_noise` y `refuse_undeclared_frontmatter`; añadir tests en `tests/api/test_structural_noise.py` y `tests/api/test_transaction.py`; actualizar `CHANGELOG.md`. Fuera de alcance: un modo `force`.

## AMBIGUEDADES

1. «con el mismo tipo de excepción»: no nombra la clase ni el mensaje. Obliga a inventar el tipo exacto o asumir que es el de la creación.
2. «ruido estructural o frontmatter no declarado»: no define sus criterios ni contra qué modelo se compara. Obliga a inventar qué contenido cuenta como perdido.
3. «aviso a deskops y graph_ui»: no indica canal, formato ni responsable. Obliga a inventar el mecanismo de notificación.
4. «CHANGELOG»: no precisa entrada ni categoría. Obliga a inventar el formato y la redacción.

## DRY-RUN

Lecturas: `payload_save.py`, `payload_save_steps.py`, `refuse_structural_noise.py`, `frontmatter_keys.py`, `transaction_ops.py`, tests citados y `CHANGELOG.md`. Cambios previstos: insertar la guarda sobre el texto actual antes de re-renderizar en `save_document_payload`; reutilizar la excepción del camino de creación; cubrir escritura directa y `apply_batch update`, verificando archivo intacto y ausencia de escritura parcial; añadir tests y entrada de changelog. Dependencias: guardas existentes de creación y delegación de `apply_batch` en `save_document_payload`. Validaciones futuras: los seis comandos de `Validation`, incluido `tools/check.sh --fast`; tests nuevos en verde y documentos limpios sin cambios de comportamiento. Sin ejecutar nada.

## FUTURO

Otro nodo o un humano hará el commit, redactará/validará el aviso a `deskops` y `graph_ui` y decidirá si algún día se añade `force`. `graph_ui` consumirá la escritura segura mediante `apply_batch update`.
