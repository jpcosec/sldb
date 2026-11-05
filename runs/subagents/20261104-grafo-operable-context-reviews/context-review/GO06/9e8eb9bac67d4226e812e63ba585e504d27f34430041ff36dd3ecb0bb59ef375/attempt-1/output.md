## REFORMULACION
GO06 es un nodo `code`/`delivery` del repo sldb. Propósito: definir `RuleDoc` (sujeto `model <= X` con herencia existente más `where` opcional, `condition`, severidad `error|alert`, momento `on_write|on_transition|on_check`, `message` opcional), validarla al escribir y registrarla como documento. Resultado: comandos `sldb rules check [--subject DOC]` y `sldb rules explain RULE SUBJECT`, que emiten `Finding` por el canal existente con exits definidos, más `docs/architecture/rules.md` y la sección Constraint marcada como reemplazada. Límites: no persiste hechos derivados, no autentica actores, no define modelos de recibo, no ejecuta nodos dependientes; el formato de explicación es contrato de GO02 vía GO05.

## AMBIGUEDADES
1. «DOC en `--subject` y SUBJECT en explain aceptan Model:name o ruta; RULE acepta RuleDoc:<nombre>, <nombre> o ruta.» No se define qué ocurre si la referencia no existe o no resuelve a documento/regla: obliga a inventar exit code y mensaje para ese caso.
2. «cualquier fallo rechaza la escritura con el error» / «rechazada al escribirla con el error correspondiente». No se especifica la forma del error (código, campo, texto), y la aceptación no es comprobable sin fijarlo; obliga a inventar el contrato de error de validación.

## DRY-RUN
Lecturas previstas: `dag.yaml` (GO06, arista GO05, PK03), modelos y `core/finding.py` existentes, `edge_index`, guía y fuentes citadas. Cambios previstos: crear `src/sldb/models/rule_doc.py`, `src/sldb/api/rules/`, `src/sldb/cli/commands/rules.py`, `docs/architecture/rules.md`; editar `docs/opsys/bridge_primitives/README.md` y `CHANGELOG.md`. Dependencias: parser/evaluador de GO05 y explicación de GO02; gate `G_SEMANTICS` sigue `pending`. Validaciones futuras: pytest con store temporal Base/X/Y/Z, exits 0/1/2/3, incomplete como alert, rechazo de RuleDoc mal formada; sin ejecutar aquí.

## FUTURO
GO08 consume el `content_hash` de RuleDoc para su caché y evalúa reglas en escritura, transición y check; GO07 aporta anclas `doc:` usadas por reglas de consumidores; el desk de sldb promueve el nodo y registra su disposición; `G_CONSUMER` lo produce deskops.
