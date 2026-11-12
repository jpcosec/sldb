## REFORMULACION

Propósito: cerrar H4–H7 de CC35d y el seguimiento de GD27 en sldb. Resultado: (H4) `create_document` y `track_document_file` evalúan las reglas `on_write` como `save`; (H5) `stores declare --write` conserva `tag_namespaces` y `tag_models`; (H6) el hallazgo de la familia de tags lleva su evaluación estructurada y se expone en JSON; (H7) las guías de reglas y tags dicen qué documentos ve la familia. Repo: sldb (`src/sldb/api/*`, `src/sldb/cli/commands/`, `tests/`, `docs/architecture/{rules,tags}.md`, `CHANGELOG.md`, `contracts/layers.toml`). Límites: fuera borrar el puente de deskops, que `stores build` evalúe `on_write`, y cambiar qué reglas existen.

## AMBIGUEDADES

1. «El documento conserva su modelo y sus aristas del índice anterior a la escritura (H-GO08-3)» aplicado a «create_document y track_document_file evalúan las reglas on_write»: en un alta no hay índice anterior. Obligaría a inventar si el sujeto ve índice vacío, sin aristas, o el payload sin anclas.
2. «lleva su evaluación estructurada (namespace, tags, lo que falta) como dato propio» frente a «El nodo viaja en subject y la cláusula en what; Finding no gana campos»: obligaría a inventar dónde vive el dato y su forma exacta.
3. «rules check, rules explain y tags check la exponen en su salida JSON», cuando `explain` ya fija `{"node","holds","clause","seen"}`: obligaría a inventar si se añade al objeto `finding` o al sobre.
4. «El worker revisa si StoreDeclaration tiene otra clave autorada que declare --write pierda, y la suma si la hay»: no enumera el conjunto. Obligaría a inventar qué claves cuentan y si sumarlas está en alcance.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout/phase, `rules.md` §9.1 y §11, `tags.md` (familia y tabla de momentos), `layers.toml` (ejes `reglas`, `op_documentos`, `op_almacen`). Cambios previstos, en orden q1→q5: `declare_store`; llamada a `check_on_write` en `create_document` y `track_document_file`; dato estructurado en `builtin_tag_rules.py` y su serialización en los tres comandos; docs; tests y CHANGELOG. Dependencias: `rules_on_write.py`, `payload_save_steps.py`, `Finding`, `TagNamespace`. Validaciones futuras: tests por hipótesis, `test_clean_code_rules`, `tools/check.sh --fast`, suite por archivo desde `/dev/shm`, 7 pasos en clon limpio. Nada ejecutado.

## FUTURO

El coordinador corre los 7 pasos del workflow, decide sobre lo «revisable» y da de baja por CLI las notas H4/H5–H7 y el ítem de drawer. deskops retira su puente en otra tarea, cuando esta cierre.
