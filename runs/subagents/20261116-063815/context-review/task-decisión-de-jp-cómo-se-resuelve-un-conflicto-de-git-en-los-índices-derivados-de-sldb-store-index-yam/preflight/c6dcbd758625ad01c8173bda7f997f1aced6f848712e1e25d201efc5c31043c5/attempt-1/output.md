## REFORMULACION

Encargo no ejecutable de decisión y coordinación: obtener de JP la elección entre tres opciones para resolver conflictos de git en los índices derivados de `.sldb` (`store_index.yaml`, `models/*.yaml`), documentarla y crear la tarea de implementación. Resultado: sección "Conflictos en los índices derivados" en `docs/versionado-y-colaboracion.md`, con fecha ISO, opción, motivo y costos; recibo owner aceptado; tarea de código en `desk/tasks`; commit del documento. Repo: `sldb` (cwd `SLDB_1`). Límites: no implementar; no hacer push; no cerrar sin recibo aceptado de JP. Si elige (a) o (b), la tarea hija incluye el hueco 2 (`stores build` sin `store.yaml`) con test propio. No es agregado con hijos previos: es un nodo de decisión que produce una tarea hija; esta se cumplirá después mediante otro ejecutor.

## AMBIGUEDADES

1. "docs/versionado-y-colaboracion.md": no indica raíz absoluta; obligaría a inventar si es `sldb/docs/...` o relativo a otro workspace.
2. "por el canal de coordinación (herdr o el supervisor)": no elige canal; obligaría a inventar cuál usar.
3. "con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when)": no fija contenidos; obligaría a inventar título, alcance y validaciones de la tarea hija más allá del hueco 2.

## DRY-RUN

Lecturas: nota de inbox, `docs/versionado-y-colaboracion.md`, atom citado y contrato de la tarea. Cambios previstos: registrar `deskops review record`, obtener `dispose accepted` de JP, escribir la sección, crear tarea con `deskops add task` y commit con `deskops closeout commit`. Dependencias: respuesta de JP, `deskops`, decisión registrada. Validaciones futuras: `grep -n 'Conflictos en los índices derivados' docs/versionado-y-colaboracion.md`; recibo aceptado; tarea existente; commit presente. Sin ejecutar nada.

## FUTURO

JP elige opción y acepta el recibo; el coordinador documenta y confirma el commit; el integrador decide push. Otro nodo ejecutará la tarea de código si corresponde.
