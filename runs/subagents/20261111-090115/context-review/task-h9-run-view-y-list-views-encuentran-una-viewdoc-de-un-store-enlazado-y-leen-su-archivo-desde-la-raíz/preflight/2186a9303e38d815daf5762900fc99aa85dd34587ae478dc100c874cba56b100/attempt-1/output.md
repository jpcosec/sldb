REFORMULACION

Propósito: corregir en el repo sldb (rutas `src/sldb/...`) la resolución, lectura, listado y evaluación de ViewDoc de un store enlazado. Resultado: `run_view`, `list_views` y `sldb serve` encuentran una ViewDoc alojada en un store B enlazado desde A, leen su archivo desde la raíz de B y la evalúan sobre A. No es un agregado: es una tarea ejecutable de depuración. Límites: en alcance `src/sldb/api/views/`, `tests/api/`, `docs/` y `CHANGELOG.md`; fuera, la forma del resultado de `run_view` y los agregados de deskops. Deben quedar implementados v1-v5, con causa raíz documentada, tests verdes, CHANGELOG y docs.

AMBIGUEDADES

1. “si ya está en main; si no, deja un TODO con la referencia a esa tarea”. No se da el identificador de la tarea de seguridad ni un criterio verificable de disponibilidad; obligaría a inventar la referencia o la comprobación.
2. “se evalúa sobre los documentos del store A (el que llama)”. No aclara si incluye los documentos enlazados de A o solo los propios; obligaría a inventar el alcance de evaluación.
3. “un archivo nuevo necesita eje en contracts/layers.toml”. Ese archivo no figura en alcance; obligaría a decidir si se puede editar o si debe evitarse crear archivos.
4. “los 7 pasos del workflow de sldb los corre el coordinador” frente a “7 pasos del workflow de sldb en clon limpio” en Validation. No fija si el ejecutor debe lanzarlos; obligaría a inventar su responsabilidad.

DRY-RUN

Sin ejecutar: lecturas previstas de `list_views.py` (`load_view`, `read_view`, `list_views`), índice compuesto, `open_store`/`project_root`, `sldb.store.source_read` si existe, tests de views, `contracts/layers.toml`, docs, CHANGELOG y referencia de seguridad. Cambios previstos: v1 resolución local y luego `<link>:ViewDoc:<name>` con error de ambigüedad; v2 lectura desde la raíz del store enlazado con guarda o TODO; v3 listado de enlazadas con nombre calificado en choque; v4 evaluación sobre A; v5 tests. Dependencias: guarda de seguridad, nomenclatura del índice y límites de clean code. Validaciones futuras: tests de views, `test_clean_code_rules`, siete pasos en clon limpio y revisión de docs/CHANGELOG.

FUTURO

La tarea de seguridad produce `sldb.store.source_read` y su referencia; el coordinador ejecuta los siete pasos y cierra; un humano decide cualquier excepción sobre `contracts/layers.toml`.
