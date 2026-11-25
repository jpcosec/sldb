## REFORMULACION

El nodo corrige dos fallos detectados al integrar j02 (commit 7dbb6bc9) en el repo SLDB_1. **Propósito:** (1) clasificar AGENTS.md en la puerta de identidad, añadiéndolo a `EXEMPT` en `tools/check_identity.py` con un comentario que lo describa como guía de procedimiento para agentes; (2) lograr que `io/derived_guard.py` de `sldb.store.io` no importe `sldb.core` fuera de los seams permitidos. **Resultado:** `tools/check.sh --fast` y `tests/test_store_seams.py` pasan con j02 integrado, sin cambiar el comportamiento del merge driver, de rebuild-index ni el mensaje de error. **Límites:** no tocar la lista de seams del test ni otros archivos de j02.

## AMBIGUEDADES

1. «usar la excepción que ya usan los demás módulos de sldb.store.io (leer cómo lo hacen) o mover la importación a un seam permitido según tests/test_store_seams.py» — dos alternativas sin criterio de elección; obligaría a inventar cuál aplicar y cuál es la lista de seams, ya que el test no está incluido.
2. «con un comentario que diga que es la guía de procedimiento para agentes (merge de .sldb)» — la redacción exacta no está fijada; obligaría a inventarla.

## DRY-RUN

**Lecturas:** `tools/check_identity.py`, `src/sldb/store/io/derived_guard.py`, módulos vecinos de `sldb/store/io/`, `tests/test_store_seams.py`, `tests/store/test_update_fault_tolerance.py`, `contracts/identity.toml`.
**Cambios previstos:** añadir `AGENTS.md` a `EXEMPT` con comentario; ajustar el import de `derived_guard.py` usando la excepción existente o moviéndolo a un seam permitido.
**Dependencias:** j02 ya presente en el árbol; contrato de identidad sin modificar.
**Validaciones futuras:** los cinco comandos de la sección Validation, empezando por `test_store_seams.py` y `check.sh --fast`; verificar que el mensaje del índice derivado sigue nombrando el comando exacto. Nada ejecutado.

## FUTURO

El integrador/tester confirma con j02 integrado que ambas puertas pasan; un humano decide si acepta la excepción elegida o exige mover el import a un seam; el nodo de cierre realiza el commit atómico y retira la tarea del Board.
