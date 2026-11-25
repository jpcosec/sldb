## REFORMULACION

Propósito: obtener de JP la decisión 6 —separar el store de sldb en paquete propio (a) o mantener el desacople interno (b)— y dejarla registrada. Resultado: sección "Decisión 6" fechada en `docs/architecture/store-extraction-proposal.md`, `desk/STANDARDS.md` sin la nota de pendiente, recibo owner con dispose `accepted` de JP, tarea de refactor con contrato completo si es (a), y commit del coordinador. Repo: sldb. Límites: no mover código, no hacer push (solo el integrador), nada se ejecuta ni cierra sin el recibo aceptado. Es un nodo de decisión: no lo ejecuta un agente, lo resuelve JP por el canal de coordinación.

## AMBIGUEDADES

1. "se crea la tarea de refactor que inyecta las tres costuras" contradice "El desacople del store dentro de sldb está hecho (beb8a99c)": obligaría a inventar qué costuras quedan por inyectar.
2. "vía la CLI que corresponda o en el commit del doc" frente a `STANDARDS.md` regla 4: "Los documentos que modela este desk (SPEC.md, STANDARDS.md) se editan con sldb fields update": obligaría a inventar qué vía prevalece para STANDARDS.md.
3. "un encabezado '## <nombre de la sección>'" no fija el texto exacto; la validación exige `grep -n 'Decisión 6'`: obligaría a inventar el encabezado literal.
4. "references a la nota o ítem de origen de esta tarea" no identifica la nota; obligaría a inventar cuál es.
5. "deskops review record <esta tarea>" no aclara si la tarea draft debe estar en el Board antes; obligaría a inventar el estado previo.

## DRY-RUN

Lecturas: `docs/architecture/store-extraction-proposal.md`, `desk/STANDARDS.md`, `tests/test_store_seams.py`. Cambios previstos: añadir la sección de decisión con fecha y motivo; reescribir la línea 19 de STANDARDS.md; crear la tarea de refactor si (a). Dependencias: respuesta de JP por herdr/supervisor, CLI deskops, recibo owner y dispose. Validaciones futuras: `grep -n 'Decisión 6'`, `TMPDIR=/dev/shm pytest -q tests/test_store_seams.py`, `deskops closeout verify`. Nada se ejecuta aquí.

## FUTURO

JP elige opción y motivo y hace el dispose `accepted`; el coordinador redacta vía deskops y ejecuta `deskops closeout commit`; el integrador hace push.
