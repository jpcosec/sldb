REFORMULACION
GO05 es un nodo `code`/`delivery` del repo sldb: implementar el parser y evaluador del lenguaje fijado por GO02 sobre el backend de GO03 y la proyección de GO04, con booleanos completos, caminos cuantificados, clausura transitiva, sustitución desde el sujeto y explicación estructurada. Resultado: una API única que reemplaza `where_parse` y `FieldCondition` en `where_matches`, `edges_holding`, `StructuredQuery` y `--where`, dejando alias deprecados y tests de equivalencia; los xfail de GO02 en verde; consulta CLI con `any()/all()` y `--explain`; CHANGELOG y docs actualizados. Límites: no define gramática ni semántica (GO02), no diseña el backend (GO03), no proyecta payload (GO04) ni implementa `RuleDoc` (GO06).

AMBIGUEDADES
1. «Rendimiento: evaluar una regla sobre todos los documentos de un modelo en este repo no debe reextraer Markdown.» No indica cómo medirlo ni lo incluye en `acceptance`; obligaría a inventar instrumentación, umbral y si ese criterio bloquea el cierre.
2. «los dos lenguajes viejos quedan como alias deprecados con aviso y tests de equivalencia» no precisa si se conservan los parsers viejos o se traducen al nuevo, ni dónde se emite el aviso; obligaría a inventar el mecanismo de compatibilidad y su contrato.

DRY-RUN
Lecturas: documento de GO02, proyección de GO04, protocolo/implementación de GO03, `where_parse`/`FieldCondition`, tests xfail. Cambios previstos: `store/query_engine/`, `store/graph/language/`, `api/where.py`, CLI `--where`, tests de equivalencia. Dependencias: GO02 y GO04; GO03 llega transitivamente vía GO04; gates `G_SEMANTICS` y `G_SEAM`. Validaciones futuras: pytest de spec y equivalencia, CLI con envelope y `--explain`, comprobación de no reextracción, CHANGELOG y docs. Sin ejecutar.

FUTURO
GO02 produce la spec y `G_SEMANTICS` con confirmación de D6; GO03 produce `G_SEAM` con D5; GO04 entrega la proyección; la revisión en frío y el dueño resuelven gates; GO06 consume esta API.
