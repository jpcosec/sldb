## REFORMULACION
Propósito: ejecutar en el repo `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`) la tarea descrita, implementando q1-q5. Resultado: creación/tracking de documentos evaluados por reglas `on_write`, `stores declare --write` conservando tags, evaluación estructurada de la familia de tags expuesta en JSON y documentación de alcance. Repo: `sldb`. Límites: no borrar el puente de deskops, no hacer que `stores build` evalúe `on_write`, no cambiar qué reglas existen. El nodo es un TaskDoc no ejecutable —no agregado ni paquete—: especifica trabajo para un ejecutor futuro.

## AMBIGUEDADES
1. “Hipótesis H4-H7 de CC35d resto de deskops (notas de inbox de sldb, la de H4 del puente q18 y la de H5-H7)”: faltan esas notas; obliga a inventar contexto y criterios de aceptación.
2. “q2 (H4), decisión del coordinador, revisable”: no aclara si el ejecutor debe esperar aprobación o implementar lo escrito; obliga a inventar el gate.
3. “El worker revisa si StoreDeclaration tiene otra clave autorada que declare --write pierda”: no lista las claves; obliga a inventar el catálogo o depender de inspección no descrita.
4. “los 7 pasos del workflow de sldb”: no se enumeran; obliga a inventar pasos y comandos.
5. “un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml”: no define “carpeta con eje” ni cómo elegir el eje; obliga a inventar la taxonomía.
6. “se dan de baja por CLI al cierre”: no indica comando; obliga a inventar la operación de cierre.

## DRY-RUN
Lecturas: TaskDoc, `docs/architecture/rules.md`, `docs/architecture/tags.md`, `contracts/layers.toml`, código en `src/sldb/api/{documents,rules,tags,stores}`, `src/sldb/cli/commands/`, tests y `CHANGELOG.md`; inspeccionar `StoreDeclaration`, `check_on_write`, `save`, `create_document`, `track_document_file` y salidas JSON.
Cambios previstos: q1 conservar `tag_namespaces`/`tag_models` y otras claves autoradas detectadas; q2 evaluar `on_write` en creación/tracking con propagación y rollback, sin evaluar en `stores build`; q3 añadir dato estructurado al hallazgo y exponerlo en `rules check`, `rules explain` y `tags check`; q4 documentar alcance; q5 tests y CHANGELOG.
Dependencias: maquinaria existente de reglas, esquema de declaración, serialización JSON y harness de tests.
Validaciones futuras: tests focalizados, suite completa de a un archivo desde `/dev/shm`, `test_clean_code_rules`, `tools/check.sh --fast`, workflow de 7 pasos en clon limpio. Sin ejecutar.

## FUTURO
El coordinador revisa/decide q2 y corre el workflow; el worker informa claves autoradas adicionales; otra tarea de deskops elimina su puente; el cierre por CLI lo ejecuta quien corresponda; un humano aporta las notas externas si faltan.
