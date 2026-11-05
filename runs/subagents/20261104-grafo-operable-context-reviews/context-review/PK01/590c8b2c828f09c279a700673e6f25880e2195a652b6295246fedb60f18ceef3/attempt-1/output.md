## REFORMULACION

PK01 es un agregado no ejecutable: su encargo es dejar fijados, antes de modificar el comportamiento del store, tres fundamentos del plan en sldb: (1) la frontera sldb/deskops reencuadrada, (2) la semántica y gramática del lenguaje de reglas, y (3) el protocolo `GraphBackend` con implementación networkx. Resultado del paquete: G_BOUNDARY, G_SEMANTICS y G_SEAM satisfechos, con documentos, commits y confirmaciones del dueño (D5, D6) como evidencia. Repo dueño: sldb. Límites: no cambia comportamiento existente; no autoriza ejecución; no incluye código del evaluador (eso es GO05 en adelante); no toca deskops.

## AMBIGUEDADES

1. "G_BOUNDARY: state: satisfied ... evidence: ... (commit pendiente en este plan)" frente a GO01 acceptance: "La pill y el atom están commiteados en main de sldb". El agregado no aclara si el gate ya está cerrado o si GO01 debe producirlo; obligaría a inventar el estado de partida real de GO01.
2. PK01 scope: "antes de tocar el store" frente a GO03 output_scope: "src/sldb/store/graph/backend*". Obligaría a inventar si escribir bajo `store/` cuenta como "tocar el store" o si solo se prohíbe cambiar comportamiento.
3. GO01 output_scope incluye "inbox de deskops" frente a brief §Fuera de alcance: "tocar deskops". Obligaría a inventar si una nota al inbox es una excepción admitida o un exceso de alcance.

## DRY-RUN

- **GO01**: lee pill, decisiones y estado de main; commitea pill+atom enlazado y deja nota en inbox de deskops; no cambia código. Salida: G_BOUNDARY con hash de commit citado.
- **GO02**: consume G_BOUNDARY; escribe `docs/architecture/rules-language.md` (gramática, Datalog estratificado, mundo cerrado, explicación, hash de contrato, tabla de equivalencia) y tests xfail; no implementa. Salida: G_SEMANTICS pendiente de revisión en frío y confirmación de D6.
- **GO03**: consume G_BOUNDARY; define protocolo `load`/`eval`, implementa networkx envolviendo compose+graph; goldens de los seis comandos; doc y selección por `store.yaml`. Salida: G_SEAM pendiente de revisión y D5.
- **Validación conjunta**: pytest sin rojos ni skips; goldens idénticos; revisión en frío de GO02 y GO03 aceptada; confirmaciones D5/D6 registradas; G_BOUNDARY cita commit existente.

## FUTURO

El dueño confirma D5 y D6; revisores en frío aceptan GO02 y GO03; GO05 retira los xfail; nodos posteriores consumen gramática y costura; deskops lee la nota y planifica su consumo.
