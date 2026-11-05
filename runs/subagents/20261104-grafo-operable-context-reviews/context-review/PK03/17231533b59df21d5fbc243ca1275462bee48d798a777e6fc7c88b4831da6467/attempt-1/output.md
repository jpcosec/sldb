## REFORMULACION

**Propósito:** empaquetar en sldb reglas como documentos y anclas/recibos atados a hash. **Resultado:** `sldb rules check` reporta findings con severidad y cláusula fallida; `sldb anchors check` reporta `intact/changed/lost` para anclas `doc:`. **Repo:** sldb. **Límites:** PK03 es `aggregate`, no se ejecuta ni se promueve; cierra cuando cierran GO06 y GO07. No incluye autenticación, hechos externos ni persistencia de derivados.

## AMBIGUEDADES

1. «Reglas como documentos y recibos atados a hash.» La aceptación solo exige «sldb rules check reporta findings con severidad y cláusula fallida; sldb anchors check reporta intact/changed/lost para anclas doc:». No hay criterio de aceptación para recibos atados a hash: el ejecutor tendría que inventar si validar recibos forma parte de PK03 o si basta con GO06/GO07 tal como están.

## DRY-RUN

Hipotético, sin ejecutar. PK03 no se promueve. Se promueven GO06 y GO07 por separado, tras preflight TaskDoc-only y gates.

- **GO06:** consume el lenguaje de GO05 y `G_SEMANTICS`; produce modelo `RuleDoc`, API/CLI de reglas y `docs/architecture/rules.md`.
- **GO07:** consume la proyección de GO04 y `G_SEMANTICS`; produce API de anclas, cambios en `provenance.py` y `docs/architecture/anchoring.md`.

No hay arista GO06→GO07: no se transfieren artefactos entre hermanos; ambos consumen sus prerrequisitos declarados. La validación conjunta sería en store temporal: reglas por familia aplicadas a subtipos y no a hermanos; error/alert con cláusula; regla mal formada rechazada; ancla `changed` al editar contrato, `intact` al editar fuera de contrato y `lost` al borrar; `anchors check` con política de alertas; regla que exige `anchor_state = "intact"`.

## FUTURO

Confirmación humana de D6 para `G_SEMANTICS`; entrega de GO05 y GO04; TaskDoc de cada hijo fija archivos, tests y comandos exactos; el Board o el humano cierra PK03 al verificar ambos hijos; deskops produce `G_CONSUMER` en su propio plan.
