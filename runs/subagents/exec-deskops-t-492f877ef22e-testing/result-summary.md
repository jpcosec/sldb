FALLA

# Resultado del tester

- **Task**: `task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización`
- **Rol**: tester
- **Run**: `run-deskops-t-492f877ef22e`
- **Session**: `scion://agent/deskops-t-492f877ef22e` (`session_sha256` vacío en el RunDoc)
- **Commit del ejecutor**: `6f14a3b537c4e3f2d72dbdee1880fbe3a2c465fb`
- **Archivos del commit**: `src/sldb/api/edges/project_graph/declared_target_nodes.py`, `tests/api/test_project_graph.py`, `CHANGELOG.md`

## Validaciones corridas

Todas las validaciones declaradas pasan (rc 0); ver `validation.log`.

| Comando | Resultado |
|---|---|
| `TMPDIR=/tmp python -m pytest -q tests/api/test_project_graph.py` | 14 passed |
| `TMPDIR=/tmp python -m pytest -q tests/api/test_project_graph_config.py` | 11 passed |
| `TMPDIR=/tmp python -m pytest -q tests/test_clean_code_rules.py` | 1212 passed |
| `TMPDIR=/tmp bash tools/check.sh --fast` | TODAS LAS PUERTAS PASAN |

Nota: `/tmp/ws-venv` no existe en este host; se usó el venv del repo (`/workspace/sldb/.venv`) con `python -m pytest` y `tools/check.sh`. No se corrió la suite completa. No existe `tests/test_declared_target_nodes.py`; el único test del módulo tocado es el nuevo de `tests/api/test_project_graph.py`.

## Bloqueo (por qué FALLA)

El Goal exige que un directorio existente declarado como target produzca nodo **y que `graph missing` no lo reporte**. Eso no se cumple cuando el target lleva `/` final, que es justamente la variante que usa el test nuevo:

- `target: generated` -> nodo `source_file:generated` (`file_kind: directory`) y `graph missing` vacío. Correcto.
- `target: generated/` -> nodo `source_file:generated` (`file_kind: directory`), pero `graph missing` sigue reportando `generated/` porque `declared_target_nodes` normaliza la ruta del nodo (le quita `/`) mientras la resolución de referencias (`NodeLookup`/`ReferenceField`) compara el valor crudo `generated/`.
- Reproducción end-to-end con un deskops sandbox y `target_identity: pkg/sub/`: `deskops graph missing` sale rc=1 con `missing_declared_target: materialization:... -> pkg/sub/`. Con `pkg/sub` sale rc=0.

Evidencia en `boundary.log` (sldb `ProjectGraph`) y `boundary-deskops.log` (`deskops graph missing`). El `CHANGELOG.md` del commit afirma “con o sin `/` final” y “`graph missing` ya no lo reporta”, pero la segunda mitad es falsa para el caso con `/` final.

Además, el test nuevo solo llama a `extract_file_nodes` y comprueba que el nodo existe. No ejecuta `graph.extraction().missing_targets` ni `graph missing`, así que no prueba el criterio principal del Goal; y para el directorio inexistente solo comprueba que no hay nodo, no que siga apareciendo como missing. Cobertura insuficiente del caso de aceptación.

## Guardrails que sí quedaron probados

- Un directorio existente genera un `FileNode` con el `kind` de la declaración y `file_kind: directory`.
- No se expande el directorio en un nodo por archivo.
- Un target inexistente no genera nodo.
- Las exclusiones se siguen aplicando.
- Las validaciones declaradas y los gates rápidos pasan.

## Follow-up antes del cierre

1. Normalizar la `/` final también al resolver la referencia/target declarado (o normalizar el valor de `target_identity`) para que el nodo `sin /` sea encontrado y `graph missing` no lo reporte.
2. Añadir regresión que afirme `missing_targets`/`graph missing` vacío para un directorio existente (con y sin `/`) y que afirme el missing para un directorio inexistente.
3. Corregir o acotar la viñeta del CHANGELOG si no se soporta el caso con `/` final.

El tester no modifica implementación ni tests; se devuelve al ejecutor.
