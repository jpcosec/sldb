## REFORMULACION

Encargo: en el repo `sldb`, decidir con evidencia si el tercer valor `incomplete` del lenguaje de predicados es alcanzable con un store real (armado con API pública en `tmp_path`, admisible enlazado y luego borrado/renombrado) mediante una evaluación pública (`where` o `rules check`). Si se demuestra, añadir test que lo obtenga y documente cuándo ocurre; si no, retirar `incomplete` del lenguaje, API (`GraphBackend.eval`, `StructuredQuery`, tipo de `holds`), tests de especificación y `docs/architecture/rules-language.md`, haciendo que lo que hoy devolvería `incomplete` devuelva `false` sin alterar resultados `true/false`. El test va en `tests/api/test_rules_evaluation.py`; `tests/test_predicates_cli.py` solo si nombra `incomplete`. Entregables: `result-summary.md` con la decisión y evidencia, tests, doc, CHANGELOG y commit, con las cuatro validaciones indicadas pasando.

## AMBIGUEDADES

1. "el tipo de holds": no aclara si el tipo tri-estado se elimina o se conserva como alias/retyping a `bool`; obligaría a inventar la superficie pública resultante.
2. "el mecanismo que check.sh --fast señala": no describe cómo actualizar el hash GO02; obligaría a inventar el procedimiento.
3. "evidencia de que ningún camino público lo produce (grep de cada sitio...)": no fija umbral de suficiencia (¿grep más argumento, o test fallido?); obligaría a inventar el criterio de decisión.
4. "una evaluación pública (where o rules check)": no dice si basta una o se exigen ambas; obligaría a inventar la cobertura.
5. "(H4)": etiqueta sin definir; obligaría a inventar su significado.

## DRY-RUN

Lecturas: `src/sldb/api/where.py`, `predicate_explain.py`, `predicate_reach.py`, `src/sldb/api/rules/`, `docs/architecture/rules-language.md`, `tests/test_predicates_cli.py`, `tests/api/test_rules_evaluation.py`, `CHANGELOG.md`. Cambios previstos: grep de emisores/consumidores de `incomplete`; intento de caso real con store enlazado no disponible e índice compuesto después; según resultado, test de alcance o retiro del valor y actualización de doc. Dependencias: API pública de store, `compose_edge_index`, `check.sh --fast`. Validaciones futuras: los cuatro comandos de Validation.

## FUTURO

El ejecutor produce `result-summary.md` y el commit; la suficiencia de la evidencia puede requerir revisión humana. El hash GO02 lo determina la salida de `check.sh --fast` en ejecución.
