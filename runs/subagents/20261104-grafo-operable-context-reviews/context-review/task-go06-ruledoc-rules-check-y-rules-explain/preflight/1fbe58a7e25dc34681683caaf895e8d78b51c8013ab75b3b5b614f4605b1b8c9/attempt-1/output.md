## REFORMULACION

Encargo ejecutable en el repositorio `sldb`: implementar GO06 para que las reglas declaradas se autoricen como documentos. Debe crearse el modelo `RuleDoc` —sujeto como expresión `model <= X`, `where` opcional, `condition`, severidad `error|alert`, momento `on_write|on_transition|on_check` y `message` opcional— con validación pydantic al escribir y resolución del modelo contra el registro. Debe añadirse `api/rules` para resolver sujetos/reglas, `sldb rules check [--subject DOC]` y `sldb rules explain RULE SUBJECT`, con conversión a `Finding` de core y exits 0/1/2/3 según el contrato. También documentación en `docs/architecture/rules.md`, marca de reemplazo en `docs/opsys/bridge_primitives/README.md`, `CHANGELOG.md` y tests de aceptación y rechazo. Límites: quedan fuera evaluación incremental, cableado `on_write/on_transition`, anclas `doc:`, transiciones como datos y retiro de shims.

## AMBIGUEDADES

1. “el finding de eval tal como lo define GO02 (node, holds, clause, seen)” y “la clave del envelope para rules explain la fija este nodo (H10 de rules-language)”: no se da el esquema exacto ni la clave. Obligaría a inventar la forma del envelope.
2. “message seguido de la explicación de GO02”: no se especifica separador ni formato. Obligaría a inventar la concatenación de `Finding.what`.
3. “con solo el motivo en el envelope”: no se indica la clave del motivo para el exit 3. Obligaría a inventar ese campo.
4. “subject = el documento”: no se aclara si `Finding.subject` es ruta, identificador o representación serializada. Obligaría a inventar el tipo.

## DRY-RUN

Un ejecutor leería los ficheros listados, especialmente modelos, API/CLI existentes, `core/finding.py`, lenguaje de reglas, store y tests. Cambiaría: nuevo `rule_doc.py`; módulos `rules_check.py`, `rules_explain.py`, `rule_subjects.py`; parser, comando y dispatcher; docs, CHANGELOG y tests. Dependencias: lenguaje/evaluación de GO05, errores de documento desconocido, validación de escritura y contrato de `Finding`. Validaría después con `pytest tests/api/test_rules.py`, escenarios Base/X/Y/Z, exits y rechazos por campo, más `test_clean_code_rules.py` y `test_store_seams.py`. No se ejecuta nada.

## FUTURO

GO08 consumirá el `content_hash` para su caché; GO07/GO09/GO10 continúan el plan. El supervisor ejecutará la suite completa, la revisión en frío la decide un humano y la integración en `main` queda fuera de este nodo.
