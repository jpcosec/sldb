FALLA

# Testing — `notations from-graph` con `--label-field`, `--kind-field` y `--group-field`

## Veredicto

**FALLA por la puerta rápida obligatoria.** `bash tools/check.sh --fast` termina con **rc 1**:
la puerta `identidad` rechaza el directorio versionado `workbench_demo`, que no está clasificado
en `contracts/identity.toml`. La regla del rol de testing es explícita: rc distinto de 0 en
`check.sh --fast` ⇒ FALLA.

La violación es **preexistente y ajena a este cambio**: `workbench_demo` entró en `562847e2`,
es ancestro del commit del ejecutor, y ni el código de esta tarea ni su test tocan
`contracts/identity.toml` ni ese directorio. Las demás puertas pasan (`núcleo aislado`, `capas`,
`ejes`, `superficie`).

**Veredicto funcional: PASA.** El comportamiento pedido está implementado y los dos comandos de
validación de la tarea pasan. Si el coordinador acepta formalmente la roja preexistente de
`identidad` como excepción, no encontré un defecto que impida cerrar el contrato.

## Dónde está el trabajo

No hay commit con el `Task-Id` de esta tarea:

    git log -1 --format=%H --grep "Task-Id: task-sldb-notations-from-graph-..."  -> vacío

El código sí está commiteado en **`0f91540dfbaee9a0eae95b2c0a20b71db0ad1d78`** (HEAD), dentro de
un commit cuyo mensaje y trailer pertenecen a otra tarea (`on_write: save_document_payload...`).
`runs/subagents/exec-deskops-e-7567d415b0e8/result-summary.md` documenta que el índice compartido
arrastró sus archivos antes de que pudiera commitear con el trailer correcto. Para el closeout hay
que citar `0f91540d`; no existe un commit propio de esta tarea.

Archivos del cambio dentro de `0f91540d`:

- `src/sldb/api/notations/component_spec_fields.py` (nuevo): lectura de campo/`tag:<namespace>`,
  aplicación de label/kind y contenedores de grupo.
- `src/sldb/api/notations/component_spec_graph.py`: `payloads=`, `label_field=`, `kind_field=`,
  `group_field=` en `component_spec_from_graph`.
- `src/sldb/cli/commands/notations_from_graph.py`: carga los payloads del store solo con
  `--store` y algún flag.
- `src/sldb/cli/parsers/notations.py`: los tres flags en `_from_graph_filters`; el `--help`
  documenta que `--snapshot` no tiene payload (solo id y modelo).
- `tests/notations/test_notations_from_graph_cli.py`: tres tests nuevos.
- `CHANGELOG.md`: una línea bajo `0.1.13 — not released yet`.

## Validación ejecutada

Todo con `/tmp/ws-venv` en `PATH` (`/tmp/ws-venv` no existía; lo enlacé al `.venv` del repo,
Python 3.13.18), `PYTHONPATH=src` y `-p no:cacheprovider`. Log completo en `validation.log`.

| Comando / archivo | rc | Resultado |
|---|---|---|
| `TMPDIR=/dev/shm python -m pytest -q tests/notations/test_notations_from_graph_cli.py` | 0 | **9 passed** |
| `TMPDIR=/dev/shm python -m pytest -q tests/notations/test_component_spec_graph.py` | 0 | **16 passed** |
| `bash tools/check.sh --fast` | **1** | identidad FALLA solo por `workbench_demo`; el resto PASS |

Tests adicionales de los archivos de test incluidos en `0f91540d` (de a uno, `TMPDIR=/tmp`):

| Archivo | Resultado |
|---|---|
| `tests/api/test_on_write_entering.py` | 8 passed |
| `tests/api/test_rules.py` | 14 passed |
| `tests/matching/test_matching_refs.py` | 11 passed |
| `tests/store/test_diagnostics.py` | 17 passed |

No existen `tests/test_component_spec_fields.py` ni `tests/test_notations_from_graph.py`; la
cobertura de los módulos tocados está en los dos archivos de `tests/notations/` de la tabla.
No corrí la suite completa (la integra el host).

## Revisión del comportamiento

- `--label-field`: el label del nodo documento sale de `payload[campo]`; si falta o está vacío,
  cae al id (`apply_fields` usa `field_value(...) or node["label"]`). La prueba del contrato
  comprueba `title` en los cuatro repos.
- `--kind-field` y `--group-field`: aceptan `campo` o `tag:<namespace>`. Para el tag se recorre
  `payload["tags"]` y se toma el primer `"<namespace>:x"`, devolviendo `x`. En la prueba,
  `tag:system` produce kinds `a`/`b` y deja `RepoDoc` para el documento sin ese tag.
- Agrupación: `add_groups` crea un nodo `kind: group` con `label` = valor y una lista `contains`
  con los ids seguros de sus miembros. La prueba verifica dos contenedores (`a` con dos members,
  `b` con uno) y el spec valida (`_validated`).
- Sin flags: `_read_payloads` devuelve `{}` y `_Fields(payloads={}, ...)` no modifica labels/kinds
  ni crea grupos. El test de regresión confirma labels = ids, kinds = `RepoDoc` y ausencia de
  `contains`; los goldens de `test_component_spec_graph.py` siguen pasando.
- `--snapshot` con flags: no se leen payloads (solo `--store`), por lo que se mantiene id/modelo;
  está documentado en el `--help`.
- `--python`: los tres flags están en `_GRAPH_ONLY`, así que `from_graph` los rechaza igual que
  los demás filtros de grafo.

## Observaciones (no cubiertas por el contrato de la tarea)

1. **Colisión de ids de grupo.** Si dos valores distintos sanitizan al mismo id, se fusionan en un
   solo contenedor porque `_container` reutiliza cualquier nodo existente con `kind == "group"` sin
   comparar el `label`. Reproducido directamente con `component_spec_from_graph`:

       valores "Foo Bar" y "Foo_Bar" -> un único nodo group_Foo_Bar
       contains = [document_Doc_a, document_Doc_b]

   Los tests pedidos (`system:a` / `system:b`) no caen en este caso. Si se quiere garantizar «un
   contenedor por valor», `_container` debería comparar también el valor y desambiguar con sufijo,
   o usar el mismo esquema de ids únicos que `_unique_ids`.
2. **Stores enlazados.** `_read_payloads` usa `load_runtime_documents(..., include_linked=False)`,
   así que los documentos de stores enlazados no aportan payload y caen a id/modelo. El alcance
   pedido habla de «un store» local y el ejecutor lo anotó como limitación; no lo considero un
   incumplimiento del contrato probado.
3. **Atribución del commit.** El único riesgo para el closeout es que no hay commit con el trailer
   `Task-Id` de esta tarea. El código y su test están completos en `0f91540d`; el coordinador debe
   citarlo explícitamente o separar la historia si lo necesita.
