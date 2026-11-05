## REFORMULACION

GO06 es un nodo de código del repo sldb, hijo de PK03, que define `RuleDoc`: sujeto como familia `model <= X` usando la herencia existente, `where` opcional, `condition`, severidad (`error|alert`), momento (`on_write|on_transition|on_check`) y `message` opcional. Incluye validación al escribir, registro como documento, y los comandos `rules check [--subject DOC]` y `rules explain RULE SUBJECT` con sus exits. Entrega además `docs/architecture/rules.md`, marca la sección `Constraint` como reemplazada y actualiza CHANGELOG. Límites: no define anclas `doc:` (GO07) ni la evaluación en escritura/transición/check (GO08); depende de GO05 para lenguaje y explicación, y del gate `G_SEMANTICS`.

## AMBIGUEDADES

1. Resultado `incomplete` en `rules check`: el input dice «level = severidad de la regla» y «exit 1 si hay al menos un Finding error». No define qué Finding, nivel o exit produce una condición `incomplete`; obligaría a inventar su tratamiento.
2. Finding cuando la condición es true en `rules explain`: dice «imprime el finding completo en el envelope; exit 0 si la condición es true». No aclara qué finding se imprime si no hay fallo; obligaría a inventar su forma.
3. Identificador `RULE` en `rules explain`: el input escribe «rules explain RULE SUBJECT» y «code = rules/<nombre de la RuleDoc>», pero solo aclara que DOC/SUBJECT aceptan «Model:name o ruta». No dice en qué forma se acepta RULE; obligaría a inventar el criterio de resolución.
4. Documento excluido por `where` en `rules explain`: el input dice «where ... false o incomplete = la regla no aplica a ese documento», pero los exits de explain solo cubren true/false/incomplete de la condición. No define el exit ni la salida cuando la regla no aplica; obligaría a inventar ese caso.

## DRY-RUN

Lecturas: `rule_doc.py` inexistente, registro de modelos y `base_models`, `finding.py`, API/CLI de documentos y envelope, contrato de GO05 (AST y explicación). Cambios previstos: crear modelo `RuleDoc` con validación, `api/rules/`, `cli/commands/rules.py`, `rules.md`, marcar `Constraint` y CHANGELOG. Dependencias: parser/evaluador y explicación de GO05; gate `G_SEMANTICS` aceptado. Validaciones futuras: store temporal con Base/X/Y/Z; herencia del sujeto; findings error/alert y exits; `--subject` por nombre y ruta; `explain` con exits 0/1/2; `where` excluyente; rechazo de reglas mal formadas; docs y CHANGELOG. Sin ejecutar nada.

## FUTURO

GO07 define anclas `doc:` y `anchor_state`; GO08 usa el `content_hash` de la regla en su caché y evalúa los tres momentos; GO09 aporta `effects`. El TaskDoc fijará nombres de archivos, funciones y tests. Un humano resuelve `G_SEMANTICS` y acepta la revisión en frío; deskops consumirá estas capacidades en su propio plan.
