## REFORMULACION
Nodo ejecutable (`task.code`), no agregado. **Propósito:** desbloquear a deskops corrigiendo GD27 en sldb: aceptar `anchored_by` con valor sin namespace, acotar las reglas de tags por modelos y dejar `tag_folder` estricto documentado. **Resultado:** g1–g4 implementados, con tests verdes, `docs/architecture/tags.md` y `CHANGELOG`. **Repo:** sldb (`src/sldb/...`). **Límites:** no cambiar deskops; no subir los límites de `test_clean_code_rules`; no relajar `tag_folder`.

## AMBIGUEDADES
1. «anchored_by admite una clave opcional 'value' con 'tag' (por defecto, el comportamiento de hoy) o 'bare'»: no dice si `value` va dentro del diccionario `anchored_by` ni si un campo `bare` puede contener el tag completo; obliga a inventar esquema y validación.
2. «solo evalúa documentos de esos modelos o de sus descendientes (base_models del índice)»: no aclara la dirección de la herencia ni si `anchors_of` se filtra igual; obliga a inventar la semántica de alcance de las anclas.
3. «tag_tree y tag_check respetan el mismo alcance»: no define cómo afecta a `roots`, `orphans` y `unplaced`, ni a anclas de modelos fuera de `tag_models`; obliga a inventar el filtrado del árbol.
4. «Este nodo solo documenta la regla en docs/architecture/tags.md»: el documento ya describe el `ValueError` de segmentos vacíos; obliga a inventar qué texto falta.
5. «Los 7 pasos del workflow los corre el coordinador.»: los rituales incluidos no enumeran siete pasos; obliga a inventar el workflow.

## DRY-RUN
**Lecturas:** TaskDoc, rituales, los archivos listados, tests de tags/reglas y `contracts/layers.toml`. **Cambios previstos:** `TagNamespace.anchored_by` con `value`; `anchors_of`/`required`/`tag_tree` comparando `name:field`; `StoreDeclaration.tag_models`; filtro por modelo en `family_findings`, `tag_tree` y `tag_check`; tests g4; docs y CHANGELOG. **Dependencias:** pydantic, `RuleGraph`, índice de modelos; eje en `layers.toml` si aparece un archivo nuevo. **Validaciones futuras:** tests nuevos, suite de tags/reglas, `test_clean_code_rules`, `check.sh --fast` y los 7 pasos en clon limpio. Sin ejecutar nada.

## FUTURO
deskops adapta «CC35d resto» (`tag_folder`, namespaces); el coordinador ejecuta el workflow y mantiene la prioridad; un humano decide si g3 estricto es aceptable y si el alcance por `tag_models` basta.
