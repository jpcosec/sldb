## REFORMULACION

Propósito: presentar a JP la decisión sobre las referencias por ruta que no resuelven a través de un store enlazado: (a) arreglarlas o (b) cerrarlas como wontfix documentado. Resultado: decisión registrada como recibo owner y consecuencia ejecutada: crear la tarea de código con test en `tests/api/test_unresolved_references.py`, o escribir la sección “Rutas a través de un store enlazado” en `docs/architecture/references.md`. Repo: sldb (`SLDB_1`), con fuentes citadas `src/sldb/store/edge_index/declared_resolution.py` y `composition_targets.py`. Límites: no implementar el arreglo; solo presentar opciones, obtener decisión y materializar la consecuencia. No es agregado ni paquete: es una tarea de decisión.

## AMBIGUEDADES

1. “Registrar el recibo owner (dispose accepted de JP)”: obliga a inventar formato, canal, artefacto y quién lo registra.
2. “Pedir la decisión”: no define canal, plazo ni formato de presentación; obliga a inventar la interacción.
3. “crear la tarea de código con test en tests/api/test_unresolved_references.py”: no aclara si la tarea debe editar el test o solo referenciarlo; obliga a inventar contenido y criterios de aceptación.
4. “sección ... y por qué”: no fija alcance ni criterios de redacción; obliga a inventar el texto y su nivel de detalle.
5. “grep ... || ls desk/tasks | grep -i enlazado”: acepta alternativas no equivalentes; obliga a inventar el criterio de validación de la decisión.

## DRY-RUN

Lecturas: ítem del drawer, `declared_resolution.py`, `composition_targets.py`, `docs/architecture/references.md` y la TaskDoc. Cambios previstos: ninguno antes de la decisión; si (a), crear una TaskDoc de código; si (b), editar la sección del documento. Dependencias: decisión de JP, recibo owner y acceso al repo. Validaciones futuras: confirmar recibo aceptado; ejecutar el grep de la sección o listar la tarea creada; en (a), comprobar que la tarea referencia el test; en (b), comprobar que la sección explica la resolución local. Sin ejecutar.

## FUTURO

JP decide (a) o (b) y emite el recibo owner. Un humano o coordinador registra `dispose accepted`. Si (a), otro nodo implementa el arreglo y ejecuta el test; si (b), documentación redacta la sección. El validador comprueba el cierre.
