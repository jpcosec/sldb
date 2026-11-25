## REFORMULACION

Propósito: exponer una API pública de lectura que devuelva, por campo de un modelo, el párrafo literal que ancla su extracción, para que deskops no use internos de sldb. Resultado: `sldb.api.template_anchors(model_type) -> dict[str, str]` en `src/sldb/api/model_registry/template_anchors.py`, reexportado en `sldb.api.__init__` y `__all__`, con tests en `tests/test_literal_paragraph_anchor.py` y una línea en `CHANGELOG.md`. Repo: sldb. Límites: no cambia render ni extract (opción b), no toca deskops; las recetas se reutilizan como las calcula el extractor, sin reparsear la plantilla. Tarea ejecutable (`task.code`), no agregado.

## AMBIGUEDADES

1. Criterio de asociación ancla→campo. Cita: "Ubicar en las recetas el anchor de tipo paragraph previo a cada campo" y "inmediatamente anterior al marcador del campo dentro de la misma sección". Obliga a inventar cómo se define "previo" en la lista de recetas (por `outer_index`, por orden de inserción, por `inner_path`) y qué ocurre con dos párrafos literales consecutivos.
2. Claves del dict. Cita: "devuelve, para cada campo cuyo marcador en __template__ va precedido…" y "el dict tiene exactamente las dos claves". Obliga a decidir si las claves son nombres de campo o nombres de marcador (`rev,markdown•body`).
3. Modelo de prueba. Cita: "para un modelo de prueba con dos campos anclados por párrafos en cursiva y uno sin ancla". Obliga a inventar nombres de campos y el `__template__` exacto.

## DRY-RUN

Lecturas: `src/sldb/core/template_extractor.py`, `src/sldb/runtime/validation.py` (65-68, recetas memoizadas), `tests/test_literal_paragraph_anchor.py`, `src/sldb/api/__init__.py`, `CHANGELOG.md`, `sldb/core/node_handler.py`. Cambios previstos: módulo nuevo, import y entrada en `__all__`, dos tests (con/sin ancla), línea de CHANGELOG bajo "## 0.1.13 — not released yet". Dependencias: split de nodos del template y recetas del extractor vía la misma llamada que `Validator(model).extract`; capa api→core. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_literal_paragraph_anchor.py`, `bash tools/check.sh --fast`, comprobar `from sldb.api import template_anchors`.

## FUTURO

El coordinador hace el commit y el aviso `deskops message send --to deskops`; si el repo no está registrado, el aviso va como línea en el informe. El ejecutor escribe `runs/subagents/<run-dir>/result-summary.md` y no hace push.
