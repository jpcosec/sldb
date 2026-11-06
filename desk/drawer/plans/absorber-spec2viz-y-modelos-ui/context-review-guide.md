# Guía para revisar un nodo de este plan

Va en todo input de revisión en frío. Deriva de `brief.md`, `alcance.md` y `decisiones.md`; no agrega requisitos.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende como **encargo de planificación y ejecución**: propósito, resultado, repo dueño (`sldb`), límites, dependencias (`SV01`–`SV04`) y aceptación comprobable.

## Cómo leer

- `dag.yaml` es la fuente de ids (`SV01`–`SV04`), aristas `depends_on` y gates `G_SV_*`.
- Una flecha `depends_on` significa prerrequisito → dependiente (`SV01 -> SV02 -> SV03`, con `SV04` independiente).
- Las decisiones `SV-D1` a `SV-D5` están registradas en `decisiones.md` y se leen como dadas.
- Ningún nodo de este plan modifica directamente otros repos (`spec2viz`, `graph_ui`, `deskops`); toda la absorción ocurre en `sldb` manteniendo compatibilidad hacia atrás (p. ej. alias `spec2viz.sldb_models:*` en `resolve_model_ref`).
