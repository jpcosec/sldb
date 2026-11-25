## REFORMULACION
Propósito: obtener de JP la decisión sobre cómo resolver conflictos de git en los índices derivados de `.sldb` y dejarla registrada. Resultado: sección “Conflictos en los índices derivados” en `docs/versionado-y-colaboracion.md` con fecha ISO, opción elegida, motivo y las tres opciones con su costo; recibo owner aceptado por JP; tarea de código creada con `deskops add task`. Repo: `sldb`. Límites: no implementar; el hueco 2 solo entra en la tarea de código si JP elige (a) o (b); no push (solo el integrador); nada se ejecuta ni cierra sin recibo aceptado. Es un nodo de decisión, no un agregado o paquete.

## AMBIGUEDADES
1. “se crea con deskops add task la tarea de código que la implementa” es incondicional, pero los tests se nombran solo para (a)/(b) y no hay `implementation_path` para (c). Si JP elige (c), obliga a inventar alcance, archivos y validación.
2. “Hueco 2 de la nota: stores build sin store.yaml” no define el comportamiento esperado; “con su propio test, y su done_when lo nombra” obliga a inventar el criterio observable.
3. “references a la nota o ítem de origen de esta tarea” deja elegir entre la nota de inbox y esta tarea; obliga a inventar cuál referencia exacta.
4. Validación: “grep -n 'Conflictos en los índices derivados' docs/versionado-y-colaboracion.md” solo comprueba el encabezado, mientras Done When exige fecha, opción, recibo y tarea; obliga a inventar checks adicionales.

## DRY-RUN
Lecturas: TaskDoc, rituales `execution`, `testing` y `closeout`, atom citado, `docs/versionado-y-colaboracion.md`, nota de inbox y estado de desk. Cambios previstos: registrar review owner con la respuesta de JP; esperar dispose accepted; editar la sección con encabezado, línea “Decisión (AAAA-MM-DD, JP): …”, “Motivo: …” y lista de opciones/costos; crear la tarea de código con contrato completo y references; commit del documento con `deskops closeout commit`. Dependencias: respuesta de JP, recibo aceptado, `deskops` disponible y contenido de la nota. Validaciones futuras: grep del encabezado; revisar contenido, fecha y opción; verificar recibo accepted; comprobar `desk/tasks`; `closeout verify` y árbol limpio.

## FUTURO
JP elige la opción y acepta el recibo; el coordinador registra la respuesta. La tarea de código la ejecutará otro nodo. El push lo hará el integrador.
