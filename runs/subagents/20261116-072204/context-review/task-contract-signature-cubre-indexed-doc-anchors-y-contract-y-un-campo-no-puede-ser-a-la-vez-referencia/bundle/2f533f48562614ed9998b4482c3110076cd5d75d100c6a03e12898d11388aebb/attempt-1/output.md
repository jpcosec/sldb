REFORMULACION

Propósito: que `contract_signature` cubra `__indexed__`, `__doc_anchors__` y `__contract__`, de modo que cambiarlos marque stale los shards y el rebuild los reproyecte, y que un campo declarado a la vez en `__references__` y `__doc_anchors__` sea rechazado con `SLDBModelError`. Resultado: firma con las tres claves siempre presentes (listas ordenadas, vacías si no se declaran), docstring de `EdgeNodeRecord.contract_signature` actualizada, problema nuevo en `definition_problems`, tests en `tests/store/test_payload_projection.py` y `tests/api/test_doc_anchors.py`, `.sldb` del repo reconstruido en el commit, entrada en `CHANGELOG.md` y avisos a `deskops` y `graph_ui`. Repo: sldb; superficie: los cinco archivos de código/test listados más `CHANGELOG.md` y `.sldb/core`. Límites: no cambia la proyección del payload ni el cálculo de aristas de ancla; el ejecutor no hace commit ni push (lo hace el coordinador con `deskops closeout commit`); el informe va en `runs/subagents/<run-dir>/result-summary.md`. Es un nodo ejecutable, no un agregado.

AMBIGUEDADES

1. «agregar al cuerpo firmado "indexed": sorted(__indexed__ o []), "doc_anchors": sorted(__doc_anchors__ o []) y "contract": sorted(__contract__ o [])»: no dice si leer con `getattr` en crudo o mediante `indexed_fields`/`doc_anchor_fields`; usar los helpers haría que un modelo inválido lance al firmar. Obliga a inventar el modo de lectura.
2. «Test: run the relevant test or validation suite, smallest first, then the full suite when shared behavior changed» frente a una Validación que solo lista dos archivos de test y `stores build --check`: obliga a decidir si se ejecuta la suite completa.
3. «agregar __doc_anchors__ a un modelo con documentos ya indexados marca stale y el rebuild agrega la arista»: la fixture escribe el módulo de modelos una sola vez; no se indica cómo reescribirlo y recargarlo dentro del test. Obliga a inventar la mecánica de reimportación.

DRY-RUN

Lecturas: `model_contract.py`, `edge_node_record.py`, `doc_anchor_value.py`, los dos tests y el entorno de fixtures. Cambios previstos: ampliar `contract_signature` y su docstring; añadir el problema de doble declaración; tests de stale/rebuild para `__indexed__` y `__doc_anchors__` y de rechazo. Dependencias: `invalidate_runtime_cache`/`invalidate_shard_cache` y helpers ya usados por los tests. Validaciones futuras: los tres comandos de la sección Validación, más la decisión sobre suite completa; `stores build` para regenerar `.sldb`; avisos y entrada de CHANGELOG.

FUTURO

El coordinador ejecuta `deskops closeout commit` con el mensaje corto de la tarea e incorpora el `.sldb` reconstruido. `deskops` y `graph_ui` reciben el aviso y reconstruyen sus stores una vez. El cierre retira la tarea del Board. Si algún repo no está registrado, el aviso queda como línea en el informe.
