# REFORMULACION

Encargo ejecutable en el repo sldb: implementar GD27 para deskops. Propósito: g1, que `anchored_by` acepte `value: bare` y compare `f'{name}:{field}'`; g2, que `tag_models` en la declaración del store acote las reglas de tags a esos modelos y descendientes; g3, mantener `tag_folder` estricto y documentarlo; g4, añadir tests de regresión. Resultado: cambios en `src/sldb/api/stores/tag_namespace.py`, `store_declaration.py`, `builtin_tag_rules.py`, `src/sldb/api/tags/`, `src/sldb/cli/commands/tags.py`, `tests/`, `docs/architecture/tags.md` y `CHANGELOG.md`. Límites: no tocar deskops; conservar el comportamiento actual sin `value` ni `tag_models`; no subir límites de clean code; los 7 pasos del workflow los corre el coordinador.

# AMBIGUEDADES

1. «alcance de las reglas de tags por modelos» frente a «la familia builtin:tag_namespace (...) solo evalúa documentos de esos modelos». ¿`tag_models` filtra solo esa familia o todas las reglas de tags? Obligaría a inventar el alcance normativo.
2. «tag_tree y tag_check respetan el mismo alcance». No define si `tag_tree` omite raíces/aristas de modelos excluidos o solo deja de validarlas. Obligaría a inventar la semántica del árbol.
3. «Este nodo solo documenta la regla» frente a incluir `tag_folder` en alcance. ¿Se espera cambio de código o únicamente documentación? Obligaría a inventar si hay implementación.
4. «anchored_by admite una clave opcional 'value' con 'tag' (...) o 'bare'». No precisa dónde vive esa clave ni el esquema exacto de cada entrada. Obligaría a inventar el formato.

# DRY-RUN

Lecturas: task, `tag_namespace.py`, `store_declaration.py`, `builtin_tag_rules.py`, `src/sldb/api/tags/`, CLI de tags, tests filtrados por `tag_namespace|anchored_by|tag_tree|tag_check`, `docs/architecture/tags.md` y `CHANGELOG.md`. Cambios previstos: parsear `value: bare` y ajustar `anchors_of`/reglas; parsear `tag_models` y aplicar alcance; tests (a)-(c); documentación y changelog; `contracts/layers.toml` solo si aparece un archivo nuevo sin eje. Dependencias: índice `base_models`, esquema de declaración y CLI existentes. Validaciones futuras: tests de tags/reglas, `test_clean_code_rules.py`, `check.sh --fast` y workflow de 7 pasos. Sin ejecutar nada.

# FUTURO

El coordinador ejecuta los 7 pasos en clon limpio; deskops/CC35d adapta sus tags y el resto de su alcance; un humano revisa la decisión g3 y aprueba el cierre.
